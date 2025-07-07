import dlt

COLLECTION_NAME = "movie-rag-test"


@dlt.source
def source():
    # step 1: prepare the data which I already did in data_cleaning
    yield

@dlt.resource
def emebed_and_store():
    # embed and store them in a qdrantDB
    yield
    
    
@dlt.pipeline(name = "movie_pipline_test")
def pipeline():
   pass
    