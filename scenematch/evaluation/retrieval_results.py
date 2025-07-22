import json

from scenematch.rag.search import multi_stage_search
from scenematch.clients.client_setup import create_qdrant_local_client
import os

def main():
    # Load your ground truth queries
    gt = json.load(open("ground_truth_ids.json", encoding="utf-8"))
    client = create_qdrant_local_client()
    collection_name = os.getenv("COLLECTION_NAME", "movie-rag-test")
    results = {}

    for query in gt.keys():
        points = multi_stage_search(collection_name, client, query, limit=50)
        # Store only the IDs in ranked order
        results[query] = [p.id for p in points]

    with open("retrieval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("retrieval_results.json created with top‑50 per query.")

if __name__ == "__main__":
    main()
