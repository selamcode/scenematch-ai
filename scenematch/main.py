import os
from dotenv import load_dotenv
from client_setup import create_qdrant_local_client, create_openai_client
from collection_config import create_my_collection
from embedding import embed
#from search import multi_stage_search
from chat import run_chatbot_loop


def main():
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    
    load_dotenv()
    filepath = os.getenv("DATASET_JSON_TEST_PATH")
    
    # create qdrant and openai client 
    movie_client_test = create_qdrant_local_client()
    openai_client = create_openai_client()
    collection_name = "movie-rag-test"
    emebedding_dim = 512
    
    create_my_collection(movie_client_test, collection_name, emebedding_dim)
    embed(collection_name,filepath, movie_client_test)

    #query = "could you please recommend a romance and action movie"
    #print(multi_stage_search(collection_name,movie_client_test,query, 10))
    '''
    [
    ScoredPoint(id=10, version=12, score=1.0, payload={'title': 'Shutter Island', 'vote_average': 8.2, 'genres': ['thriller', 'mystery']}),
    ScoredPoint(id=16, version=12, score=0.66, payload={'title': 'Avatar', 'vote_average': 7.9, 'genres': ['adventure', 'science fiction']}),
    ...
    ]
    '''

    run_chatbot_loop(collection_name, movie_client_test, openai_client)

     
    
    #print(result[0].payload['title'])
    
    
    
    '''
    print("\n Here are your top 10 recomendations \n")
    for point in result:
        print("\n", point.payload["title"])
    '''

if __name__ == "__main__":
    main()


