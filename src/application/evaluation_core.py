import json

from datasets import Dataset
from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import answer_relevancy, context_precision, faithfulness
from ragas.run_config import RunConfig
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_single_query_dataset(query, answer, contexts, ground_truth=""):
    return Dataset.from_dict(
        {
            "question": [query],
            "answer": [answer],
            "contexts": [contexts],
            "ground_truth": [ground_truth],
        }
    )


def build_results_dataset(results):
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": [],
    }

    for item in results:
        data["question"].append(item["query"])
        data["answer"].append(item["answer"])
        data["contexts"].append(item.get("context") or [""])
        data["ground_truth"].append(item["ground_truth"])

    return Dataset.from_dict(data)


def run_ragas_evaluation(dataset):
    llm = LangchainLLMWrapper(
        ChatOllama(
            model="qwen2.5",
            timeout=300,
            num_ctx=8192,
        )
    )
    embeddings = LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    run_config = RunConfig(max_workers=1, timeout=300)

    return evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
        llm=llm,
        embeddings=embeddings,
        run_config=run_config,
        raise_exceptions=False,
    )


def scores_to_dict(scores):
    return {
        "faithfulness": float(scores["faithfulness"]),
        "answer_relevancy": float(scores["answer_relevancy"]),
        "context_precision": float(scores["context_precision"]),
    }


def load_results(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
