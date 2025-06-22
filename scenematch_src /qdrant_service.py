# pip install qdrant_client
# pip install fastembed

from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, SparseVectorParams, Distance
#from fastembed import TextEmbedding # embedding model

import json

# Open the JSON file and load its content into a variable
with open('movies_test.json', 'r', encoding='utf-8') as f:
    movies_raw = json.load(f)

# Now `data` is a Python dict or list depending on your JSON structure
print(movies_raw[0])

# set up out movie client
movie_client = QdrantClient(url="http://localhost:6333")

# choose embedding model and embedding dimention

EMBEDDING_DIMENSIONALITY = 512
model_handle = "jinaai/jina-embeddings-v2-small-en"

# collection -> points -> upsert

# collection
# handle coolection already exist, invlaid config error (bad input)
collection_name = "movie-rag-test"

if not movie_client.collection_exists(collection_name=collection_name):
    movie_client.create_collection(
        
        collection_name=collection_name,
        vectors_config = {
            "overview_dense": VectorParams(
                size=EMBEDDING_DIMENSIONALITY,
                distance=Distance.COSINE
            ),
            "tagline_dense": VectorParams(
                size=EMBEDDING_DIMENSIONALITY,
                distance=Distance.COSINE
            ),
        },
        sparse_vectors_config={
            "genre_sparse_bm25":SparseVectorParams(
                modifier=models.Modifier.IDF,
            )
        }
    )
else:
    print("Collection already exists. Skipping creation.")




    



 




