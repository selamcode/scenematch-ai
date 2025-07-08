from typing import List

def precision_at_k(pred: List[str], gt: List[str], k: int) -> float:
    """
    Calculate precision at cutoff k.

    Args:
        pred (List[str]): List of predicted item IDs in ranked order.
        gt (List[str]): List of ground truth relevant item IDs.
        k (int): Cutoff rank to consider for evaluation.

    Returns:
        float: Precision at k, the fraction of top-k predictions that are relevant.
    """
    pred_k = pred[:k]  # Top-k predicted items
    hits = 0           # Counter for relevant items found in top-k

    for p in pred_k:
        if p in gt:
            hits += 1

    return hits / k


def recall_at_k(pred: List[str], gt: List[str], k: int) -> float:
    """
    Calculate recall at cutoff k.

    Args:
        pred (List[str]): List of predicted item IDs in ranked order.
        gt (List[str]): List of ground truth relevant item IDs.
        k (int): Cutoff rank to consider for evaluation.

    Returns:
        float: Recall at k, the fraction of all relevant items retrieved in top-k predictions.
    """
    pred_k = pred[:k]  # Top-k predicted items
    hits = 0           # Counter for relevant items found in top-k

    for p in pred_k:
        if p in gt:
            hits += 1

    return hits / len(gt) if gt else 0.0


def reciprocal_rank(pred: List[str], gt: List[str]) -> float:
    """
    Calculate reciprocal rank of the first relevant item.

    Args:
        pred (List[str]): List of predicted item IDs in ranked order.
        gt (List[str]): List of ground truth relevant item IDs.

    Returns:
        float: Reciprocal rank, 1 divided by rank position of the first relevant item; 0 if none found.
    """
    for idx in range(len(pred)):
        if pred[idx] in gt:
            return 1 / (idx + 1)

    return 0.0
