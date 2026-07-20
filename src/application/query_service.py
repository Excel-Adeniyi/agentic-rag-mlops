from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
import time


@dataclass
class EvaluationResult:
    faithfulness: float
    answer_relevancy: float
    context_precision: float


@dataclass
class PipelineResult:
    answer: str
    response_time: float
    evaluation: EvaluationResult | None = None
    evaluation_error: str | None = None


class RagasEvaluationService:
    """Run Ragas out-of-process so Streamlit's event loop is untouched."""

    def __init__(self):
        self.runner_path = Path(__file__).with_name("ragas_runner.py")
        if not self.runner_path.exists():
            raise FileNotFoundError(f"Missing evaluator runner: {self.runner_path}")
        self.project_root = self.runner_path.parent.parent

    def score(self, query, answer, contexts):
        payload = {
            "query": query,
            "answer": answer,
            "contexts": contexts,
        }

        result = subprocess.run(
            [sys.executable, "-m", "application.ragas_runner"],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=360,
            check=False,
            cwd=str(self.project_root),
        )

        if result.returncode != 0:
            stderr = result.stderr.strip() or "Unknown evaluation error."
            raise RuntimeError(stderr)

        scores = json.loads(result.stdout)
        return EvaluationResult(
            faithfulness=float(scores["faithfulness"]),
            answer_relevancy=float(scores["answer_relevancy"]),
            context_precision=float(scores["context_precision"]),
        )


class AppService:
    """Application-facing orchestration for query execution and evaluation."""

    def __init__(self, evaluator=None):
        self.evaluator = evaluator
        self.evaluator_error = None

    def run_query(self, mode, query, run_eval=False):
        if mode == "Compare Both":
            baseline = self._run_pipeline("Baseline RAG", query, run_eval)
            agentic = self._run_pipeline("Agentic RAG", query, run_eval)
            return {
                "mode": mode,
                "baseline": baseline,
                "agentic": agentic,
            }

        return {
            "mode": mode,
            "result": self._run_pipeline(mode, query, run_eval),
        }

    def _run_pipeline(self, mode, query, run_eval):
        pipeline_fn = self._get_pipeline(mode)
        start = time.time()
        answer, context = pipeline_fn(query)
        response_time = time.time() - start
        result = PipelineResult(answer=answer, response_time=response_time)

        if not run_eval:
            return result

        evaluator = self._get_evaluator()
        if evaluator is None:
            result.evaluation_error = self.evaluator_error or "Evaluation is unavailable."
            return result

        try:
            result.evaluation = evaluator.score(query, answer, context)
        except Exception as exc:
            result.evaluation_error = f"Evaluation failed: {exc}"

        return result

    def _get_pipeline(self, mode):
        if mode == "Agentic RAG":
            from pipeline.pipeline_agentic import agentic_rag

            return agentic_rag

        if mode == "Baseline RAG":
            from pipeline.pipeline_baseline import baseline_rag

            return baseline_rag

        raise ValueError(f"Unsupported mode: {mode}")

    def _get_evaluator(self):
        if self.evaluator is not None:
            return self.evaluator

        if self.evaluator_error is not None:
            return None

        try:
            self.evaluator = RagasEvaluationService()
        except Exception as exc: 
            message = str(exc)
            if "Can't patch loop of type" in message and "uvloop" in message:
                self.evaluator_error = (
                    "Ragas evaluation is unavailable in the Streamlit UI because "
                    "Ragas tries to patch Streamlit's uvloop event loop."
                )
            else:
                self.evaluator_error = message
            return None

        return self.evaluator


def build_default_app_service():
    return AppService()
