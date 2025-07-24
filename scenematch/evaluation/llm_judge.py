import json
import openai
import os
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables
load_dotenv()

def get_llm_judgments(search_function, client, collection_name: str) -> Dict:
    """
    Returns dictionary mapping each query to its search results and LLM judgments
    """
    
    # Load ground truth from GROUND_TRUTH_PATH
    ground_truth_path = os.getenv("GROUND_TRUTH_PATH")
    if not ground_truth_path:
        raise ValueError("GROUND_TRUTH_PATH must be set in .env file")
    
    with open(ground_truth_path, 'r') as f:
        gt = json.load(f)
    
    query_judgments = {}
    all_queries = []
    
    # Collect all queries
    all_queries.extend(gt["ground_truth_data"]["descriptive_queries"])
    all_queries.extend(gt["ground_truth_data"]["less_descriptive_queries"])
    
    # Process each query
    for i, query_data in enumerate(all_queries, 1):
        query = query_data["query"]
        query_key = f"query_{i}"
        
        print(f"Processing {query_key}/{len(all_queries)}: {query[:50]}...")
        
        # Get search results
        search_results = search_function(collection_name, client, query, limit=10)
        
        # Extract only title, score, uuid, and genres
        extracted_results = []
        movies_info = []
        
        for point in search_results:
            extracted_result = {
                "title": point.payload.get("title", "Unknown"),
                "score": float(point.score) if hasattr(point, 'score') else 0.0,
                "uuid": point.payload.get("uuid", ""),
                "genres": point.payload.get("genres", [])
            }
            extracted_results.append(extracted_result)
            
            movies_info.append({
                "title": extracted_result["title"],
                "overview": point.payload.get("overview", "")[:100] + "...",
                "genres": extracted_result["genres"]
            })
        
        # Create LLM prompt
        prompt = f"""
Query: "{query}"

Movies: {json.dumps(movies_info, indent=2)}

For each movie, judge if it's relevant (1) or not (0) to the query.
Return ONLY a JSON array like: [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
"""
        
        # Call LLM
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Return only a JSON array of 0s and 1s."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            response_text = response.choices[0].message.content.strip()
            judgments = json.loads(response_text)
            judgments = (judgments + [0] * 10)[:10]
            
        except Exception as e:
            print(f"LLM call failed: {e}")
            judgments = [0] * 10
        
        # Store in dictionary
        query_judgments[query_key] = {
            "query_text": query,
            "search_results": extracted_results,
            "judgments": judgments,
            "relevant_count": sum(judgments)
        }
        
        print(f"Judgments: {judgments} (Relevant: {sum(judgments)}/10)")
    
    print(f"\n✅ Generated judgments for {len(query_judgments)} queries")
    return query_judgments

# Usage
if __name__ == "__main__":
    from scenematch.rag.search import multi_stage_search
    from qdrant_client import QdrantClient
    
    client = QdrantClient("http://localhost:6333")
    judgments_dict = get_llm_judgments(
        search_function=multi_stage_search,
        client=client,
        collection_name="movies"
    )
    
    # Save to EVALUATION_RESULT folder
    evaluation_result_dir = os.getenv("EVALUATION_RESULT")
    if not evaluation_result_dir:
        raise ValueError("EVALUATION_RESULT must be set in .env file")
    
    output_file = os.path.join(evaluation_result_dir, "llm_judgments_map.json")
    
    with open(output_file, "w") as f:
        json.dump(judgments_dict, f, indent=2)
    
    print(f"💾 Saved LLM judgments to: {output_file}")
