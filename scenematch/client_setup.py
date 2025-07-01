import http.client
from qdrant_client import QdrantClient
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def create_qdrant_local_client() -> QdrantClient:
    try:
        conn = http.client.HTTPConnection("localhost", 6333, timeout=2)
        conn.request("GET", "/")  # simple health check
        response = conn.getresponse()
        if response.status != 200:
            raise ConnectionError(f"Qdrant responded with status {response.status}")
    except Exception as e:
        print(f"Failed to connect to Qdrant: {e}")
        raise ConnectionError("Qdrant is not reachable at http://localhost:6333")

    print("Qdrant connection established.")
    return QdrantClient(url="http://localhost:6333")

def create_openai_client() -> OpenAI:
    try:
        client = OpenAI()  # Will auto-load API key from env var OPENAI_API_KEY
        print("OpenAI client configured.")
        return client
    except Exception as e:
        raise RuntimeError(
            "Failed to create OpenAI client. "
            "Make sure OPENAI_API_KEY is set and valid."
        ) from e