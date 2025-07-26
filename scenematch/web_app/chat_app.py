from flask import Flask, request, render_template, jsonify
from scenematch.rag.agentic_chat import detect_intent, chat_with_openai
from scenematch.rag.search import multi_stage_search
from scenematch.clients.client_setup import create_qdrant_local_client, create_openai_client
from scenematch.web_app.model import SessionLocal, UserFeedback
from datetime import datetime,timezone

app = Flask(__name__)

chat_history = []
collection_name = "movies-rag-main"
qdrant_client = create_qdrant_local_client()
openai_client = create_openai_client()

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["message"].strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            chat_history.append(("bot", "Goodbye! Enjoy your movies 🎬"))
            return render_template("chat.html", chat_history=chat_history)
        
        # Detect intent
        intent = detect_intent(openai_client, user_input)

        # Get search results based on intent
        if intent == "movie_recommendation":
            results = multi_stage_search(collection_name, qdrant_client, user_input, limit=10)
        else:
            results = []  # Empty list for general chat

        # Generate response using OpenAI with results directly
        reply = chat_with_openai(user_input, results, openai_client)

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
