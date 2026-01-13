"""
AIVibe Training Scheduler Module

Automated scheduling for AI agent training with daily/weekly schedules.
"""

import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional

from aivibe.evaluator import AIVibeEvaluator
from aivibe.models import Scorecard, TrainingResult
from aivibe.trainer import AIVibeTrainer


class TrainingScheduler:
    """
    Automated training scheduler for AI agents.

    Usage:
        scheduler = TrainingScheduler()
        scheduler.schedule_daily("aikutty", "02:00")
        scheduler.start()
    """

    def __init__(
        self,
        trainer: Optional[AIVibeTrainer] = None,
        evaluator: Optional[AIVibeEvaluator] = None,
        scorecard_path: str = "./scorecards",
    ):
        """Initialize scheduler with trainer and evaluator."""
        self.trainer = trainer or AIVibeTrainer()
        self.evaluator = evaluator or AIVibeEvaluator()
        self.scorecard_path = Path(scorecard_path)
        self.scorecard_path.mkdir(parents=True, exist_ok=True)

        self._schedules: dict[str, dict] = {}
        self._scorecards: dict[str, Scorecard] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks: list[Callable[[TrainingResult], None]] = []

    def schedule_daily(
        self,
        agent: str,
        time_str: str = "02:00",
        modules: Optional[list[str]] = None,
    ) -> None:
        """
        Schedule daily training for an agent.

        Args:
            agent: Agent name
            time_str: Time in HH:MM format (24-hour)
            modules: Optional specific modules to train
        """
        hour, minute = map(int, time_str.split(":"))
        self._schedules[agent] = {
            "type": "daily",
            "hour": hour,
            "minute": minute,
            "modules": modules,
            "last_run": None,
        }

    def schedule_weekly(
        self,
        agent: str,
        day: int,
        time_str: str = "02:00",
        modules: Optional[list[str]] = None,
    ) -> None:
        """
        Schedule weekly training for an agent.

        Args:
            agent: Agent name
            day: Day of week (0=Monday, 6=Sunday)
            time_str: Time in HH:MM format (24-hour)
            modules: Optional specific modules to train
        """
        hour, minute = map(int, time_str.split(":"))
        self._schedules[agent] = {
            "type": "weekly",
            "day": day,
            "hour": hour,
            "minute": minute,
            "modules": modules,
            "last_run": None,
        }

    def on_training_complete(
        self, callback: Callable[[TrainingResult], None]
    ) -> None:
        """Register callback for training completion."""
        self._callbacks.append(callback)

    def start(self, daemon: bool = True) -> None:
        """Start the scheduler in background thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=daemon)
        self._thread.start()

    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _run_loop(self) -> None:
        """Main scheduler loop."""
        while self._running:
            now = datetime.now()

            for agent, schedule in self._schedules.items():
                if self._should_run(schedule, now):
                    self._execute_training(agent, schedule)
                    schedule["last_run"] = now

            # Sleep for 1 minute before checking again
            time.sleep(60)

    def _should_run(self, schedule: dict, now: datetime) -> bool:
        """Check if schedule should run now."""
        if schedule["last_run"]:
            last_run = schedule["last_run"]
            if schedule["type"] == "daily":
                if (now - last_run) < timedelta(hours=23):
                    return False
            elif schedule["type"] == "weekly":
                if (now - last_run) < timedelta(days=6):
                    return False

        if schedule["type"] == "daily":
            return (
                now.hour == schedule["hour"]
                and now.minute == schedule["minute"]
            )
        elif schedule["type"] == "weekly":
            return (
                now.weekday() == schedule["day"]
                and now.hour == schedule["hour"]
                and now.minute == schedule["minute"]
            )
        return False

    def _execute_training(self, agent: str, schedule: dict) -> None:
        """Execute training for an agent."""
        try:
            # Run training
            result = self.trainer.train_agent(
                agent,
                modules=schedule.get("modules"),
                verbose=False,
            )

            # Update scorecard
            self._update_scorecard(agent, result)

            # Run evaluation
            evaluation = self.evaluator.evaluate(agent)

            # Save results
            self._save_results(agent, result, evaluation)

            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(result)
                except Exception as e:
                    print(f"Callback error: {e}")

        except Exception as e:
            print(f"Training error for {agent}: {e}")

    def _update_scorecard(self, agent: str, result: TrainingResult) -> None:
        """Update agent's scorecard."""
        if agent not in self._scorecards:
            self._scorecards[agent] = Scorecard(agent=agent)

        self._scorecards[agent].add_result(result)

    def _save_results(self, agent: str, result: TrainingResult, evaluation) -> None:
        """Save training results to file."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = self.scorecard_path / f"{agent}_{date_str}.json"

        data = {
            "agent": agent,
            "date": date_str,
            "training": result.to_log_entry(),
            "evaluation": {
                "score": evaluation.overall_score,
                "grade": evaluation.grade,
                "passed": evaluation.passed,
            },
            "scorecard": {
                "total_trainings": self._scorecards[agent].total_trainings,
                "average_score": self._scorecards[agent].average_score,
                "best_score": self._scorecards[agent].best_score,
                "current_streak": self._scorecards[agent].current_streak,
                "trend": self._scorecards[agent].get_trend(),
            },
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def run_now(self, agent: str, verbose: bool = True) -> TrainingResult:
        """
        Run training immediately for an agent.

        Args:
            agent: Agent name
            verbose: Print training progress

        Returns:
            TrainingResult
        """
        result = self.trainer.train_agent(agent, verbose=verbose)
        self._update_scorecard(agent, result)

        # Run evaluation
        evaluation = self.evaluator.evaluate(agent)
        self._save_results(agent, result, evaluation)

        # Print scorecard
        if verbose:
            print("\n" + self.evaluator.generate_scorecard(evaluation))

        return result

    def get_scorecard(self, agent: str) -> Optional[Scorecard]:
        """Get scorecard for an agent."""
        return self._scorecards.get(agent)

    def get_all_scorecards(self) -> dict[str, Scorecard]:
        """Get all agent scorecards."""
        return self._scorecards.copy()

    def load_scorecard(self, agent: str) -> Optional[Scorecard]:
        """Load scorecard from saved files."""
        files = sorted(self.scorecard_path.glob(f"{agent}_*.json"))
        if not files:
            return None

        scorecard = Scorecard(agent=agent)

        for filepath in files:
            with open(filepath) as f:
                data = json.load(f)
                # Reconstruct minimal result for scorecard
                result = TrainingResult(
                    agent=agent,
                    score=data["training"]["score"],
                    modules_trained=data["training"]["modules"],
                    duration_seconds=data["training"]["duration"],
                    timestamp=datetime.fromisoformat(data["training"]["timestamp"]),
                    success=data["training"]["success"],
                )
                scorecard.add_result(result)

        self._scorecards[agent] = scorecard
        return scorecard

    def print_schedule(self) -> None:
        """Print current schedule."""
        print("\nAIVibe Training Schedule")
        print("=" * 40)

        if not self._schedules:
            print("No schedules configured")
            return

        for agent, schedule in self._schedules.items():
            time_str = f"{schedule['hour']:02d}:{schedule['minute']:02d}"
            if schedule["type"] == "daily":
                print(f"  {agent}: Daily at {time_str}")
            elif schedule["type"] == "weekly":
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                day_name = days[schedule["day"]]
                print(f"  {agent}: {day_name} at {time_str}")

            if schedule["last_run"]:
                print(f"    Last run: {schedule['last_run'].strftime('%Y-%m-%d %H:%M')}")

        print("=" * 40)
