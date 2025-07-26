import os
from dotenv import load_dotenv
from scenematch.clients.client_setup import create_qdrant_local_client, create_openai_client
from scenematch.rag.collection_config import create_my_collection # for testing your own
from scenematch.rag.embedding import embed # for testing your own 
from scenematch.rag.search import multi_stage_search # if you want to test the retrieval 
from scenematch.rag.agentic_chat import run_chatbot_loop

def main():
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    
    """You can uncomment this to create your own collection and embedding"""
    
    '''
    load_dotenv()
    
    # raw movies json file
    filepath = os.getenv("DATASET_JSON_PATH")
    
    # choose vector dimention
    emebedding_dim = 512
    # index 
    collection_name = "movies-rag-main"
    
    # create collection and embed movie data
    create_my_collection(movie_client_test, collection_name, emebedding_dim)
    embed(collection_name,filepath, movie_client_test)
    
    '''
    
    # Create qdrant and openai client 
    movie_client_test = create_qdrant_local_client()
    openai_client = create_openai_client()
    
    # Using exiting collection name 
    collection_name = "movies-rag-main"
    
    # Run the chatbot for movie recomendation
    run_chatbot_loop(collection_name, movie_client_test, openai_client)

if __name__ == "__main__":
    main()


