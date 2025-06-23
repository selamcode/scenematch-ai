from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, SparseVectorParams, Distance

def create_my_collection(client: QdrantClient, collection_name: str, embedding_dim: int) -> None:
    
    if client.collection_exists(collection_name=collection_name):
        print(f"Collection '{collection_name}' already exists. Skipping creation.")
        return

    print(f"Creating collection '{collection_name}'...")

    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "overview_dense": VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
            ),
            "tagline_dense": VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
            ),
            "genre_dense": VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
            ),
        },
        sparse_vectors_config={
            "overview_sparse_bm25": SparseVectorParams(
                modifier=models.Modifier.IDF
            )
        }
    )

    print(f"Collection '{collection_name}' created.")
