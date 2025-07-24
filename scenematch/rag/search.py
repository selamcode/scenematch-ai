from qdrant_client import models, QdrantClient 
from qdrant_client.models import Document

def multi_stage_search(collection_name: str, client: QdrantClient, query: str, limit: int ) -> list[models.ScoredPoint]:
    results = client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=Document(text=query, model="jinaai/jina-embeddings-v2-small-en"),
                using="overview_dense",
                limit=limit
            ),
            models.Prefetch(
                query=Document(text=query, model="jinaai/jina-embeddings-v2-small-en"),
                using="tagline_dense",
                limit=limit
            ),
            models.Prefetch(
                query=Document(text=query, model="jinaai/jina-embeddings-v2-small-en"),
                using="keywords_dense",
                limit=limit
            ),
            models.Prefetch(
                query=Document(text=query, model="Qdrant/bm25"),
                using="overview_sparse_bm25",
                limit=limit
            ),
            models.Prefetch(
                query=Document(text=query, model="Qdrant/bm25"),
                using="genre_sparse_bm25",
                limit=limit
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        with_payload=True,
    )
    
    # uncomment to see the data structure of points
    '''
    print(f"Full results object:\n{results}")
    print(f"Number of points found: {len(results.points)}")
    for i, point in enumerate(results.points):
        print(f"Point {i+1}: ID={point.id}, Score={point.score}, Payload keys={list(point.payload.keys())}")

    '''
   
    return results.points
