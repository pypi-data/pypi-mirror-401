"""
Evaluation module for assessing retrieval quality.

Provides the BinaryEvaluator for comparing retrieved chunks against expected answers.
Simple, reproducible, no LLM cost.
"""

from embedding_eval.evaluation.evaluators import (
    BaseEvaluator,
    BinaryEvaluator,
    get_evaluator,
)

__all__ = [
    "BaseEvaluator",
    "BinaryEvaluator",
    "get_evaluator",
]
