"""
AIVibe Knowledge Base

Complete knowledge modules for Flutter, Dart, Kotlin, Python,
JavaScript, PostgreSQL, AWS, Google Cloud, Firebase, and SDLC.
"""

from aivibe.knowledge.flutter import FlutterKnowledge
from aivibe.knowledge.dart import DartKnowledge
from aivibe.knowledge.kotlin import KotlinKnowledge
from aivibe.knowledge.python import PythonKnowledge
from aivibe.knowledge.javascript import JavaScriptKnowledge
from aivibe.knowledge.postgresql import PostgreSQLKnowledge
from aivibe.knowledge.aws import AWSKnowledge
from aivibe.knowledge.gcloud import GCloudKnowledge
from aivibe.knowledge.firebase import FirebaseKnowledge
from aivibe.knowledge.sdlc import SDLCKnowledge
from aivibe.knowledge.troubleshooting import TroubleshootingKnowledge


class KnowledgeBase:
    """
    Central knowledge base containing all modules.

    Usage:
        kb = KnowledgeBase()
        flutter_knowledge = kb.flutter.get_all()
        sdlc_phases = kb.sdlc.get_phases()
    """

    def __init__(self):
        self.flutter = FlutterKnowledge()
        self.dart = DartKnowledge()
        self.kotlin = KotlinKnowledge()
        self.python = PythonKnowledge()
        self.javascript = JavaScriptKnowledge()
        self.postgresql = PostgreSQLKnowledge()
        self.aws = AWSKnowledge()
        self.gcloud = GCloudKnowledge()
        self.firebase = FirebaseKnowledge()
        self.sdlc = SDLCKnowledge()
        self.troubleshooting = TroubleshootingKnowledge()

        self._modules = {
            "flutter": self.flutter,
            "dart": self.dart,
            "kotlin": self.kotlin,
            "python": self.python,
            "javascript": self.javascript,
            "postgresql": self.postgresql,
            "aws": self.aws,
            "gcloud": self.gcloud,
            "firebase": self.firebase,
            "sdlc": self.sdlc,
            "troubleshooting": self.troubleshooting,
        }

    def get_module(self, name: str):
        """Get a specific knowledge module."""
        return self._modules.get(name)

    def get_all_modules(self) -> list[str]:
        """Get list of all available modules."""
        return list(self._modules.keys())

    def get_complete_knowledge(self) -> dict:
        """Get complete knowledge from all modules."""
        return {
            name: module.get_all()
            for name, module in self._modules.items()
        }

    def get_coding_standards(self) -> dict:
        """Get coding standards from all relevant modules."""
        return {
            "flutter": self.flutter.get_coding_standards(),
            "dart": self.dart.get_coding_standards(),
            "kotlin": self.kotlin.get_coding_standards(),
            "python": self.python.get_coding_standards(),
            "javascript": self.javascript.get_coding_standards(),
            "postgresql": self.postgresql.get_coding_standards(),
        }

    def get_version_info(self) -> dict:
        """Get version information for all technologies."""
        return {
            "flutter": self.flutter.VERSION,
            "dart": self.dart.VERSION,
            "kotlin": self.kotlin.VERSION,
            "python": self.python.VERSION,
            "javascript": self.javascript.VERSION,
            "postgresql": self.postgresql.VERSION,
            "ios_sdk": "18.0",
            "android_api": "36",
        }


__all__ = [
    "KnowledgeBase",
    "FlutterKnowledge",
    "DartKnowledge",
    "KotlinKnowledge",
    "PythonKnowledge",
    "JavaScriptKnowledge",
    "PostgreSQLKnowledge",
    "AWSKnowledge",
    "GCloudKnowledge",
    "FirebaseKnowledge",
    "SDLCKnowledge",
    "TroubleshootingKnowledge",
]
