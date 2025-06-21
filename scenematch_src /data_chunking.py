# pip install qdrant_client
# pip install fastembed

from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding # embedding model
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
collection_name = "movie-rag-test"
try: 
    movie_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size = EMBEDDING_DIMENSIONALITY,  # Dimensionality of the vectors
            distance=models.Distance.COSINE  # Distance metric for similarity search
        )
    )
except UnexpectedResponse as e:
    if "already exists" in str(e):
        print("Collection already exists. Skipping creation.")
    else:
        raise e


 




