import json
import os
from abc import ABC, abstractmethod
from typing import List, Optional
from core.models import Customer, RegularCustomer, PremiumCustomer, CorporateCustomer

class CustomerRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Customer]:
        pass

    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        pass

class JSONRepository(CustomerRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Ensure the file exists when initializing
        if not os.path.exists(self.file_path):
            self._write_to_file([])

    def _read_file(self) -> list:
        """Helper to read the raw list from JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_to_file(self, data: list) -> None:
        """Helper to write a list to the JSON file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def save(self, customer: Customer) -> None:
        """Saves a customer. If ID exists, it updates it."""
        customers_data = self._read_file()
        
        # Convert the object to a dictionary
        new_data = customer.to_dict()
        
        # Search if it already exists to update it or add it
        found = False
        for i, c in enumerate(customers_data):
            if c['id'] == customer.customer_id:
                customers_data[i] = new_data
                found = True
                break
        
        # If it doesn't exist in the file, add it
        if not found:
            customers_data.append(new_data)
            
        self._write_to_file(customers_data)

    def get_all(self) -> List[Customer]:
        """Reads JSON and converts dictionaries back to Customer objects."""
        raw_data = self._read_file()
        customers = []
        
        for item in raw_data:
            # Factory method to convert JSON dictionaries back into specific Customer objects
            c_type = item.get('type')
            if c_type == 'RegularCustomer':
                obj = RegularCustomer(item['id'], item['name'], item['email'], item['phone'])
            elif c_type == 'PremiumCustomer':
                obj = PremiumCustomer(item['id'], item['name'], item['email'], item['phone'], item.get('loyalty_points', 0))
            elif c_type == 'CorporateCustomer':
                obj = CorporateCustomer(item['id'], item['name'], item['email'], item['phone'], 
                                        item['company_name'], item['tax_id'], item['position'])
            else:
                raise ValueError(f'Unknown customer type: {c_type}')
            
            # Add the object to the list of customers
            customers.append(obj)
            
        return customers

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Finds a specific customer by ID."""
        all_customers = self.get_all()
        for c in all_customers:
            if c.customer_id == customer_id:
                return c
        return None