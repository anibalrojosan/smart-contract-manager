import re
from utils.exceptions import InvalidEmailError, InvalidPhoneError, ValidationError

class DataValidator:
    """Utility class for validating customer data using Regex."""

    # Simple email pattern: 'text' + '@' + 'text' + '.' + 'text'
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Phone pattern: optional '+' followed by 9 to 15 digits
    PHONE_REGEX = r'^\+?[1-9]\d{8,14}$'

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validates the email format.
        Raises InvalidEmailError if invalid.
        """
        if not email or not re.match(DataValidator.EMAIL_REGEX, email):
            raise InvalidEmailError(email)
        return email.strip().lower()

    @staticmethod
    def validate_phone(phone: str) -> str:
        """
        Validates the phone format.
        Raises InvalidPhoneError if invalid.
        """
        if not phone or not re.match(DataValidator.PHONE_REGEX, phone):
            raise InvalidPhoneError(phone)
        return phone.strip()

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Validates that the name is not empty and has a minimum length.
        """
        if not name or len(name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        return name.strip()