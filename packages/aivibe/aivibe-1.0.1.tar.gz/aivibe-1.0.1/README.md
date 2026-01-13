# AIVibe - AI Agent Training Package

[![PyPI version](https://badge.fury.io/py/aivibe.svg)](https://pypi.org/project/aivibe/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AIVibe** is the comprehensive AI agent training package for [VibeKaro.ai](https://vibekaro.ai) - the AI-powered full-stack development platform. This package contains complete knowledge modules for training AI agents with production-grade coding standards.

## Features

- **Complete Flutter/Dart Knowledge** - Latest Flutter 3.24+, Dart 3.5+ standards
- **Multi-Platform Support** - iOS SDK 26+, Android API 36, Web hybrid
- **Backend Expertise** - Kotlin, Python, JavaScript, PostgreSQL
- **Cloud Services** - AWS, Google Cloud, Firebase integration patterns
- **SDLC Framework** - 10-phase waterfall model with agent roles
- **Coding Standards** - Zero-tolerance, production-ready patterns
- **Auto-Training** - Daily scheduled training with evaluation
- **Scorecard System** - Training effectiveness tracking

## Installation

```bash
pip install aivibe
```

## Quick Start

### Train AI Agent

```python
from aivibe import AIVibeTrainer

trainer = AIVibeTrainer()
result = trainer.train_agent("aikutty")
print(f"Training Score: {result.score}%")
```

### Schedule Daily Training

```bash
aivibe-schedule --agent aikutty --time 02:00
```

### Evaluate Agent Knowledge

```bash
aivibe-evaluate --agent aikutty --output scorecard.json
```

## Knowledge Modules

| Module | Description | Version |
|--------|-------------|---------|
| `flutter` | Flutter framework, widgets, state management | 3.24.x |
| `dart` | Dart language, null safety, patterns | 3.5.x |
| `kotlin` | Kotlin coroutines, Android development | 2.0.x |
| `python` | Python 3.12+, async patterns | 3.12.x |
| `javascript` | ES2024, TypeScript 5.5 | ES2024 |
| `postgresql` | PostgreSQL 16, Aurora patterns | 16.x |
| `aws` | AWS services, CDK, Lambda | Latest |
| `gcloud` | Google Cloud, Firebase | Latest |
| `sdlc` | 10-phase SDLC, agent roles | 1.0 |

## Agent Roles by SDLC Phase

| Phase | AiVedha Role | AiKutty Role |
|-------|--------------|--------------|
| 1. Requirements | Gather & clarify | Document structure |
| 2. System Design | Architecture review | Component design |
| 3. UI/UX Design | User feedback | Widget specifications |
| 4. Database Design | Schema review | Migration scripts |
| 5. API Development | Endpoint validation | Implementation |
| 6. Flutter Dev | Code review | Full implementation |
| 7. Testing | Test planning | Test execution |
| 8. Integration | Integration review | E2E testing |
| 9. Deployment | Release coordination | Build & deploy |
| 10. Maintenance | User support | Bug fixes |

## Coding Standards

### Zero-Tolerance Policy
- No lint errors or warnings
- No type mismatches
- No deprecated dependencies
- No duplicate code
- Complete error handling
- Full documentation

### Naming Conventions
- `camelCase` for variables and functions
- `PascalCase` for classes and types
- `snake_case` for file names
- `SCREAMING_SNAKE_CASE` for constants

## Training Evaluation

Training sessions are evaluated on:

1. **Syntax Correctness** (25%) - Code compiles without errors
2. **Best Practices** (25%) - Follows recommended patterns
3. **Security Compliance** (20%) - No vulnerabilities
4. **Performance** (15%) - Optimized code
5. **Documentation** (15%) - Complete dartdocs

## Configuration

Create `aivibe.yaml` in your project:

```yaml
agent: aikutty
schedule:
  enabled: true
  time: "02:00"
  timezone: "UTC"
evaluation:
  min_score: 85
  report_path: ./reports/
training:
  modules:
    - flutter
    - dart
    - aws
    - sdlc
```

## API Reference

### AIVibeTrainer

```python
class AIVibeTrainer:
    def train_agent(self, agent_name: str, modules: list = None) -> TrainingResult
    def evaluate_agent(self, agent_name: str) -> EvaluationResult
    def get_scorecard(self, agent_name: str) -> Scorecard
    def schedule_training(self, agent_name: str, cron: str) -> None
```

### TrainingResult

```python
@dataclass
class TrainingResult:
    agent: str
    score: float
    modules_trained: list[str]
    duration_seconds: float
    timestamp: datetime
    details: dict
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

- Documentation: https://docs.vibekaro.ai
- Issues: https://github.com/aicippy/aivibe/issues
- Email: support@vibekaro.ai

---

Built with excellence by [AICippy Technologies](https://aicippy.com) for [VibeKaro.ai](https://vibekaro.ai)
