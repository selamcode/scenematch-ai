from qdrant_client import models
from qdrant_client import QdrantClient
'''
You correctly understood that:

prefetch runs first to fetch a candidate pool using the dense model (jina-small).

Then BM25 reranks that candidate pool — not the full collection.

The final results.points are BM25-scored results from the dense candidates.

This is exactly how multi-stage (hybrid) search works in Qdrant 1.10+.

'''

'''
Dense vector search (prefetch) → Candidate points
↓
BM25 search (main) → Rerank the candidates
↓
Final result (results.points)
'''
def multi_stage_search(collection_name:str,  client:QdrantClient, query: str, limit: int) -> list[models.ScoredPoint]:
    results = client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=models.Document(text=query, model="jinaai/jina-embeddings-v2-small-en"),
                using="overview_dense",
                limit=1 * limit
            ),
            models.Prefetch(
                query=models.Document(text=query, model="jinaai/jina-embeddings-v2-small-en"),
                using="tagline_dense",
                limit=1 * limit
            ),
            
            models.Prefetch(
                query=models.Document(text=query, model="jinaai/jina-embeddings-v2-small-en"),
                using="genre_dense",
                limit=1 * limit
            ),
            models.Prefetch(
                query=models.Document(
                    text=query,
                    model="Qdrant/bm25",
                ),
                using="overview_sparse_bm25",
                limit=(1 * limit),
            ),
        ],
        #query=models.FusionQuery(fusion=models.Fusion.DBSF),
        #with_payload=True,
        

        #you can use this too
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        with_payload=True,
       
    )

    return results.points
