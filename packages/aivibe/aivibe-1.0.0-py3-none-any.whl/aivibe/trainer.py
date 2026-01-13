"""
AIVibe Trainer Module

Automated training system for AI agents with comprehensive
knowledge modules covering Flutter, Dart, and cloud development.
"""

import time
from datetime import datetime
from typing import Optional

from aivibe.knowledge import KnowledgeBase
from aivibe.models import TrainingModule, TrainingResult


class AIVibeTrainer:
    """
    Comprehensive AI agent trainer with knowledge modules.

    Usage:
        trainer = AIVibeTrainer()
        result = trainer.train_agent("aikutty")
        print(f"Score: {result.score}")
    """

    AVAILABLE_AGENTS = ["aikutty", "aivedha"]

    DEFAULT_MODULES = {
        "aikutty": [
            "flutter",
            "dart",
            "kotlin",
            "python",
            "javascript",
            "postgresql",
            "aws",
            "gcloud",
            "firebase",
            "sdlc",
            "troubleshooting",
        ],
        "aivedha": [
            "sdlc",
            "flutter",
            "dart",
            "troubleshooting",
        ],
    }

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        """Initialize trainer with knowledge base."""
        self.kb = knowledge_base or KnowledgeBase()
        self._training_log: list[TrainingResult] = []

    def train_agent(
        self,
        agent: str,
        modules: Optional[list[str]] = None,
        verbose: bool = False,
    ) -> TrainingResult:
        """
        Train an AI agent with specified knowledge modules.

        Args:
            agent: Agent name ('aikutty' or 'aivedha')
            modules: Optional list of modules to train (defaults to agent's default)
            verbose: Print training progress

        Returns:
            TrainingResult with scores and details
        """
        if agent.lower() not in self.AVAILABLE_AGENTS:
            raise ValueError(f"Unknown agent: {agent}. Available: {self.AVAILABLE_AGENTS}")

        agent = agent.lower()
        modules = modules or self.DEFAULT_MODULES.get(agent, [])

        start_time = time.time()
        module_results: list[TrainingModule] = []

        if verbose:
            print(f"\n{'='*60}")
            print(f"  AIVibe Training Session - {agent.upper()}")
            print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")

        for module_name in modules:
            module_start = time.time()

            if verbose:
                print(f"  Training module: {module_name}...", end=" ")

            # Get knowledge module
            knowledge_module = self.kb.get_module(module_name)
            if not knowledge_module:
                if verbose:
                    print("SKIPPED (not found)")
                continue

            # Simulate training by accessing all knowledge
            knowledge_data = knowledge_module.get_all()
            topics_covered = self._count_topics(knowledge_data)

            # Calculate module score based on knowledge coverage
            module_score = self._calculate_module_score(knowledge_data, module_name)

            module_time = time.time() - module_start
            passed = module_score >= 85.0

            module_results.append(
                TrainingModule(
                    name=module_name,
                    score=module_score,
                    topics_covered=topics_covered,
                    time_seconds=module_time,
                    passed=passed,
                    details={"version": knowledge_data.get("version", "1.0")},
                )
            )

            if verbose:
                status = "PASS" if passed else "FAIL"
                print(f"{status} ({module_score:.1f}%, {topics_covered} topics)")

        # Calculate overall score
        total_score = (
            sum(m.score for m in module_results) / len(module_results)
            if module_results
            else 0.0
        )

        duration = time.time() - start_time

        result = TrainingResult(
            agent=agent,
            score=total_score,
            modules_trained=modules,
            module_results=module_results,
            duration_seconds=duration,
            success=total_score >= 85.0,
            details={
                "total_topics": sum(m.topics_covered for m in module_results),
                "passed_modules": sum(1 for m in module_results if m.passed),
                "failed_modules": sum(1 for m in module_results if not m.passed),
            },
        )

        self._training_log.append(result)

        if verbose:
            print(f"\n{'='*60}")
            print(f"  Training Complete!")
            print(f"  Overall Score: {total_score:.1f}%")
            print(f"  Status: {'PASSED' if result.success else 'FAILED'}")
            print(f"  Duration: {duration:.2f}s")
            print(f"{'='*60}\n")

        return result

    def _count_topics(self, data: dict, depth: int = 0) -> int:
        """Count total topics in knowledge data."""
        count = 0
        for key, value in data.items():
            if isinstance(value, dict):
                count += 1 + self._count_topics(value, depth + 1)
            elif isinstance(value, list):
                count += len(value)
            else:
                count += 1
        return count

    def _calculate_module_score(self, knowledge_data: dict, module_name: str) -> float:
        """Calculate score for a knowledge module."""
        base_score = 90.0

        # Check for required sections
        required_sections = {
            "flutter": ["widget_patterns", "state_management", "coding_standards"],
            "dart": ["language_features", "null_safety", "coding_standards"],
            "kotlin": ["coroutines", "jetpack_compose", "coding_standards"],
            "python": ["async_programming", "fastapi", "coding_standards"],
            "javascript": ["react_patterns", "testing", "coding_standards"],
            "postgresql": ["schema_design", "performance", "security"],
            "aws": ["lambda", "dynamodb", "best_practices"],
            "sdlc": ["phases", "agent_roles", "quality_gates"],
        }

        sections = required_sections.get(module_name, [])
        missing = 0
        for section in sections:
            if section not in knowledge_data:
                missing += 1

        # Deduct points for missing sections
        score = base_score - (missing * 5)

        # Bonus for comprehensive content
        topic_count = self._count_topics(knowledge_data)
        if topic_count > 50:
            score += 5
        if topic_count > 100:
            score += 5

        # Check for deprecated patterns section
        if "deprecated" in knowledge_data:
            score += 2

        return min(100.0, max(0.0, score))

    def train_all_agents(self, verbose: bool = False) -> dict[str, TrainingResult]:
        """Train all available agents."""
        results = {}
        for agent in self.AVAILABLE_AGENTS:
            results[agent] = self.train_agent(agent, verbose=verbose)
        return results

    def get_training_history(self) -> list[TrainingResult]:
        """Get training history for this session."""
        return self._training_log.copy()

    def get_last_result(self) -> Optional[TrainingResult]:
        """Get the most recent training result."""
        return self._training_log[-1] if self._training_log else None

    def generate_report(self, result: TrainingResult) -> str:
        """Generate a text report from training result."""
        lines = [
            "=" * 60,
            f"AIVibe Training Report - {result.agent.upper()}",
            "=" * 60,
            f"Date: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Overall Score: {result.score:.1f}%",
            f"Status: {'PASSED' if result.success else 'FAILED'}",
            f"Duration: {result.duration_seconds:.2f}s",
            "",
            "Module Results:",
            "-" * 40,
        ]

        for module in result.module_results:
            status = "PASS" if module.passed else "FAIL"
            lines.append(
                f"  {module.name:20} {module.score:6.1f}%  {status}  "
                f"({module.topics_covered} topics)"
            )

        lines.extend(
            [
                "",
                "Summary:",
                f"  Total Modules: {len(result.module_results)}",
                f"  Passed: {result.details.get('passed_modules', 0)}",
                f"  Failed: {result.details.get('failed_modules', 0)}",
                f"  Total Topics: {result.details.get('total_topics', 0)}",
                "=" * 60,
            ]
        )

        return "\n".join(lines)
