import qdrant_client_setup 
from collection_config import create_my_collection

def main():
# create 
    movie_client_test = qdrant_client_setup.create_qdrant_local_client()
    collection_name = "movie-rag-test"
    emebedding_dim = 512
    create_my_collection(movie_client_test, collection_name, emebedding_dim)

if __name__ == "__main__":
    main()


