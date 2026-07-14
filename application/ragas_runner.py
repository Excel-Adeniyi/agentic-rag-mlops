import json
import sys

from application.evaluation_core import (
    build_single_query_dataset,
    run_ragas_evaluation,
    scores_to_dict,
)


def main():
    payload = json.load(sys.stdin)

    dataset = build_single_query_dataset(
        query=payload["query"],
        answer=payload["answer"],
        contexts=payload["contexts"],
    )
    scores = run_ragas_evaluation(dataset)
    json.dump(scores_to_dict(scores), sys.stdout)


if __name__ == "__main__":
    main()
