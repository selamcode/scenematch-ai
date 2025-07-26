from scenematch.rag.prompt import build_prompt
from qdrant_client.models import ScoredPoint
from scenematch.rag.search import multi_stage_search 
from scenematch.clients.client_setup import create_qdrant_local_client, create_openai_client

# Detecect the intention of the user chat
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

# Main chat
def chat_with_openai(user_input: str, results: list[ScoredPoint], openai_client) -> str:
    system_prompt = (
        build_prompt(user_input, results)  # All prompting logic is now here!
        + "\nInstructions for the assistant:\n"
        + "- Make small talks very short and polite\n"  # Fixed typo
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

# Make the chat continuous 
def run_chatbot_loop(collection_name: str, qdrant_client, openai_client):
    print("Welcome to MovieBot! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("MovieBot: Goodbye! Enjoy your movies 🎬")
            break

        intent = detect_intent(openai_client, user_input)

        if intent == "movie_recommendation":
            # Get search results directly
            results = multi_stage_search(collection_name, qdrant_client, user_input, limit=10)
        else:
            results = []  # Empty list for general chat

        reply = chat_with_openai(user_input, results, openai_client)
        
        print("\nMovieBot:\n")
        print(reply)
        print("\n---\n")
if __name__ == "__main__":
    # Simple test setup
    collection_name = "movies-rag-main"
    qdrant_client = create_qdrant_local_client()
    openai_client = create_openai_client()
    
    print("=== TESTING AGENTIC CHAT ===\n")
    
    # Test with one simple query
    test_query = "recommend me a good action movie"
    print(f"Test Query: '{test_query}'\n")
    
    # Test intent detection
    intent = detect_intent(openai_client, test_query)
    print(f"Detected Intent: {intent}\n")
    
    # Get results based on intent
    if intent == "movie_recommendation":
        results = multi_stage_search(collection_name, qdrant_client, test_query, limit=3)
        print(f"Found {len(results)} movies\n")
    else:
        results = []
        print("No search performed (general chat)\n")
    
    # Generate the full prompt that will be sent to OpenAI
    full_prompt = build_prompt(test_query, results)
    
    print("=== PROMPT SENT TO LLM ===")
    print(full_prompt)
    print("\n" + "="*50)
    
    # Get the actual response
    reply = chat_with_openai(test_query, results, openai_client)
    print(f"\n=== LLM RESPONSE ===")
    print(reply)
