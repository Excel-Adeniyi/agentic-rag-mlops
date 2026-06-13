# evaluate.py
# Scores pipeline results using Ragas with local Qwen model via Ollama

import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

# Configure local LLM and embeddings using Ollama
llm = LangchainLLMWrapper(Ollama(model="qwen2.5",     
                                 timeout=300,        # 5 minutes per request
    num_ctx=4096        # context window size
))
embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="qwen2.5"))

def load_results(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def prepare_dataset(results):
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }
    for item in results:
        data["question"].append(item["query"])
        data["answer"].append(item["answer"])
        data["contexts"].append([item.get("context", item["answer"])])
        data["ground_truth"].append(item["ground_truth"])
    return Dataset.from_dict(data)

def score_pipeline(results_file, pipeline_name):
    print(f"\n{'='*60}")
    print(f"Evaluating {pipeline_name} pipeline")
    print(f"{'='*60}")

    results = load_results(results_file)
    print(f"Loaded {len(results)} results")

    dataset = prepare_dataset(results)

    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
        llm=llm,
        embeddings=embeddings
    )

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