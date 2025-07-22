"""
Runs the retrieval evaluation metrics defined in retrieval_evaluation_methods.py
"""

import json
from collections import defaultdict
from typing import Dict, List

import scenematch.evaluation.retrieval_evaluation_methods as rem


def eval_retrieval(gt_path: str,
                   res_path: str,
                   k: int = 5) -> Dict[str, float]:
    ground = json.load(open(gt_path, encoding="utf-8"))
    retrieved = json.load(open(res_path, encoding="utf-8"))

    bucket: Dict[str, List[float]] = defaultdict(list)

    for scenario in ground:
        relevant_set = set(ground[scenario])

        if scenario not in retrieved:
            continue

        ranked_lists = retrieved[scenario]
        for ranked in ranked_lists:
            bucket["precision@k"].append(rem.precision_at_k(ranked, relevant_set, k))
            bucket["recall"].append(rem.recall(ranked, relevant_set))
            bucket["mrr"].append(rem.reciprocal_rank(ranked, relevant_set))
            bucket["hit@k"].append(rem.hit_rate_k(ranked, relevant_set, k))

    results: Dict[str, float] = {}
    for metric in bucket:
        values = bucket[metric]
        results[metric] = sum(values) / float(len(values)) if values else 0.0

    return results


if __name__ == "__main__":
   
    SCORES = eval_retrieval(
        "/Users/selamsew/Documents/llm-zoomcamp-final-project/ground_truth_ids.json",
        "/Users/selamsew/Documents/llm-zoomcamp-final-project/retrieval_results.json",
        k=50
    )

    print("\n=== RETRIEVAL METRICS (macro-average) ===")
    for metric in sorted(SCORES):
        print(f"{metric:12}: {SCORES[metric]:.4f}")
