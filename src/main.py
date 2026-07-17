import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import json
from pipeline.question_pool import ALL_QUERIES
from pipeline.pipeline_baseline import baseline_rag
from pipeline.pipeline_agentic import agentic_rag
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