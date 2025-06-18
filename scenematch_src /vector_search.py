# pip install qdrant_client
# pip install fastembed

from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client import QdrantClient, models
import json

# Open the JSON file and load its content into a variable
with open('movies.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Now `data` is a Python dict or list depending on your JSON structure
print(type(data[0]))




