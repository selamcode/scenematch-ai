import dlt
from prepare_data import get_clean_movie_data
from collection_config import create_my_collection
from embedding import prepare_points, upsert_points
from client_setup import create_qdrant_local_client
import json
import os
from dotenv import load_dotenv

load_dotenv()
filepath = os.getenv("DATASET_JSON_TEST_PATH")

COLLECTION_NAME = "movie-rag-test"
EMBEDDING_DIM = 512

# Resource that consumes raw data, does embedding + upsert, yields rows for DLT
@dlt.resource
def embed_and_store(data):
    print("Starting embed_and_store resource...")
    client = create_qdrant_local_client()
    print("Qdrant client created.")
    
    create_my_collection(client, COLLECTION_NAME, EMBEDDING_DIM)
    print(f"Collection '{COLLECTION_NAME}' checked/created.")
    
    batch = list(data)
    print(f"Loaded batch of {len(batch)} records.")
    
    if not batch:
        print("No data to process, exiting resource.")
        return
    
    print("Preparing points for embedding...")
    points = prepare_points(batch)
    print(f"Prepared {len(points)} points for upsert.")
    
    print("Upserting points into Qdrant...")
    upsert_points(client, COLLECTION_NAME, points)
    print("Upsert complete.")
    
    for idx, row in enumerate(batch):
        if idx % 1000 == 0:
            print(f"Yielding row {idx+1} / {len(batch)}")
        yield row
    
    print("embed_and_store resource done.")

"""
# for procuction 
# Source that yields the embed_and_store resource with raw data
@dlt.source
def movie_source():
    print("Starting movie_source...")
    records = get_clean_movie_data(as_json=True)
    print(f"Got {len(records)} raw records.")
    
    # Yield the resource generator passing the records generator
    yield embed_and_store(iter(records))
    print("movie_source done yielding embed_and_store.")
"""

# Source that yields the embed_and_store resource with raw data from cleaned JSON file
@dlt.source
def movie_source():
    print("Starting movie_source...")
    with open(filepath, "r") as f:
        records = json.load(f)
    print(f"Loaded {len(records)} records from JSON file.")
    
    # Yield the resource generator passing the records generator
    yield embed_and_store(iter(records))
    print("movie_source done yielding embed_and_store.")



if __name__ == "__main__":
    print("Creating pipeline...")
    pipeline = dlt.pipeline(
        pipeline_name="movie_pipeline_test",
        dataset_name="movie_dataset_test",
        destination="duckdb"
    )
    
    print("Running pipeline...")
    load_info = pipeline.run(movie_source())
    print("Pipeline run complete.")
    print(pipeline.last_trace)


