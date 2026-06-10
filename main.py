import json
from question_pool import ALL_QUERIES
from pipeline_baseline import baseline_rag
from pipeline_agentic import agentic_rag
from components.evaluator_runner import run_evaluation

if __name__ == "__main__":
    print(f"Starting evaluation. Total queries: {len(ALL_QUERIES)}")

    baseline_results = run_evaluation(baseline_rag, "baseline", ALL_QUERIES)
    with open("results_baseline.json", "w") as f:
        json.dump(baseline_results, f, indent=2)

    agentic_results = run_evaluation(agentic_rag, "agentic", ALL_QUERIES)
    with open("results_agentic.json", "w") as f:
        json.dump(agentic_results, f, indent=2)

    print(f"\nDone. Results saved to results_baseline.json and results_agentic.json")