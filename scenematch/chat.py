from prompt import build_prompt
from util import get_payloads
from qdrant_client.models import ScoredPoint
from search import multi_stage_search 
from client_setup import create_qdrant_local_client, create_openai_client

def detect_intent(openai_client, user_input: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You're an intent classifier. Given the user message, classify the intent as 'movie_recommendation' or 'general_chat'. Only respond with one of those two strings."},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )
    intent = response.choices[0].message.content.strip().lower()
    return intent

def chat_with_openai(user_input: str, payload_str: str, openai_client) -> str:
    system_prompt = (
        build_prompt(user_input, payload_str)
        + "\nInstructions for the assistant:\n"
        + "- Avoid repeating greetings if they have been said before.\n"
        + "- Do not add generic or filler phrases.\n"
        + "- Keep responses concise, relevant, and focused on the user's question.\n"
        + "- If context is missing, politely ask for clarification without repeating previous prompts.\n"
        + "- Do not assume information not provided by the user or retrieved documents.\n"
        + "- Respond naturally and engagingly but professionally."
    )


    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content

def run_chatbot_loop(collection_name: str, qdrant_client, openai_client):
    print("Welcome to MovieBot! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("MovieBot: Goodbye! Enjoy your movies 🎬")
            break

        intent = detect_intent(openai_client, user_input)

        if intent == "movie_recommendation":
            results = multi_stage_search(collection_name, qdrant_client, user_input, limit=10)
            payload_str = "\n".join(get_payloads(results)) if results else ""
        else:
            payload_str = ""

        reply = chat_with_openai(user_input, payload_str, openai_client)
        
        print("\nMovieBot:\n")
        print(reply)
        print("\n---\n")
