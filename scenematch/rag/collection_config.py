from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, SparseVectorParams, Distance, HnswConfigDiff


def create_my_collection(
        client: QdrantClient,
        collection_name: str,
        embedding_dim: int = 384           # jina-embeddings-v2-small-en output size
) -> None:

    # ----- recreate collection if it already exists -----
    if client.collection_exists(collection_name=collection_name):
        print(f"Collection '{collection_name}' already exists – deleting so we can apply new schema.")
        client.delete_collection(collection_name=collection_name)

    print(f"Creating collection '{collection_name}' ...")

    # ----- dense vector fields (all share same dimension) -----
    vectors_config = {
        "overview_dense":  VectorParams(size=embedding_dim, distance=Distance.COSINE),
        "tagline_dense":   VectorParams(size=embedding_dim, distance=Distance.COSINE),
        "keywords_dense":  VectorParams(size=embedding_dim, distance=Distance.COSINE),
        "cast_dense":      VectorParams(size=embedding_dim, distance=Distance.COSINE),
        "director_dense":  VectorParams(size=embedding_dim, distance=Distance.COSINE),
    }

    # ----- sparse BM25 fields -----
    sparse_vectors_config = {
        "overview_sparse_bm25":  SparseVectorParams(modifier=models.Modifier.IDF),
        "genre_sparse_bm25":     SparseVectorParams(modifier=models.Modifier.IDF),
        "keywords_sparse_bm25":  SparseVectorParams(modifier=models.Modifier.IDF),
        "names_sparse_bm25":     SparseVectorParams(modifier=models.Modifier.IDF),
    }

    # ----- create collection -----
    client.create_collection(
        collection_name=collection_name,
        vectors_config=vectors_config,
        sparse_vectors_config=sparse_vectors_config,
        # optional index tuning; safe defaults
        hnsw_config=HnswConfigDiff(m=32, ef_construct=128)
    )

    print(
        f"Collection '{collection_name}' created with "
        f"{len(vectors_config)} dense + {len(sparse_vectors_config)} sparse fields."
    )
