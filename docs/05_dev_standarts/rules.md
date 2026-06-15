# 📜 Development Standards & Project Rules

This document establishes engineering guardrails, commit patterns, and architectural workflows for the SmartCity platform.

---

## 1. Commit Message Standard (Conventional Commits)

All commits must follow the **Conventional Commits** specification using the **Imperative Mood** in the header.

### 📋 Formatting Pattern

```text
<type>(<scope>): <short description in imperative mood>

[optional body: detailed explanations, trade-offs, or breaking changes]

[optional footer: task IDs or issue references]
```

### 🛠️ Allowed Commit Types (`<type>`)

- **`feat`**: A new feature implemented in the codebase.
- **`fix`**: A bug fix.
- **`docs`**: Changes strictly bound to documentation (Markdown files, diagrams).
- **`refactor`**: Code changes that neither fix a bug nor add a feature (e.g., restructuring).
- **`infra`** / **`chore`**: Building pipelines, Docker configs, dependencies updates, or tooling.
- **`test`**: Adding missing tests or correcting existing test suites.

### 📝 Examples

- *Good Header*: `feat(simulator): implement local sqlite database encryption`
- *Bad Header*: `fixed bugs in socket` (No type, no scope, past tense).

---

## 2. Architecture Decision Records (ADR) Workflow

An ADR must be compiled **before** introducing any major architectural pivot or technological shift. Records are stored chronologically inside the `docs/06_ADR/` directory.

### 📂 File Naming Convention

`XXXX-short-lowercase-description.md` (e.g., `0001-switch-to-timescaledb.md`)

### 📋 Unified ADR Template

```markdown
# 🏛️ ADR-XXXX: [Short Title of the Decision]

* **Date**: YYYY-MM-DD
* **Author**: @username
* **Status**: Proposed / Accepted / Deprecated / Superseded by [[ADR-YYYY]]

## 1. Context (The Problem)
[Describe the technical challenge, current operational limitations, or changing requirements driving this decision.]

## 2. Decision (The Solution)
[State the explicit technological or design pattern choice. Be direct.]

## 3. Consequences & Trade-offs
*   **Pros (+)**: [What do we gain? Speed, scalability, simplified maintenance?]
*   **Cons (-)**: [What is the cost? Memory overhead, infrastructure complexity, learning curve?]
```

---

## 🤝 3. Core Project Guardrails (Best Practices)

### A. Atomic Commits & Pull Requests

- **One Change per Commit**: Do not mix structural code modifications with documentation updates or refactoring sweeps.
- **Synchronous Docs updates**: If a feature modifies a data schema or an API interface, the corresponding `.md` file (e.g., `data_dictionary.md`) must be modified inside the **same** Git branch or Pull Request.

### B. Clean Database Engineering

- **Database Independence via Abstraction**: Route all data reads and mutations strictly through the `Database manager` (Repository/UoW pattern). Direct native SQL strings inside business logic/routers are forbidden.
- **Immutable Migrations**: Never modify an already committed Alembic migration file. If a schema needs changes, always generate a new forward migration script.

### C. Software Engineering Paradigms & Pragmatism

- **Core Architectural Principles**: Adhere to **KISS** (Keep It Simple, Stupid) as the ultimate priority for solo development. Apply **DRY** (Don't Repeat Yourself) to business logic, but favor duplication over wrong abstractions. Enforce **SOLID** and clean **OOP** principles within internal core layers to guarantee modularity.
- **Design Patterns Implementation**: Leverage established **Design Patterns** (e.g., Repository, Unit of Work, Singleton, Factory) where structural scalability requires them.
- **Pragmatic Flexibility Warning**: Patterns must serve the architecture, not the other way around. Follow strict software design patterns whenever feasible; however, **reasonable compromises and pragmatic simplifications are explicitly allowed** if a pattern creates excessive boilerplate or over-engineering.
