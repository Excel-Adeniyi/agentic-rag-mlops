import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import csv
import json
from application.evaluation_core import (
    build_results_dataset,
    load_results,
    run_ragas_evaluation,
)
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

PER_QUERY_FIELDS = ["pipeline", "index", "query", "faithfulness", "answer_relevancy", "context_precision"]


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
    return results, scores


def per_query_rows(results, scores, pipeline_name):
    df = scores.to_pandas()
    return [
        {
            "pipeline": pipeline_name,
            "index": i,
            "query": results[i]["query"],
            "faithfulness": row["faithfulness"],
            "answer_relevancy": row["answer_relevancy"],
            "context_precision": row["context_precision"],
        }
        for i, row in df.iterrows()
    ]


if __name__ == "__main__":
    baseline_results, baseline_scores = score_pipeline("results_baseline.json", "Baseline RAG")
    agentic_results, agentic_scores = score_pipeline("results_agentic.json", "Agentic RAG")

    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    print(f"Baseline: {baseline_scores}")
    print(f"Agentic:  {agentic_scores}")

    rows = per_query_rows(baseline_results, baseline_scores, "baseline") + \
        per_query_rows(agentic_results, agentic_scores, "agentic")

    csv_path = "ragas_per_query_scores.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=PER_QUERY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nPer-query scores written to {csv_path}")
