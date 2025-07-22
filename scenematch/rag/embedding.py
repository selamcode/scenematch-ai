
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Document
from scenematch.util import load_json

def prepare_points(docs: list[dict]) -> list[PointStruct]:
    points = []
    for doc in docs:
        overview = doc.get("overview", "")
        tagline = doc.get("tagline", "")
        genres = doc.get("genres", [])
        keywords = doc.get("keywords", [])

        # Ensure keywords is a list of strings
        if isinstance(keywords, str):
            keywords_list = [keywords]
        elif isinstance(keywords, list):
            keywords_list = [str(k) for k in keywords if k]
        else:
            keywords_list = []

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
                    "keywords_dense": Document(
                        text=" ".join(keywords_list),
                        model="jinaai/jina-embeddings-v2-small-en",
                    ),
                    "overview_sparse_bm25": Document(
                        text=overview,
                        model="Qdrant/bm25",
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
                    "overview": overview,
                    "tagline": tagline,
                    "keywords": keywords_list,
                },
            )
        )

    return points


'''
def upsert_points(client: QdrantClient, collection_name: str, points: list[PointStruct]) -> None:
    
    client.upsert(
        collection_name=collection_name,
        points=points,
    )
    print(f"Inserted {len(points)} points into '{collection_name}'.")
'''

    
def upsert_points(client: QdrantClient, collection_name: str, points: list[PointStruct], batch_size: int = 500) -> None:
    
    total = len(points)
    print(f"Starting to insert {total} points into '{collection_name}' in batches of {batch_size}...")

    for i in range(0, total, batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch,
        )
        print(f"✅ Inserted batch {i // batch_size + 1} — Total so far: {i + len(batch)} / {total}")

    print(f"🎉 Finished inserting all {total} points into '{collection_name}'.")    

def embed(collection_name: str, json_file: str, client: QdrantClient) -> None:
    
    docs = load_json(json_file)
    points = prepare_points(docs)
    upsert_points(client, collection_name, points)
