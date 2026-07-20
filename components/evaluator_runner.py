# components/evaluator_runner.py
# Runs a pipeline function against a query set and collects results

import time

def run_evaluation(pipeline_fn, pipeline_name, queries):
    """
    Run all queries through a pipeline and collect results.
    
    Args:
        pipeline_fn: the pipeline function to run (baseline_rag or agentic_rag)
        pipeline_name: string label for the pipeline
        queries: list of dicts with 'query' and 'ground_truth' keys
    
    Returns:
        list of result dicts with query, ground_truth, answer and pipeline fields
    """
    results = []
    total = len(queries)

    print(f"\n{'='*60}")
    print(f"Running {pipeline_name} pipeline ({total} queries)")
    print(f"{'='*60}\n")

    for i, item in enumerate(queries, 1):
        print(f"Query {i}/{total}: {item['query'][:50]}...")
        
        try:
            answer, context = pipeline_fn(item['query'])
            results.append({
                "query": item['query'],
                "ground_truth": item['ground_truth'],
                "answer": answer,
                "context": list(context),
                "pipeline": pipeline_name
            })
        except Exception as e:
            print(f"  Error on query {i}: {e}")
            results.append({
                "query": item['query'],
                "ground_truth": item['ground_truth'],
                "answer": f"ERROR: {str(e)}",
                "context": [],
                "pipeline": pipeline_name
            })

        time.sleep(1)

    return results