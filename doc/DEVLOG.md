# Development Log - SCM Project

## [2026-02-03] - First Commit & Project Setup
- **Tasks**: Initialized Git repository and defined project structure.
- **Documentation**: Created `README.md`, `ROADMAP.md`, and `.gitignore`.
- **Architecture**: Defined the directory structure following modular principles (core, data, utils).
- **Status**: Project skeleton is ready for implementation.

## [2026-02-04] - Core Modeling: Abstract Base Class & Concrete Customer Classes
- **Task #1**: Implemented the `Customer` abstract base class in `core/models.py`.
    - **Technical Decisions & OOP Patterns**:
        - **Abstraction**: Used `ABC` and `@abstractmethod` from the Python standard library to define a strict contract for all customer types.
        - **Encapsulation**: Implemented protected attributes using the `_attribute` convention to prevent direct external access.
        - **Properties**: Added `@property` (getters) and setters for `customer_id`, `name`, `email`, and `phone`. This ensures a single point of control for future validations (Phase 2).
        - **Object Identity**: Implemented `__str__` for formatted string representation, and `__eq__` and `__hash__` based on `customer_id` to allow efficient object comparison and usage in sets/dictionaries.
    - **Key Learning**: Clarified the distinction between using `_attribute` (internal storage) and `attribute` (public property interface) to avoid recursion and maintain clean encapsulation.
    - **Status**: Task #1 completed. Ready to implement specific customer subclasses.

- **Task #2**: Completed the implementation of `RegularCustomer`, `PremiumCustomer`, and `CorporateCustomer` in `core/models.py`.
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