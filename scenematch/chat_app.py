from flask import Flask
from client_setup import create_qdrant_local_client, create_openai_client
from collection_config import create_my_collection
from embedding import embed
from chat import chat_with_user  # assuming this handles one message

import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load and initialize resources once
load_dotenv()
collection_name = "movie-rag-test"
embedding_dim = 512
filepath = os.getenv("DATASET_JSON_TEST_PATH")

qdrant_client = create_qdrant_local_client()
openai_client = create_openai_client()
create_my_collection(qdrant_client, collection_name, embedding_dim)
embed(collection_name, filepath, qdrant_client)