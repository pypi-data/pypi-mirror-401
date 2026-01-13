"""
AIVibe Data Models

Pydantic models for training results, evaluations, and scorecards.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TrainingModule(BaseModel):
    """Individual training module result."""

    name: str
    score: float = Field(ge=0, le=100)
    topics_covered: int
    time_seconds: float
    passed: bool
    details: dict = Field(default_factory=dict)


class TrainingResult(BaseModel):
    """Complete training session result."""

    agent: str
    score: float = Field(ge=0, le=100)
    modules_trained: list[str]
    module_results: list[TrainingModule] = Field(default_factory=list)
    duration_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    success: bool = True
    error_message: Optional[str] = None
    details: dict = Field(default_factory=dict)

    def to_log_entry(self) -> dict:
        """Convert to log entry format."""
        return {
            "agent": self.agent,
            "score": self.score,
            "modules": self.modules_trained,
            "duration": self.duration_seconds,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
        }


class EvaluationCategory(BaseModel):
    """Evaluation category with score breakdown."""

    name: str
    weight: float = Field(ge=0, le=1)
    score: float = Field(ge=0, le=100)
    weighted_score: float = Field(ge=0, le=100)
    criteria: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    """Complete evaluation result."""

    agent: str
    overall_score: float = Field(ge=0, le=100)
    categories: list[EvaluationCategory]
    passed: bool
    min_passing_score: float = 85.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    recommendations: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    @property
    def grade(self) -> str:
        """Get letter grade based on score."""
        if self.overall_score >= 95:
            return "A+"
        elif self.overall_score >= 90:
            return "A"
        elif self.overall_score >= 85:
            return "B+"
        elif self.overall_score >= 80:
            return "B"
        elif self.overall_score >= 75:
            return "C+"
        elif self.overall_score >= 70:
            return "C"
        else:
            return "F"


class ScorecardEntry(BaseModel):
    """Single scorecard entry."""

    date: datetime
    score: float
    modules: list[str]
    duration_seconds: float
    passed: bool


class Scorecard(BaseModel):
    """Agent training scorecard with history."""

    agent: str
    total_trainings: int = 0
    average_score: float = 0.0
    best_score: float = 0.0
    worst_score: float = 100.0
    current_streak: int = 0
    best_streak: int = 0
    last_training: Optional[datetime] = None
    history: list[ScorecardEntry] = Field(default_factory=list)

    def add_result(self, result: TrainingResult) -> None:
        """Add a training result to the scorecard."""
        entry = ScorecardEntry(
            date=result.timestamp,
            score=result.score,
            modules=result.modules_trained,
            duration_seconds=result.duration_seconds,
            passed=result.score >= 85.0,
        )
        self.history.append(entry)
        self.total_trainings += 1

        # Update statistics
        scores = [e.score for e in self.history]
        self.average_score = sum(scores) / len(scores)
        self.best_score = max(scores)
        self.worst_score = min(scores)
        self.last_training = result.timestamp

        # Update streak
        if entry.passed:
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0

    def get_trend(self, last_n: int = 7) -> str:
        """Get score trend over last N trainings."""
        if len(self.history) < 2:
            return "stable"

        recent = self.history[-last_n:]
        if len(recent) < 2:
            return "stable"

        first_half = sum(e.score for e in recent[:len(recent)//2]) / (len(recent)//2)
        second_half = sum(e.score for e in recent[len(recent)//2:]) / (len(recent) - len(recent)//2)

        diff = second_half - first_half
        if diff > 2:
            return "improving"
        elif diff < -2:
            return "declining"
        return "stable"


class AgentConfig(BaseModel):
    """Agent configuration."""

    name: str
    type: str  # "aikutty" or "aivedha"
    enabled_modules: list[str]
    training_schedule: Optional[str] = None
    min_score_threshold: float = 85.0
    s3_memory_key: Optional[str] = None
    dynamodb_table: Optional[str] = None


class TrainingConfig(BaseModel):
    """Training configuration."""

    agent: AgentConfig
    schedule_enabled: bool = True
    schedule_time: str = "02:00"
    schedule_timezone: str = "UTC"
    report_path: str = "./reports/"
    log_path: str = "./logs/"
    max_history: int = 365
    notify_on_failure: bool = True
    notification_email: Optional[str] = None
