import http.client
from qdrant_client import QdrantClient

def create_qdrant_local_client() -> QdrantClient:
    try:
        conn = http.client.HTTPConnection("localhost", 6333, timeout=2)
        conn.request("GET", "/")  # simple health check
        response = conn.getresponse()
        if response.status != 200:
            raise ConnectionError(f"Qdrant responded with status {response.status}")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        raise ConnectionError("Qdrant is not reachable at http://localhost:6333")

    print("✅ Qdrant connection established.")
    return QdrantClient(url="http://localhost:6333")
