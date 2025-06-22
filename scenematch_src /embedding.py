
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Document
from io_utils import load_json
def prepare_points(docs: list[dict]) -> list[PointStruct]:
    points = []
    for doc in docs:
        overview = doc.get("overview", "")
        tagline = doc.get("tagline", "")
        genres = doc.get("genres", [])
        
        points.append(
            PointStruct(
                id=doc["id"],
                vector={
                    "overview": Document(
                        text=overview,
                        model="jinaai/jina-embeddings-v2-small-en",
                    ),
                    "tagline": Document(
                        text=tagline,
                        model="jinaai/jina-embeddings-v2-small-en",
                    ),
                    "bm25": Document(
                        text=" ".join(genres),
                        model="Qdrant/bm25",
                    ),
                },
                payload={
                    "title": doc.get("title"),
                    "vote_average": doc.get("vote_average"),
                    "genres": genres,
                },
            )
        )

    return points

def upsert_points(client: QdrantClient, collection_name: str, points: list[PointStruct]) -> None:
    client.upsert(
        collection_name=collection_name,
        points=points,
    )

def embed(collection_name: str, json_file: str, client: QdrantClient) -> None:
    docs = load_json(json_file)
    points = prepare_points(docs)
    upsert_points(client, collection_name, points)
