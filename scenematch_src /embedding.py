
from qdrant_client import QdrantClient, models
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
                    "overview_dense": Document(
                        text=overview,
                        model="jinaai/jina-embeddings-v2-small-en",
                    ),
                    "tagline_dense": Document(
                        text=tagline,
                        model="jinaai/jina-embeddings-v2-small-en",
                    ),
                    "genre_sparse_bm25": Document(
                        text=" ".join(genres),
                        model="Qdrant/bm25",
                    )
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
    print(f"Inserted {len(points)} points into '{collection_name}'.")

def embed(collection_name: str, json_file: str, client: QdrantClient) -> None:
    docs = load_json(json_file)
    points = prepare_points(docs)
    upsert_points(client, collection_name, points)
