# Project Roadmap: SCM

This document outlines the development phases and the branching strategy for the Smart Customer Manager project.

## Branching Strategy (Simplified GitFlow)
- `main`: Stable code and production-ready versions.
- `develop`: Integration branch for ongoing features.
- `feature/phase-X`: Temporary branches for specific phase goals.

---

## Phase 1: Modeling & Business Logic (OOP)
**Branch:** `feature/phase1-oop`
- [ ] Define the `Customer` abstract base class.
- [ ] Implement subclasses: `Regular`, `Premium`, and `Corporate`.
- [ ] Implement special methods (`__str__`, `__eq__`).
- [ ] In-memory instantiation tests.

## Phase 2: Validations & Error Handling
**Branch:** `feature/phase2-validations`
- [ ] Create custom exceptions (e.g., `InvalidEmailError`).
- [ ] Implement `@property` decorators for attribute validation.
- [ ] Utility module with Regex for data sanitization.
- [ ] Basic logging system for error tracking.

## Phase 3: Data Persistence (JSON to SQLite)
**Branch:** `feature/phase3-persistence`
- [ ] Implement `JSONRepository` for quick persistence.
- [ ] Design the SQLite database schema.
- [ ] Implement `SQLiteRepository` (DAO pattern).
- [ ] Data migration script from JSON to SQL.

---

## Future improvements
- [ ] Unit Testing implementation (`unittest` or `pytest`).
- [ ] UI/API evaluation.