"""
AIVibe Command Line Interface

CLI commands for training and evaluating AI agents.
"""

import argparse
import sys
from typing import Optional

from aivibe.evaluator import AIVibeEvaluator
from aivibe.scheduler import TrainingScheduler
from aivibe.trainer import AIVibeTrainer


def train_agent(args: Optional[list[str]] = None) -> int:
    """
    Train an AI agent.

    Usage:
        aivibe-train aikutty
        aivibe-train aivedha --modules flutter dart
        aivibe-train aikutty -v
    """
    parser = argparse.ArgumentParser(
        description="Train an AI agent with knowledge modules"
    )
    parser.add_argument(
        "agent",
        choices=["aikutty", "aivedha"],
        help="Agent to train",
    )
    parser.add_argument(
        "--modules",
        "-m",
        nargs="+",
        help="Specific modules to train",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )

    parsed = parser.parse_args(args)

    trainer = AIVibeTrainer()
    result = trainer.train_agent(
        parsed.agent,
        modules=parsed.modules,
        verbose=parsed.verbose,
    )

    # Print report
    print(trainer.generate_report(result))

    return 0 if result.success else 1


def evaluate_agent(args: Optional[list[str]] = None) -> int:
    """
    Evaluate an AI agent.

    Usage:
        aivibe-evaluate aikutty
        aivibe-evaluate aivedha
    """
    parser = argparse.ArgumentParser(
        description="Evaluate an AI agent's knowledge"
    )
    parser.add_argument(
        "agent",
        choices=["aikutty", "aivedha"],
        help="Agent to evaluate",
    )
    parser.add_argument(
        "--categories",
        "-c",
        nargs="+",
        help="Specific categories to evaluate",
    )

    parsed = parser.parse_args(args)

    evaluator = AIVibeEvaluator()
    result = evaluator.evaluate(
        parsed.agent,
        categories=parsed.categories,
    )

    # Print scorecard
    print(evaluator.generate_scorecard(result))

    return 0 if result.passed else 1


def schedule_training(args: Optional[list[str]] = None) -> int:
    """
    Schedule automated training.

    Usage:
        aivibe-schedule aikutty --daily 02:00
        aivibe-schedule aivedha --weekly 0 03:00
        aivibe-schedule --run-now aikutty
    """
    parser = argparse.ArgumentParser(
        description="Schedule automated training for AI agents"
    )
    parser.add_argument(
        "agent",
        nargs="?",
        choices=["aikutty", "aivedha"],
        help="Agent to schedule",
    )
    parser.add_argument(
        "--daily",
        help="Daily training time (HH:MM)",
    )
    parser.add_argument(
        "--weekly",
        nargs=2,
        metavar=("DAY", "TIME"),
        help="Weekly training (0-6 for Mon-Sun, HH:MM)",
    )
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Run training immediately",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List current schedules",
    )

    parsed = parser.parse_args(args)

    scheduler = TrainingScheduler()

    if parsed.list:
        scheduler.print_schedule()
        return 0

    if parsed.run_now and parsed.agent:
        scheduler.run_now(parsed.agent, verbose=True)
        return 0

    if not parsed.agent:
        parser.print_help()
        return 1

    if parsed.daily:
        scheduler.schedule_daily(parsed.agent, parsed.daily)
        print(f"Scheduled daily training for {parsed.agent} at {parsed.daily}")

    if parsed.weekly:
        day = int(parsed.weekly[0])
        time_str = parsed.weekly[1]
        scheduler.schedule_weekly(parsed.agent, day, time_str)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(f"Scheduled weekly training for {parsed.agent} on {days[day]} at {time_str}")

    scheduler.print_schedule()

    if parsed.daily or parsed.weekly:
        print("\nStarting scheduler... Press Ctrl+C to stop.")
        try:
            scheduler.start(daemon=False)
        except KeyboardInterrupt:
            scheduler.stop()
            print("\nScheduler stopped.")

    return 0


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="AIVibe - AI Agent Training Package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  train       Train an AI agent
  evaluate    Evaluate agent knowledge
  schedule    Schedule automated training

Examples:
  aivibe train aikutty -v
  aivibe evaluate aikutty
  aivibe schedule aikutty --daily 02:00
        """,
    )
    parser.add_argument(
        "command",
        choices=["train", "evaluate", "schedule"],
        help="Command to run",
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Command arguments",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version",
    )

    if "--version" in sys.argv:
        from aivibe import __version__
        print(f"AIVibe version {__version__}")
        return 0

    parsed = parser.parse_args()

    commands = {
        "train": train_agent,
        "evaluate": evaluate_agent,
        "schedule": schedule_training,
    }

    return commands[parsed.command](parsed.args)


if __name__ == "__main__":
    sys.exit(main())
