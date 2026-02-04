from abc import ABC, abstractmethod

class Customer(ABC):
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._phone = phone

    # --- Getters (Properties) and Setters ---
    @property
    def customer_id(self):
        return self._customer_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # The name validation will be implemented later
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # The Regex validation will be implemented later
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        # The Regex validation will be implemented later
        if not value:
            raise ValueError("Phone number cannot be empty")
        self._phone = value

    # --- Abstract Methods ---
    @abstractmethod
    def get_details(self) -> str:
        """Return a formatted string with customer info."""
        pass

    @abstractmethod
    def calculate_value(self) -> float:
        """Calculate the customer's value based on their type."""
        pass

    # --- Persistence Helper ---
    def to_dict(self) -> dict:
        """Converts the object to a dictionary for JSON/SQLite."""
        return {
            "id": self._customer_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "type": self.__class__.__name__
        }

    def __str__(self):
        """Return a formatted string with customer info."""
        return f"[{self.__class__.__name__}] {self.name} ({self.email})"

    def __eq__(self, other):
        """Check if two customers are equal by comparing their IDs."""
        if not isinstance(other, Customer):
            return False
        return self.customer_id == other.customer_id