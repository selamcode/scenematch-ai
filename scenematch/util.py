
from qdrant_client.models import ScoredPoint


def get_payloads(results: list[ScoredPoint]) -> list[str]:
    
    formatted = []
    for result in results:
        payload = result.payload
        title = payload.get("title", "Unknown Title")
        rating = payload.get("vote_average", "N/A")  # Will keep decimals like 8.1
        genres = ", ".join(payload.get("genres", []))
        
        text = f'Title: {title}, Rating: {rating}/10, Genres: {genres}'
        formatted.append(text)
    return formatted
