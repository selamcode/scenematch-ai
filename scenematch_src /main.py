import os
from dotenv import load_dotenv
import qdrant_client_setup 
from collection_config import create_my_collection
from embedding import embed
from search import multi_stage_search


def main():
    
    load_dotenv()
    filepath = os.getenv("DATASET_JSON_TEST_PATH")
    # create 
    movie_client_test = qdrant_client_setup.create_qdrant_local_client()
    collection_name = "movie-rag-test"
    emebedding_dim = 512

    create_my_collection(movie_client_test, collection_name, emebedding_dim)
    embed(collection_name,filepath, movie_client_test)

    query = "could you please recommend a romance and action movie"
    print(multi_stage_search(collection_name,movie_client_test,query, 10))
    
    result = multi_stage_search(collection_name,movie_client_test,query, 10)
    
    print("\n Here are your top 10 recomendations \n")
    for point in result:
        print("\n", point.payload["title"])

if __name__ == "__main__":
    main()


