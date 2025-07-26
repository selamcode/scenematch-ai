"""
evaluation Metrics provided
---------------------------
precision_at_k   – quality of the top k results
recall           – coverage of all relevant items
reciprocal_rank  – rank position of the first relevant item
hit_rate_k       – 1 ⇢ hit present in top-k, else 0
"""

from typing import List, Set, Dict

def precision_at_k(ranked: List[str], relevant: Set[str], k: int) -> float:
    if k == 0:
        return 0.0
    hits = sum(1 for doc_id in ranked[:k] if doc_id in relevant)
    return hits / k

def recall(ranked: List[str], relevant: Set[str]) -> float:
    if not relevant:
        return 0.0
    found = sum(1 for doc_id in ranked if doc_id in relevant)
    return found / len(relevant)

def reciprocal_rank(ranked: List[str], relevant: Set[str]) -> float:
    for pos, doc_id in enumerate(ranked, 1):
        if doc_id in relevant:
            return 1.0 / pos
    return 0.0

def hit_rate_k(ranked: List[str], relevant: Set[str], k: int) -> float:
    return 1.0 if any(doc_id in relevant for doc_id in ranked[:k]) else 0.0

def calculate_all_metrics(ranked: List[str], relevant: Set[str], k: int = 10) -> Dict[str, float]:
    
    """Calculate all metrics at once"""
    return {
        'precision_at_k': precision_at_k(ranked, relevant, k),
        'recall': recall(ranked, relevant),
        'mrr': reciprocal_rank(ranked, relevant),
        'hit_rate_k': hit_rate_k(ranked, relevant, k)
    }
