import json
from application.evaluation_core import (
    build_results_dataset,
    load_results,
    run_ragas_evaluation,
)
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"


def score_pipeline(results_file, pipeline_name):
    print(f"\n{'='*60}")
    print(f"Evaluating {pipeline_name} pipeline")
    print(f"{'='*60}")

    results = load_results(results_file)
    print(f"Loaded {len(results)} results")

    dataset = build_results_dataset(results)
    scores = run_ragas_evaluation(dataset)

    print(f"\n{pipeline_name} Scores:")
    print(scores)
    return scores

if __name__ == "__main__":
    baseline_scores = score_pipeline("results_baseline.json", "Baseline RAG")
    agentic_scores = score_pipeline("results_agentic.json", "Agentic RAG")

    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    print(f"Baseline: {baseline_scores}")
    print(f"Agentic:  {agentic_scores}")
