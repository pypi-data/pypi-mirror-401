"""
AIVibe - AI Agent Training Package for VibeKaro.ai

Complete knowledge modules for training AI agents with production-grade
Flutter, Dart, Kotlin, Python, JavaScript, AWS, and cloud expertise.

Version: 1.0.1
Author: AICippy Technologies
License: MIT
"""

from aivibe.trainer import AIVibeTrainer
from aivibe.evaluator import AIVibeEvaluator
from aivibe.scheduler import TrainingScheduler
from aivibe.models import TrainingResult, EvaluationResult, Scorecard
from aivibe.knowledge import KnowledgeBase

__version__ = "1.0.1"
__author__ = "AICippy Technologies"
__email__ = "dev@vibekaro.ai"

__all__ = [
    "AIVibeTrainer",
    "AIVibeEvaluator",
    "TrainingScheduler",
    "TrainingResult",
    "EvaluationResult",
    "Scorecard",
    "KnowledgeBase",
    "__version__",
]


def get_version() -> str:
    """Get the current AIVibe package version."""
    return __version__


def quick_train(agent_name: str = "aikutty") -> TrainingResult:
    """Quick training function for immediate use."""
    trainer = AIVibeTrainer()
    return trainer.train_agent(agent_name)


def quick_evaluate(agent_name: str = "aikutty") -> EvaluationResult:
    """Quick evaluation function for immediate use."""
    evaluator = AIVibeEvaluator()
    return evaluator.evaluate(agent_name)
