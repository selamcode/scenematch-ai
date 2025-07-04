from prompt import build_prompt
from util import get_payloads
from qdrant_client.models import ScoredPoint
from search import multi_stage_search 
from client_setup import create_qdrant_local_client, create_openai_client

def chat_with_openai(user_input: str, qdrant_results: list[ScoredPoint], openai_client) -> str:
    
    # Convert Qdrant results to payload string for prompt
    payload_lines = get_payloads(qdrant_results)
    payload_str = "\n".join(payload_lines)

    # Build system prompt with user input and payload string
    system_prompt = build_prompt(user_input, payload_str)

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

        results = multi_stage_search(collection_name, qdrant_client, user_input, limit=10)
        if not results:
            print("MovieBot: Sorry, I couldn't find any movies matching your request. Try again.")
            continue

        reply = chat_with_openai(user_input, results, openai_client)
        print("\nMovieBot recommendations:\n")
        print(reply)
        print("\n---\n")
        
def chat_with_user(user_input: str, collection_name: str, qdrant_client, openai_client) -> str:
    if user_input.lower() in {"exit", "quit", "q"}:
        return "Goodbye! Enjoy your movies 🎬"

    results = multi_stage_search(collection_name, qdrant_client, user_input, limit=10)

    if not results:
        return "Sorry, I couldn't find any movies matching your request. Try again."

    reply = chat_with_openai(user_input, results, openai_client)
    return reply
