from flask import Flask, request, render_template, jsonify
from scenematch.rag.agentic_chat import detect_intent, chat_with_openai
from scenematch.rag.search import multi_stage_search
from scenematch.clients.client_setup import create_qdrant_local_client, create_openai_client
from scenematch.util import get_payloads
import os
from scenematch.web_app.model import SessionLocal, UserFeedback
from datetime import datetime,timezone
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

# Assume collection is created and embedded elsewhere or do it here if needed
# from scenematch.rag.collection_config import create_my_collection
# from scenematch.rag.embedding import embed
# create_my_collection(qdrant_client, collection_name, embedding_dim)
# embed(collection_name, filepath, qdrant_client)


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["message"].strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            chat_history.append(("bot", "Goodbye! Enjoy your movies 🎬"))
            return render_template("chat.html", chat_history=chat_history)

        # Detect intent
        intent = detect_intent(openai_client, user_input)

        # If intent is movie recommendation, get relevant docs from Qdrant
        if intent == "movie_recommendation":
            results = multi_stage_search(collection_name, qdrant_client, user_input, limit=10)
            if results:
                payload_str = "\n".join(get_payloads(results))
            else:
                payload_str = ""
        else:
            payload_str = ""

        # Generate response using OpenAI with context if any
        reply = chat_with_openai(user_input, payload_str, openai_client)

        # Append conversation to chat history
        chat_history.append(("user", user_input))
        chat_history.append(("bot", reply))

    return render_template("chat.html", chat_history=chat_history)

@app.route("/feedback", methods=["POST"])
def receive_feedback():
    data = request.form
    session = SessionLocal()

    try:
        rating_val = int(data.get("rating", 0))
    except ValueError:
        rating_val = 0

    feedback = UserFeedback(
        user_id=data.get("user_id", "anonymous"),
        session_id=data.get("session_id", "static-session"),
        message_id=data.get("message_id", ""),
        feedback_type="rating",
        rating=rating_val,
        comment=data.get("comment", ""),
        user_message=data.get("user_message", ""),
        model_response=data.get("model_response", ""),
        timestamp=datetime.now(timezone.utc)
    )
    try:
        session.add(feedback)
        session.commit()
        chat_history.append(("bot", "Thanks for your feedback! 👍"))
    except Exception as e:
        session.rollback()
        chat_history.append(("bot", f"Error saving feedback: {str(e)}"))
    finally:
        session.close()

    return render_template("chat.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
