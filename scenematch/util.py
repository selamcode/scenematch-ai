
import json
from qdrant_client.models import ScoredPoint
import os

def load_json(filepath: str):
    filepath = os.path.expanduser(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_payloads(results: list[ScoredPoint]) -> list[str]:
    formatted = []
    for result in results:
        payload = result.payload or {}

        title = payload.get("title", "Unknown Title")
        overview = payload.get("overview", "No overview available.")
        rating = payload.get("vote_average", "N/A")
        vote_count = payload.get("vote_count", "N/A")
        tagline = payload.get("tagline", "")
        genres = ", ".join(payload.get("genres", []))
        keywords = payload.get("keywords", "")
        release_date = payload.get("release_date", "Unknown")
        runtime = payload.get("runtime", "Unknown")
        language = payload.get("original_language", "Unknown")
        popularity = payload.get("popularity", "N/A")

        text = (
            f"Title: {title}\n"
            f"Tagline: {tagline}\n"
            f"Overview: {overview}\n"
            f"Genres: {genres}\n"
            f"Keywords: {keywords}\n"
            f"Rating: {rating}/10 from {vote_count} votes\n"
            f"Release Date: {release_date}\n"
            f"Runtime: {runtime} minutes\n"
            f"Language: {language}\n"
            f"Popularity Score: {popularity}\n"
        )

        formatted.append(text.strip())

    return formatted


    
def format_payload_for_llm(payload_list: list[str]) -> str:
    """Format movie payloads in a minimal structure for LLM understanding"""
    if not payload_list:
        return "No movies available."
    
    formatted_movies = []
    for i, movie_data in enumerate(payload_list, 1):
        formatted_movies.append(f"Movie {i}:\n{movie_data}")
    
    return "\n\n".join(formatted_movies)


if __name__ == "__main__":
    from scenematch.rag.search import multi_stage_search
    from scenematch.clients.client_setup import create_qdrant_local_client
    
    # Test both functions together
    client = create_qdrant_local_client()
    results = multi_stage_search("movies-rag-main", client, "romantic comedies", limit=3)
    
    if results:
        print("=== Testing get_payloads ===\n")
        payload_list = get_payloads(results)
        
        print("=== Testing format_payload_for_llm ===\n")
        llm_formatted = format_payload_for_llm(payload_list)
        print(llm_formatted)
        
        print(f"\n=== Summary ===")
        print(f"Found {len(results)} movies")
        print(f"Formatted into {len(payload_list)} payload strings")
        print(f"Final LLM format length: {len(llm_formatted)} characters")
        
    else:
        print("No results found!")



