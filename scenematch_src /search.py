from qdrant_client import models
from qdrant_client import QdrantClient


def multi_stage_search(collection_name:str,  client:QdrantClient, query: str, limit: int = 3) -> list[models.ScoredPoint]:
    results = client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=models.Document(
                    text=query,
                    model="jinaai/jina-embeddings-v2-small-en"
                ),
                using="overview_dense",  # must match what's used in PointStruct
                limit=10 * limit
            ),
            models.Prefetch(
                query=models.Document(
                    text=query,
                    model="jinaai/jina-embeddings-v2-small-en"
                ),
                using="tagline_dense",  # also matching your stored vector names
                limit=10 * limit
            )
        ],
        query=models.Document(
            text=query,
            model="Qdrant/bm25"
        ),
        using="genre_sparse_bm25",  # this must match the sparse vector name
        limit=limit,
        with_payload=True
    )

    return results.points
