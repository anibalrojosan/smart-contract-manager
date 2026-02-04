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

    def __hash__(self):
        """Return a hash of the customer's ID. Useful for sets and dictionaries."""
        return hash(self.customer_id)


class RegularCustomer(Customer):
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        super().__init__(customer_id, name, email, phone)

    def get_details(self) -> str:
        """Return basic contact information for a regular customer."""
        return f"Regular Customer: {self.name}, Contact: {self.email}"

    def calculate_value(self) -> float:
        """Regular customers have a fixed base value."""
        return 100.0

    def calculate_discount(self) -> float:
        """Applies a standard 5% discount over the base value."""
        return 0.05 * self.calculate_value()

class PremiumCustomer(Customer):
    def __init__(self, customer_id: str, name: str, email: str, phone: str, loyalty_points: int = 0):
        super().__init__(customer_id, name, email, phone)
        # Premium customers have loyalty points
        self._loyalty_points = loyalty_points

    @property
    def loyalty_points(self):
        return self._loyalty_points

    @loyalty_points.setter
    def loyalty_points(self, value):
        if value < 0:
            raise ValueError("Loyalty points cannot be negative")
        self._loyalty_points = value

    def get_details(self) -> str:
        """Returns detailed info including loyalty status."""
        return f"PREMIUM CUSTOMER - {self.name} | Points: {self.loyalty_points}"

    def calculate_value(self) -> float:
        """Premium customers have a base rate plus a bonus for loyalty points."""
        base_premium_fee = 200.0
        point_bonus = self.loyalty_points * 0.5
        return base_premium_fee + point_bonus

    def to_dict(self) -> dict:
        """Extends the base dictionary with premium-specific data."""
        data = super().to_dict()
        data.update({
            "loyalty_points": self.loyalty_points
        })
        return data