from scenematch.util import get_payloads, format_payload_for_llm
from qdrant_client.models import ScoredPoint

# The result will be the result we get from our muti_stage_search AKA top-k
def build_prompt(user_input: str, results: list[ScoredPoint]) -> str:
    role = """
    You are MovieBot, a friendly and intelligent assistant that helps users discover movies based on their input.
    """

    task = """
    Your goal is to recommend 3 movies that best match the user's request.
    """

    conditions = """
    Conditions:
    - You are given a numbered list of the top k movie results retrieved from a vector database (Qdrant).
    - Only choose your final 3 recommendations from this top k list — do not invent or add new movies.
    - Use genre information and user intent to help refine your recommendations.
    - If Qdrant scores are close, prioritize emotional fit using genres.
    - Each recommendation must not exceed 50 words.
    - Include a rating (IMDb or general 1–10 score).
    """

    consider = """
    When selecting movies, always consider:
    - Age appropriateness
    - Language preferences (e.g., subtitles, dubs)
    - Mood (e.g., light, emotional, suspenseful)
    - Variety (not all mainstream or obscure unless asked)
    - Cultural and personal sensitivity
    """

    output_style = """
    Format and Tone:
    - Use emojis 🎞️ before each movie.
    - Format: 🎞️ → Movie Title (Rating) – Description
    Example: 🎞️ → The Matrix (8.7/10) – A hacker discovers reality is a simulation.
    - Keep descriptions short, helpful, and spoiler-free.
    - Use a warm, conversational tone like you're chatting with a friend.
    """

    example = """
    Example:

    User: I want something feel-good and inspirational.

    A:
    🎞️ → The Intouchables (8.5/10) – A rich quadriplegic and his caregiver form a life-changing friendship in this uplifting French film.

    🎞️ → The Pursuit of Happyness (8.0/10) – A struggling father never gives up on his dreams in this powerful story of perseverance.

    🎞️ → Chef (7.3/10) – A chef rediscovers joy, creativity, and family through a food truck journey across the U.S.
    """

    # Format top k search results for LLM
    if results:
        payload_list = get_payloads(results)
        top_k_movies = format_payload_for_llm(payload_list)
    else:
        top_k_movies = "No movies found."

    context = f"""
    User Request: {user_input}

    Top K Movies (Ranked by Relevance):
    {top_k_movies}
    """

    full_prompt = f"""
    {role}

    {task}

    {conditions}

    {consider}

    {output_style}

    Here is how your response should look:
    {example}

    {context}
    """

    return full_prompt
if __name__ == "__main__":
    from scenematch.rag.search import multi_stage_search
    from scenematch.clients.client_setup import create_qdrant_local_client
    
    print("=== TESTING build_prompt FUNCTION ===\n")
    
    # Setup
    client = create_qdrant_local_client()
    collection_name = "movies-rag-main"
    test_query = "action movies with good ratings"
    
    print(f"Test Query: '{test_query}'")
    print("="*50)
    
    # Get search results
    results = multi_stage_search(collection_name, client, test_query, limit=5)
    
    if results:
        print(f"\nFound {len(results)} movies\n")
        
        # Test build_prompt function
        full_prompt = build_prompt(test_query, results)
        
        print("=== GENERATED PROMPT ===\n")
        print(full_prompt)
        
        print(f"\n=== PROMPT STATS ===")
        print(f"Total prompt length: {len(full_prompt)} characters")
        
        # Fix: Use a variable for newline
        newline = '\n'
        print(f"Number of lines: {len(full_prompt.split(newline))}")
        
    else:
        print("No results found! Check your Qdrant connection.")
