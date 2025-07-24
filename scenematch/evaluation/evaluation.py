import json
import os
from dotenv import load_dotenv
from  scenematch.evaluation.metrics import calculate_all_metrics

# Load .env
load_dotenv()

def load_llm_judgments():
    """Load LLM judgments from EVALUATION_RESULT folder"""
    evaluation_result_dir = os.getenv("EVALUATION_RESULT")
    if not evaluation_result_dir:
        raise ValueError("EVALUATION_RESULT must be set in .env file")
    
    judgments_file = os.path.join(evaluation_result_dir, "llm_judgments_map.json")
    
    with open(judgments_file, 'r') as f:
        return json.load(f)

def evaluate_llm_judgments():
    """Calculate metrics from LLM judgments and save results"""
    
    # Load judgments
    judgments_data = load_llm_judgments()
    
    all_metrics = []
    individual_results = {}
    
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
        individual_results[query_key] = metrics
        
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
    
    # Prepare results
    evaluation_results = {
        "summary": {
            "total_queries": len(all_metrics),
            "average_metrics": {
                "precision_at_10": avg_precision,
                "recall": avg_recall,
                "mrr": avg_mrr,
                "hit_rate_10": avg_hit_rate
            }
        },
        "individual_results": individual_results
    }
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    print(f"Average Precision@10: {avg_precision:.3f}")
    print(f"Average Recall:       {avg_recall:.3f}")
    print(f"Average MRR:          {avg_mrr:.3f}")
    print(f"Average Hit Rate@10:  {avg_hit_rate:.3f}")
    
    # Save results to EVALUATION_RESULT folder
    evaluation_result_dir = os.getenv("EVALUATION_RESULT")
    results_file = os.path.join(evaluation_result_dir, "evaluation_metrics.json")
    
    with open(results_file, "w") as f:
        json.dump(evaluation_results, f, indent=2)
    
    print(f"\n💾 Evaluation results saved to: {results_file}")
    
    return evaluation_results

if __name__ == "__main__":
    evaluate_llm_judgments()
    print("\n✅ Evaluation complete!")
