# Development Log - SCM Project

## [2026-02-03] - First Commit & Project Setup
- **Tasks**: Initialized Git repository and defined project structure.
- **Documentation**: Created `README.md`, `ROADMAP.md`, and `.gitignore`.
- **Architecture**: Defined the directory structure following modular principles (core, data, utils).
- **Status**: Project skeleton is ready for implementation.

## [2026-02-04] - Phase 1: Core Modeling: Abstract Base Class & Concrete Customer Classes
- **Task #1**: Implemented the `Customer` abstract base class in `core/models.py` (Phase 1).
    - **Technical Decisions & OOP Patterns**:
        - **Abstraction**: Used `ABC` and `@abstractmethod` from the Python standard library to define a strict contract for all customer types.
        - **Encapsulation**: Implemented protected attributes using the `_attribute` convention to prevent direct external access.
        - **Properties**: Added `@property` (getters) and setters for `customer_id`, `name`, `email`, and `phone`. This ensures a single point of control for future validations (Phase 2).
        - **Object Identity**: Implemented `__str__` for formatted string representation, and `__eq__` and `__hash__` based on `customer_id` to allow efficient object comparison and usage in sets/dictionaries.
    - **Key Learning**: Clarified the distinction between using `_attribute` (internal storage) and `attribute` (public property interface) to avoid recursion and maintain clean encapsulation.
    - **Status**: Task #1 completed. Ready to implement specific customer subclasses.

- **Task #2**: Completed the implementation of `RegularCustomer`, `PremiumCustomer`, and `CorporateCustomer` in `core/models.py` (Phase 1).
    - **Technical Decisions & OOP Patterns**:
        - **Inheritance & Delegation**: Used `super().__init__()` in all subclasses to delegate basic attribute initialization to the base class, ensuring that global property logic (getters/setters) is applied consistently.
        - **Polymorphism**: 
            - Implemented `calculate_value()` across all classes with different business rules: fixed rates for Regular, point-based bonuses for Premium, and higher base fees for Corporate.
            - Customized `get_details()` to provide type-specific information while maintaining a consistent interface.
        - **Extensible Persistence**: Overrode the `to_dict()` method in `Premium` and `Corporate` classes using a "Call-and-Update" pattern (`data = super().to_dict()`). This allows adding specific fields (like `loyalty_points` or `tax_id`) without duplicating the core data logic.
        - **Default Arguments**: Applied default values in constructors (e.g., `loyalty_points=0`) to increase flexibility when instantiating new objects from different data sources.
        - **Identity Logic**: Verified that `__eq__` and `__hash__` (implemented in the base class) correctly handle comparisons across different subclasses by using the public `customer_id` property.
    - **Key Reflection**: The use of properties without underscores in methods like `__eq__` and `to_dict()` ensures that any future formatting or validation logic added to the `@property` will be automatically reflected throughout the system, avoiding technical debt.
    - **Status**: Phase 1 is now fully complete. Ready to move to Phase 2 (Advanced Validations).

## [2026-02-04] - Phase 2: Exceptions, Validations & Logging
- **Task #3**: Implemented a robust validation layer and error handling system (Phase 2).
    - **Technical Decisions**:
        - **Exception Hierarchy**: Created a custom exception tree in `utils/exceptions.py` starting from a base `SCMError`. This allows for granular error catching (e.g., catching all `ValidationError` types at once or specifically `InvalidEmailError`).
        - **Data Validation (Regex)**: Centralized validation logic in `core/validators.py` using `@staticmethod`. Applied Regular Expressions to enforce strict formats for emails and international phone numbers.
        - **Encapsulation & Setters**: Refactored `Customer` class to trigger validations during both instantiation and attribute updates by calling the validator inside `@property.setter` methods.
        - **Logging Infrastructure**: Implemented a centralized logging system in `utils/logger.py` using Python's `logging` module. Configured to store events in `logs/scm_system.log` with timestamps and severity levels (INFO/ERROR).
        - **Improved Entry Point**: Enhanced `main.py` with hierarchical `try/except` blocks. The system now gracefully handles data errors, logs them, and continues processing the remaining data instead of crashing the application.
    - **Key Learning**: Moving validation from the `__init__` direct assignment to property setters ensures that data integrity is maintained throughout the object's entire lifecycle, not just at creation.
    - **Status**: Phase 2 completed. The system is now secure and traceable. Ready for Phase 3: Data Persistence.

## [2026-02-04] - Phase 3: Data Persistence & Repository Pattern
- **Task #4**: Implemented a dual-layer persistence system (JSON and SQLite).
    - **Technical Decisions & OOP Patterns**:
        - **Repository Pattern**: Introduced the `CustomerRepository` abstract interface in `data/repository.py`. This decouples the business logic from the storage implementation, allowing the system to switch between JSON and SQL with a single line of code change in `main.py`.
        - **JSON Implementation (Step A)**: 
            - Developed `JSONRepository` for lightweight file-based storage.
            - Implemented manual **Idempotency** logic by searching and replacing existing IDs before saving to prevent duplicate records.
            - Solved the **Rehydration** challenge: created a factory-like logic to convert flat JSON dictionaries back into specialized `Customer` objects (`Regular`, `Premium`, `Corporate`).
        - **SQLite Upgrade (Step B)**:
            - Implemented `SQLiteRepository` using the `sqlite3` standard library.
            - Designed a relational schema to store all customer types in a single table, using `NULL` values for type-specific optional fields.
            - Leveraged SQL power: Used `INSERT OR REPLACE` for automatic idempotency and `PRIMARY KEY` constraints for data integrity.
            - Applied **Context Managers** (`with` statements) to ensure safe database connections and automatic transaction commits.
    - **Key Reflection**: The transition from JSON to SQLite was completed without touching the `core/models.py` or the validation logic, proving that the architecture is truly modular and follows the Dependency Inversion Principle.
    - **Status**: Phase 3 (Persistence) is nearly complete. JSON and SQLite repositories are fully functional. Next: Data migration script.

## [2026-02-05] - Phase 3 Completion: Data Migration Utility
- **Tasks**: Developed a standalone migration script to ensure data continuity between storage engines.
    - **Technical Decisions**:
        - **Dual Repository Usage**: Implemented `migrate_data.py` in the project root. The script instantiates both `JSONRepository` (source) and `SQLiteRepository` (target) simultaneously, showcasing the interoperability of the Repository Pattern.
        - **Data Integrity**: The migration process leverages the "Rehydration" logic of the JSON repository and the "Persistence" logic of the SQLite repository, ensuring that all business rules and object types are preserved during the transfer.
        - **Fault Tolerance**: Added granular error handling within the migration loop. If one record fails to migrate, the script logs the error and continues with the next, preventing a total process failure.
        - **Idempotency Check**: Verified that running the migration multiple times does not result in duplicate records in the SQLite database, thanks to the `INSERT OR REPLACE` logic implemented in the previous step.
    - **Key Reflection**: The successful migration confirms that the system's architecture is truly decoupled. We were able to move the entire dataset from a flat-file system to a relational database without modifying the core business logic or the customer models.
    - **Status**: Phase 3 (Persistence) is completed. All milestones in the Roadmap have been achieved.