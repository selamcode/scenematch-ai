from flask import Flask, request, render_template
from client_setup import create_qdrant_local_client, create_openai_client
from collection_config import create_my_collection
from embedding import embed
from chat import chat_with_user
import os
from dotenv import load_dotenv

app = Flask(__name__)

chat_history = []
qdrant_client = None
openai_client = None
collection_name = "movie-rag-test"
embedding_dim = 512

load_dotenv()
filepath = os.getenv("DATASET_JSON_TEST_PATH")
qdrant_client = create_qdrant_local_client()
openai_client = create_openai_client()
create_my_collection(qdrant_client, collection_name, embedding_dim)
embed(collection_name, filepath, qdrant_client)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["message"]
        raw_response = chat_with_user(user_input, collection_name, qdrant_client, openai_client)
        formatted = "<br>".join("🎬 " + line.strip() for line in raw_response.split("🎬") if line.strip())
        # Use class names 'user' and 'bot' to match CSS selectors
        chat_history.append(("user", user_input))
        chat_history.append(("bot", formatted))
    return render_template("chat.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
