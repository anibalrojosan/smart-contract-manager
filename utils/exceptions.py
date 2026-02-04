class SCMError(Exception):
    """Base class for all exceptions in the SCM system."""
    def __init__(self, message="A system error occurred"):
        self.message = message
        super().__init__(self.message)

class ValidationError(SCMError):
    """Exception raised for errors in the input data validation."""
    pass

class InvalidEmailError(ValidationError):
    """Raised when the email format is incorrect."""
    def __init__(self, email, message="Invalid email format"):
        self.email = email
        self.full_message = f"{message}: '{email}'"
        super().__init__(self.full_message)

class InvalidPhoneError(ValidationError):
    """Raised when the phone number format is incorrect."""
    def __init__(self, phone, message="Invalid phone number format"):
        self.phone = phone
        self.full_message = f"{message}: '{phone}'"
        super().__init__(self.full_message)

class CustomerNotFoundError(SCMError):
    """Raised when a requested customer does not exist in the system."""
    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"Customer with ID '{customer_id}' was not found.")