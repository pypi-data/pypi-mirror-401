"""
AIVibe Evaluator Module

Evaluation system for AI agents with scoring and recommendations.
"""

from datetime import datetime
from typing import Optional

from aivibe.knowledge import KnowledgeBase
from aivibe.models import EvaluationCategory, EvaluationResult


class AIVibeEvaluator:
    """
    Evaluates AI agent knowledge and provides recommendations.

    Usage:
        evaluator = AIVibeEvaluator()
        result = evaluator.evaluate("aikutty")
        print(f"Grade: {result.grade}")
    """

    EVALUATION_CATEGORIES = {
        "coding_standards": {
            "weight": 0.25,
            "description": "Coding standards and best practices",
            "criteria": [
                "Naming conventions followed",
                "Code organization patterns",
                "Documentation standards",
                "Error handling patterns",
            ],
        },
        "framework_knowledge": {
            "weight": 0.25,
            "description": "Framework-specific knowledge",
            "criteria": [
                "Flutter widget patterns",
                "State management proficiency",
                "Navigation implementation",
                "Platform integration",
            ],
        },
        "architecture": {
            "weight": 0.20,
            "description": "Architecture and design patterns",
            "criteria": [
                "MVVM/Clean architecture",
                "Dependency injection",
                "Repository pattern",
                "API design",
            ],
        },
        "cloud_services": {
            "weight": 0.15,
            "description": "Cloud service integration",
            "criteria": [
                "AWS service usage",
                "Firebase integration",
                "Database operations",
                "Authentication flows",
            ],
        },
        "sdlc_process": {
            "weight": 0.15,
            "description": "SDLC process knowledge",
            "criteria": [
                "Phase understanding",
                "Deliverable creation",
                "Quality gate compliance",
                "Role responsibilities",
            ],
        },
    }

    MIN_PASSING_SCORE = 85.0

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        """Initialize evaluator with knowledge base."""
        self.kb = knowledge_base or KnowledgeBase()

    def evaluate(
        self,
        agent: str,
        categories: Optional[list[str]] = None,
    ) -> EvaluationResult:
        """
        Evaluate an AI agent's knowledge.

        Args:
            agent: Agent name ('aikutty' or 'aivedha')
            categories: Optional list of categories to evaluate

        Returns:
            EvaluationResult with scores and recommendations
        """
        agent = agent.lower()
        categories = categories or list(self.EVALUATION_CATEGORIES.keys())

        category_results: list[EvaluationCategory] = []
        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[str] = []

        for cat_name in categories:
            cat_config = self.EVALUATION_CATEGORIES.get(cat_name)
            if not cat_config:
                continue

            # Evaluate category
            score, findings = self._evaluate_category(cat_name, agent)
            weighted_score = score * cat_config["weight"]

            category_results.append(
                EvaluationCategory(
                    name=cat_name,
                    weight=cat_config["weight"],
                    score=score,
                    weighted_score=weighted_score,
                    criteria=cat_config["criteria"],
                    findings=findings,
                )
            )

            # Determine strengths and weaknesses
            if score >= 90:
                strengths.append(f"{cat_name}: {cat_config['description']}")
            elif score < 80:
                weaknesses.append(f"{cat_name}: {cat_config['description']}")
                recommendations.append(self._get_recommendation(cat_name, score))

        # Calculate overall score
        overall_score = sum(cat.weighted_score for cat in category_results) / sum(
            cat.weight for cat in category_results
        ) if category_results else 0.0

        return EvaluationResult(
            agent=agent,
            overall_score=overall_score,
            categories=category_results,
            passed=overall_score >= self.MIN_PASSING_SCORE,
            min_passing_score=self.MIN_PASSING_SCORE,
            recommendations=recommendations,
            strengths=strengths,
            weaknesses=weaknesses,
        )

    def _evaluate_category(
        self, category: str, agent: str
    ) -> tuple[float, list[str]]:
        """Evaluate a specific category."""
        findings: list[str] = []
        base_score = 85.0

        if category == "coding_standards":
            # Check coding standards knowledge
            modules = ["flutter", "dart", "kotlin", "python", "javascript"]
            for module_name in modules:
                module = self.kb.get_module(module_name)
                if module and hasattr(module, "get_coding_standards"):
                    standards = module.get_coding_standards()
                    if standards:
                        base_score += 2
                        findings.append(f"{module_name} coding standards loaded")

        elif category == "framework_knowledge":
            # Check Flutter/Dart knowledge
            flutter = self.kb.flutter
            if flutter:
                if flutter.WIDGET_PATTERNS:
                    base_score += 3
                    findings.append("Widget patterns comprehensive")
                if flutter.STATE_MANAGEMENT:
                    base_score += 3
                    findings.append("State management patterns included")
                if flutter.NAVIGATION:
                    base_score += 2
                    findings.append("Navigation patterns defined")

        elif category == "architecture":
            # Check architecture patterns
            flutter = self.kb.flutter
            kotlin = self.kb.kotlin
            if flutter and flutter.API_PATTERNS:
                base_score += 3
                findings.append("API patterns defined")
            if kotlin and kotlin.ANDROID_ARCHITECTURE:
                base_score += 3
                findings.append("Android architecture patterns included")

        elif category == "cloud_services":
            # Check cloud knowledge
            if self.kb.aws and self.kb.aws.DYNAMODB:
                base_score += 3
                findings.append("AWS DynamoDB patterns included")
            if self.kb.firebase and self.kb.firebase.FIRESTORE:
                base_score += 3
                findings.append("Firebase Firestore patterns included")

        elif category == "sdlc_process":
            # Check SDLC knowledge
            sdlc = self.kb.sdlc
            if sdlc:
                if sdlc.PHASES and len(sdlc.PHASES) >= 10:
                    base_score += 5
                    findings.append("All 10 SDLC phases defined")
                if sdlc.AGENT_ROLES:
                    base_score += 3
                    findings.append("Agent roles defined")
                if sdlc.QUALITY_GATES:
                    base_score += 2
                    findings.append("Quality gates established")

        return min(100.0, base_score), findings

    def _get_recommendation(self, category: str, score: float) -> str:
        """Get recommendation for a category based on score."""
        recommendations = {
            "coding_standards": "Review and reinforce coding standards documentation",
            "framework_knowledge": "Deep dive into Flutter widget and state management patterns",
            "architecture": "Study clean architecture and design patterns",
            "cloud_services": "Practice AWS and Firebase integration patterns",
            "sdlc_process": "Review SDLC phases and deliverable requirements",
        }
        return recommendations.get(category, "Review this category's knowledge content")

    def generate_scorecard(self, result: EvaluationResult) -> str:
        """Generate a text scorecard from evaluation result."""
        lines = [
            "=" * 60,
            f"AIVibe Evaluation Scorecard - {result.agent.upper()}",
            "=" * 60,
            f"Date: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Overall Score: {result.overall_score:.1f}%",
            f"Grade: {result.grade}",
            f"Status: {'PASSED' if result.passed else 'FAILED'}",
            f"Minimum Required: {result.min_passing_score}%",
            "",
            "Category Scores:",
            "-" * 40,
        ]

        for cat in result.categories:
            bar = self._generate_bar(cat.score)
            lines.append(f"  {cat.name:20} {bar} {cat.score:.1f}%")

        if result.strengths:
            lines.extend(["", "Strengths:", "-" * 40])
            for strength in result.strengths:
                lines.append(f"  + {strength}")

        if result.weaknesses:
            lines.extend(["", "Areas for Improvement:", "-" * 40])
            for weakness in result.weaknesses:
                lines.append(f"  - {weakness}")

        if result.recommendations:
            lines.extend(["", "Recommendations:", "-" * 40])
            for i, rec in enumerate(result.recommendations, 1):
                lines.append(f"  {i}. {rec}")

        lines.append("=" * 60)

        return "\n".join(lines)

    def _generate_bar(self, score: float, width: int = 20) -> str:
        """Generate a visual progress bar."""
        filled = int(score / 100 * width)
        empty = width - filled
        return f"[{'#' * filled}{'-' * empty}]"

    def compare_evaluations(
        self, results: list[EvaluationResult]
    ) -> dict:
        """Compare multiple evaluation results."""
        if not results:
            return {}

        return {
            "count": len(results),
            "average_score": sum(r.overall_score for r in results) / len(results),
            "best_score": max(r.overall_score for r in results),
            "worst_score": min(r.overall_score for r in results),
            "pass_rate": sum(1 for r in results if r.passed) / len(results) * 100,
            "trend": self._calculate_trend(results),
        }

    def _calculate_trend(self, results: list[EvaluationResult]) -> str:
        """Calculate score trend."""
        if len(results) < 2:
            return "stable"

        # Compare first half to second half
        mid = len(results) // 2
        first_half_avg = sum(r.overall_score for r in results[:mid]) / mid
        second_half_avg = sum(r.overall_score for r in results[mid:]) / (len(results) - mid)

        diff = second_half_avg - first_half_avg
        if diff > 2:
            return "improving"
        elif diff < -2:
            return "declining"
        return "stable"
