from typing import List, Dict
from scenematch.search import multi_stage_search
from qdrant_client import QdrantClient
from .evaluation_metrics import precision_at_k, recall_at_k, reciprocal_rank
from .ground_truth import ground_truth  # This is your function returning Dict[str, List[str]]


def evaluate_query(
    collection_name: str,
    client: QdrantClient,
    query: str,
    relevant_ids: List[str],
    k: int = 10
) -> Dict:
    """
    Evaluate a single query against ground truth.

    Args:
        collection_name (str): Qdrant collection name.
        client (QdrantClient): Qdrant client instance.
        query (str): User search query.
        relevant_ids (List[str]): Ground truth relevant document IDs.
        k (int): Cutoff rank for precision and recall.

    Returns:
        dict: Evaluation metrics for the query.
    """
    # Run the search to get predicted results
    results = multi_stage_search(collection_name=collection_name, client=client, query=query, limit=k)
    predicted_ids = [point.id for point in results]

    # Calculate metrics
    precision = precision_at_k(predicted_ids, relevant_ids, k)
    recall = recall_at_k(predicted_ids, relevant_ids, k)
    rr = reciprocal_rank(predicted_ids, relevant_ids)

    return {
        "query": query,
        "precision_at_k": precision,
        "recall_at_k": recall,
        "reciprocal_rank": rr,
    }


if __name__ == "__main__":
    client = QdrantClient(url="http://localhost:6333")  # your Qdrant client config
    collection_name = "movie-rag-test"

    gt_dict = ground_truth()  # Now returns Dict[str, List[str]]

    for query, relevant_ids in gt_dict.items():
        eval_results = evaluate_query(collection_name, client, query, relevant_ids, k=10)
        print(f"\nEvaluation for query: '{query}'")
        print(f"Precision@10      : {eval_results['precision_at_k']:.3f}")
        print(f"Recall@10         : {eval_results['recall_at_k']:.3f}")
        print(f"Reciprocal Rank   : {eval_results['reciprocal_rank']:.3f}")
        print("-" * 50)
