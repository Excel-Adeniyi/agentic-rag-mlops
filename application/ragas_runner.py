import json
<<<<<<< HEAD
import sys

=======
import os
import sys

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

>>>>>>> 2329503a4c29ad16dde5dee9d7ee1ce029dfaab5
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
