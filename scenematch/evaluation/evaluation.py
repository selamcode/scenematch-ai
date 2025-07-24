# evaluation.py
import json
from scenematch.evaluation.metrics import calculate_all_metrics

def load_llm_judgments(json_path="llm_judgments_map.json"):
    """Load LLM judgments from JSON file"""
    with open(json_path, 'r') as f:
        return json.load(f)

def evaluate_llm_judgments():
    """Calculate metrics from LLM judgments"""
    
    # Load judgments
    judgments_data = load_llm_judgments()
    
    all_metrics = []
    
    print("🤖 LLM-as-a-Judge Evaluation Results")
    print("=" * 50)
    
    # Process each query
    for query_key, query_data in judgments_data.items():
        judgments = query_data["judgments"]
        
        # Convert judgments to ranked/relevant format
        ranked_list = list(range(len(judgments)))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        relevant_set = {i for i, judgment in enumerate(judgments) if judgment == 1}
        
        # Calculate metrics
        metrics = calculate_all_metrics(ranked_list, relevant_set, k=10)
        all_metrics.append(metrics)
        
        # Show individual results
        print(f"{query_key}: P@10={metrics['precision_at_k']:.3f}, "
              f"Recall={metrics['recall']:.3f}, "
              f"MRR={metrics['mrr']:.3f}, "
              f"HR@10={metrics['hit_rate_k']:.3f}")
    
    # Calculate averages
    avg_precision = sum(m['precision_at_k'] for m in all_metrics) / len(all_metrics)
    avg_recall = sum(m['recall'] for m in all_metrics) / len(all_metrics)
    avg_mrr = sum(m['mrr'] for m in all_metrics) / len(all_metrics)
    avg_hit_rate = sum(m['hit_rate_k'] for m in all_metrics) / len(all_metrics)
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    print(f"Average Precision@10: {avg_precision:.3f}")
    print(f"Average Recall:       {avg_recall:.3f}")
    print(f"Average MRR:          {avg_mrr:.3f}")
    print(f"Average Hit Rate@10:  {avg_hit_rate:.3f}")
    
    return all_metrics

if __name__ == "__main__":
    evaluate_llm_judgments()
