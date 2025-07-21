"""
retrieval_evaluation_methods.py
---------------------------------------------------------------
retrieval metrics
-----------------
Metrics provided
-----------------
precision_at_k   – quality of the first *k* results
recall           – coverage of all relevant items
reciprocal_rank  – rank position of the first relevant item
hit_rate_k       – 1 ⇢ hit present in top-k, else 0
"""
from typing import List, Set


def precision_at_k(ranked: List[str], relevant: Set[str], k: int) -> float:
    """
    Precision@k: fraction of the first *k* retrieved IDs that are relevant.

    Parameters
    ----------
    ranked   : full ranked list of document IDs returned for one query
    relevant : set with all ground-truth IDs for the query
    k        : evaluate the first *k* positions in *ranked*

    Returns
    -------
    float in [0, 1].  If *k* == 0 the function returns 0.0 by definition.
    """
    hits = 0
    top_k = ranked[:k]
    for doc_id in top_k:
        if doc_id in relevant:
            hits += 1
    if k == 0:
        return 0.0
    return hits / float(k)


def recall(ranked: List[str], relevant: Set[str]) -> float:
    """
    Recall: fraction of all relevant IDs that were retrieved (any rank).

    Parameters
    ----------
    ranked   : full ranked list of document IDs
    relevant : set with all ground-truth IDs

    Returns
    -------
    float in [0, 1].  If *relevant* is empty the function returns 0.0.
    """
    if not relevant:
        return 0.0

    found = 0
    for doc_id in ranked:
        if doc_id in relevant:
            found += 1
    return found / float(len(relevant))


def reciprocal_rank(ranked: List[str], relevant: Set[str]) -> float:
    """
    Reciprocal Rank (RR): 1 / rank of the first relevant ID.

    Parameters
    ----------
    ranked   : full ranked list of document IDs
    relevant : set with ground-truth IDs

    Returns
    -------
    float in (0, 1].  If no relevant ID is found, returns 0.0.
    """
    pos = 1
    for doc_id in ranked:
        if doc_id in relevant:
            return 1.0 / pos
        pos += 1
    return 0.0


def hit_rate_k(ranked: List[str], relevant: Set[str], k: int) -> float:
    """
    Hit-Rate@k: indicator that at least one relevant ID appears in top-k.

    Parameters
    ----------
    ranked   : full ranked list of document IDs
    relevant : set with ground-truth IDs
    k        : look only at the first *k* positions

    Returns
    -------
    1.0 if any relevant document is found in the first *k* slots, else 0.0
    """
    top_k = ranked[:k]
    for doc_id in top_k:
        if doc_id in relevant:
            return 1.0
    return 0.0
