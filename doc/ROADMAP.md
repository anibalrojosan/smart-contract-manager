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

## Phase 3: Data Persistence (Evolutionary Approach)
**Branch:** `feature/phase3-persistence`

### Step A: Initial Persistence with JSON
- [ ] Define `CustomerRepository` abstract interface (Repository Pattern).
- [ ] Implement `JSONRepository` for local file storage.
- [ ] Develop logic to convert JSON dictionaries back into specific Customer objects using the `from_dict` factory method.
- [ ] Integration test: Save and load customers from `customers.json`.

### Step B: Professional Upgrade to SQLite
- [ ] Design the relational database schema (Table structure).
- [ ] Implement `SQLiteRepository` using the same `CustomerRepository` interface.
- [ ] Handle database connections, cursors, and SQL transactions (CRUD).
- [ ] Create a **Migration Script** to transfer data from JSON to SQLite.
- [ ] Final verification: Switch repository types in `main.py` with zero impact on business logic.

---

## Future improvements
- [ ] Unit Testing implementation (`unittest` or `pytest`).
- [ ] UI/API evaluation.