
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

