"""
AIVibe SDLC Knowledge Module

Complete Software Development Life Cycle (SDLC) phases,
agent roles, and development workflow patterns.
"""


class SDLCKnowledge:
    """Comprehensive SDLC and development workflow knowledge."""

    VERSION = "1.0"
    TOTAL_PHASES = 10

    PHASES = {
        1: {
            "name": "Requirements Analysis",
            "code": "REQ",
            "description": "Gather and analyze project requirements from stakeholders",
            "agent_role": "AIVEDHA - Requirement Analyst",
            "inputs": [
                "User stories or feature requests",
                "Business requirements document",
                "Stakeholder interviews",
                "Existing system documentation",
            ],
            "outputs": [
                "Software Requirements Specification (SRS)",
                "Functional requirements list",
                "Non-functional requirements",
                "Acceptance criteria",
                "User personas",
            ],
            "activities": [
                "Clarify ambiguous requirements with stakeholders",
                "Translate user needs into technical requirements",
                "Identify constraints and dependencies",
                "Prioritize features (MoSCoW method)",
                "Define scope and out-of-scope items",
            ],
            "deliverables": ["requirements.md", "user_stories.md", "acceptance_criteria.md"],
            "validation": [
                "All requirements are testable",
                "No conflicting requirements",
                "Stakeholder sign-off obtained",
                "Traceability matrix created",
            ],
        },
        2: {
            "name": "System Design",
            "code": "SYS",
            "description": "Design the overall system architecture and components",
            "agent_role": "AIKUTTY - System Architect",
            "inputs": [
                "Approved SRS document",
                "Technical constraints",
                "Infrastructure requirements",
                "Integration points",
            ],
            "outputs": [
                "System Architecture Document (SAD)",
                "Component diagrams",
                "Data flow diagrams",
                "API specifications",
                "Technology stack decisions",
            ],
            "activities": [
                "Design high-level architecture",
                "Define microservices/modules boundaries",
                "Select technology stack",
                "Design API contracts",
                "Plan for scalability and performance",
                "Define security architecture",
            ],
            "deliverables": ["architecture.md", "api_specs.yaml", "component_diagram.md"],
            "validation": [
                "Architecture supports all requirements",
                "Scalability requirements addressed",
                "Security considerations documented",
                "Technology choices justified",
            ],
        },
        3: {
            "name": "UI/UX Design",
            "code": "UIX",
            "description": "Design user interfaces and user experience flows",
            "agent_role": "AIKUTTY - UI/UX Designer",
            "inputs": [
                "User personas",
                "User stories",
                "Brand guidelines",
                "Accessibility requirements",
            ],
            "outputs": [
                "Wireframes",
                "High-fidelity mockups",
                "User flow diagrams",
                "Design system/components",
                "Interactive prototypes",
            ],
            "activities": [
                "Create wireframes for all screens",
                "Design responsive layouts",
                "Define color schemes and typography",
                "Create reusable component library",
                "Design micro-interactions",
                "Ensure accessibility compliance (WCAG 2.1)",
            ],
            "deliverables": ["wireframes/", "design_system.md", "user_flows.md"],
            "validation": [
                "All user flows covered",
                "Responsive design verified",
                "Accessibility audit passed",
                "Stakeholder approval obtained",
            ],
        },
        4: {
            "name": "Database Design",
            "code": "DBS",
            "description": "Design database schema and data architecture",
            "agent_role": "AIKUTTY - Database Architect",
            "inputs": [
                "Data requirements from SRS",
                "Entity relationships",
                "Performance requirements",
                "Data retention policies",
            ],
            "outputs": [
                "Entity-Relationship Diagram (ERD)",
                "Database schema",
                "Migration scripts",
                "Indexing strategy",
                "Backup/recovery plan",
            ],
            "activities": [
                "Identify entities and relationships",
                "Normalize database schema",
                "Design indexes for query patterns",
                "Plan data partitioning/sharding",
                "Define data validation rules",
                "Create migration scripts",
            ],
            "deliverables": ["schema.sql", "migrations/", "erd.md"],
            "validation": [
                "Schema supports all data requirements",
                "Referential integrity maintained",
                "Query performance optimized",
                "Security (RLS, encryption) implemented",
            ],
        },
        5: {
            "name": "API Development",
            "code": "API",
            "description": "Develop backend APIs and services",
            "agent_role": "AIKUTTY - Backend Developer",
            "inputs": [
                "API specifications",
                "Database schema",
                "Authentication requirements",
                "Third-party integration specs",
            ],
            "outputs": [
                "RESTful/GraphQL APIs",
                "Authentication endpoints",
                "Business logic implementation",
                "API documentation",
                "Integration connectors",
            ],
            "activities": [
                "Implement API endpoints",
                "Add authentication/authorization",
                "Write business logic",
                "Integrate with database",
                "Connect third-party services",
                "Write unit tests for all endpoints",
            ],
            "deliverables": ["src/api/", "tests/api/", "openapi.yaml"],
            "validation": [
                "All endpoints implemented",
                "Authentication working",
                "Unit test coverage > 80%",
                "API documentation complete",
                "Security vulnerabilities addressed",
            ],
        },
        6: {
            "name": "Flutter Development",
            "code": "FLT",
            "description": "Develop Flutter mobile/web application",
            "agent_role": "AIKUTTY - Flutter Developer",
            "inputs": [
                "UI/UX designs",
                "API documentation",
                "Component library specs",
                "State management plan",
            ],
            "outputs": [
                "Flutter application code",
                "Reusable widgets",
                "State management implementation",
                "Platform-specific code",
                "Localization files",
            ],
            "activities": [
                "Implement UI screens",
                "Create reusable widget library",
                "Integrate with backend APIs",
                "Implement state management (Riverpod)",
                "Add platform-specific features",
                "Implement deep linking",
                "Add analytics and crash reporting",
            ],
            "deliverables": ["lib/", "test/", "pubspec.yaml"],
            "validation": [
                "All screens implemented",
                "Responsive on all platforms",
                "Widget tests passing",
                "No lint warnings",
                "Performance benchmarks met",
            ],
        },
        7: {
            "name": "Testing",
            "code": "TST",
            "description": "Comprehensive testing of the application",
            "agent_role": "AIKUTTY - QA Engineer",
            "inputs": [
                "Application code",
                "Test cases from requirements",
                "Acceptance criteria",
                "Performance requirements",
            ],
            "outputs": [
                "Unit test suite",
                "Integration test suite",
                "E2E test suite",
                "Performance test results",
                "Security audit report",
            ],
            "activities": [
                "Write and run unit tests",
                "Perform integration testing",
                "Execute E2E tests",
                "Conduct performance testing",
                "Perform security testing",
                "Accessibility testing",
                "Cross-platform testing",
            ],
            "deliverables": ["test/", "test_results/", "security_audit.md"],
            "validation": [
                "Unit test coverage > 80%",
                "All integration tests passing",
                "E2E tests for critical flows",
                "No critical security issues",
                "Performance benchmarks met",
            ],
        },
        8: {
            "name": "Integration",
            "code": "INT",
            "description": "Integrate all components and third-party services",
            "agent_role": "AIKUTTY - Integration Engineer",
            "inputs": [
                "All developed components",
                "Third-party API credentials",
                "Environment configurations",
                "Integration test plans",
            ],
            "outputs": [
                "Integrated application",
                "CI/CD pipeline",
                "Environment configurations",
                "Integration documentation",
            ],
            "activities": [
                "Integrate frontend with backend",
                "Configure third-party services",
                "Set up CI/CD pipeline",
                "Configure environment variables",
                "Run integration tests",
                "Perform smoke testing",
            ],
            "deliverables": [".github/workflows/", "docker-compose.yml", "env.example"],
            "validation": [
                "All components integrated",
                "CI/CD pipeline working",
                "Integration tests passing",
                "Environments configured correctly",
            ],
        },
        9: {
            "name": "Deployment",
            "code": "DEP",
            "description": "Deploy application to production environment",
            "agent_role": "AIKUTTY - DevOps Engineer",
            "inputs": [
                "Tested application build",
                "Infrastructure requirements",
                "Deployment checklist",
                "Rollback plan",
            ],
            "outputs": [
                "Deployed application",
                "Infrastructure as Code",
                "Monitoring dashboards",
                "Alerting rules",
                "Runbook documentation",
            ],
            "activities": [
                "Provision infrastructure",
                "Configure CDN and caching",
                "Deploy to app stores",
                "Set up monitoring and alerting",
                "Configure auto-scaling",
                "Perform production smoke tests",
                "Document runbooks",
            ],
            "deliverables": ["terraform/", "k8s/", "runbook.md"],
            "validation": [
                "Application accessible",
                "SSL/TLS configured",
                "Monitoring active",
                "Alerts configured",
                "Rollback tested",
            ],
        },
        10: {
            "name": "Maintenance",
            "code": "MNT",
            "description": "Ongoing maintenance and support",
            "agent_role": "AIKUTTY - Support Engineer",
            "inputs": [
                "Bug reports",
                "Feature requests",
                "Performance metrics",
                "Security bulletins",
            ],
            "outputs": [
                "Bug fixes",
                "Performance improvements",
                "Security patches",
                "Feature updates",
                "Documentation updates",
            ],
            "activities": [
                "Monitor application health",
                "Triage and fix bugs",
                "Apply security patches",
                "Optimize performance",
                "Update dependencies",
                "Respond to user feedback",
            ],
            "deliverables": ["CHANGELOG.md", "patches/", "performance_reports/"],
            "validation": [
                "SLA compliance",
                "No critical bugs open",
                "Dependencies up to date",
                "Security vulnerabilities addressed",
            ],
        },
    }

    AGENT_ROLES = {
        "AIVEDHA": {
            "full_name": "AI Visual Exploration & Design Helper Agent",
            "type": "Gemini Coordinator",
            "responsibilities": [
                "Receive and clarify user requirements",
                "Multi-language prompt translation",
                "Duplicate detection across projects",
                "Phase-appropriate question generation",
                "Requirement validation",
            ],
            "phases": [1],  # Requirements Analysis
            "skills": [
                "Natural language understanding",
                "Multi-language support (20+ languages)",
                "Requirement extraction",
                "Stakeholder communication",
            ],
        },
        "AIKUTTY": {
            "full_name": "AI Kutty - Implementation Specialist",
            "type": "Claude Implementation Agent",
            "responsibilities": [
                "Code generation and implementation",
                "Architecture design",
                "Database design",
                "API development",
                "Flutter development",
                "Testing and QA",
                "Deployment and DevOps",
            ],
            "phases": [2, 3, 4, 5, 6, 7, 8, 9, 10],  # All except Requirements
            "skills": [
                "Flutter 3.24+ development",
                "Dart 3.5+ programming",
                "Python backend development",
                "PostgreSQL database design",
                "AWS cloud services",
                "Firebase integration",
                "CI/CD automation",
            ],
        },
    }

    WORKFLOW = {
        "handoff": {
            "aivedha_to_aikutty": {
                "trigger": "Requirements approved by user",
                "data_passed": [
                    "Structured requirements document",
                    "User stories with acceptance criteria",
                    "Technical constraints",
                    "Priority matrix",
                ],
                "validation": "AIKUTTY confirms understanding of requirements",
            },
            "aikutty_to_aivedha": {
                "trigger": "Clarification needed during implementation",
                "data_passed": [
                    "Specific technical questions",
                    "Design decisions requiring user input",
                    "Scope change requests",
                ],
                "validation": "AIVEDHA translates and presents to user",
            },
        },
        "phase_transitions": {
            "approval_required": True,
            "auto_advance": False,
            "rollback_allowed": True,
            "parallel_phases": [],  # Strictly sequential
        },
    }

    QUALITY_GATES = {
        "code_quality": {
            "lint_errors": 0,
            "test_coverage": 80,
            "documentation": "required",
            "no_deprecated": True,
            "no_duplicates": True,
        },
        "security": {
            "owasp_check": "required",
            "dependency_audit": "required",
            "secrets_scan": "required",
            "vulnerability_score": "low",
        },
        "performance": {
            "page_load": "< 3s",
            "api_response": "< 500ms",
            "memory_usage": "optimized",
            "bundle_size": "minimized",
        },
    }

    def get_all(self) -> dict:
        """Get complete SDLC knowledge."""
        return {
            "version": self.VERSION,
            "total_phases": self.TOTAL_PHASES,
            "phases": self.PHASES,
            "agent_roles": self.AGENT_ROLES,
            "workflow": self.WORKFLOW,
            "quality_gates": self.QUALITY_GATES,
        }

    def get_phases(self) -> dict:
        """Get all SDLC phases."""
        return self.PHASES

    def get_phase(self, phase_number: int) -> dict | None:
        """Get specific phase details."""
        return self.PHASES.get(phase_number)

    def get_agent_roles(self) -> dict:
        """Get agent role definitions."""
        return self.AGENT_ROLES

    def get_quality_gates(self) -> dict:
        """Get quality gate requirements."""
        return self.QUALITY_GATES

    def get_phase_for_agent(self, agent: str) -> list[int]:
        """Get phases assigned to an agent."""
        role = self.AGENT_ROLES.get(agent.upper())
        if role:
            return role["phases"]
        return []

    def get_phase_deliverables(self, phase_number: int) -> list[str]:
        """Get deliverables for a specific phase."""
        phase = self.PHASES.get(phase_number)
        if phase:
            return phase.get("deliverables", [])
        return []
