import json
import os
from abc import ABC, abstractmethod
from typing import List, Optional
from core.models import Customer, RegularCustomer, PremiumCustomer, CorporateCustomer
from utils.exceptions import SCMError
import sqlite3

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


class SQLiteRepository(CustomerRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        """Helper to get a connection to SQLite."""
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        """Creates the customers table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    type TEXT NOT NULL,
                    loyalty_points INTEGER,
                    company_name TEXT,
                    tax_id TEXT,
                    position TEXT
                )
            ''')
            conn.commit()

    def save(self, customer: Customer) -> None:
        """Saves or updates a customer using SQL."""
        data = customer.to_dict()
        
        # Prepare the fields. If they don't exist in the dict (e.g. Regular), set them to None
        fields = (
            data['id'], data['name'], data['email'], data['phone'], data['type'],
            data.get('loyalty_points'), data.get('company_name'), 
            data.get('tax_id'), data.get('position')
        )

        query = '''
            INSERT OR REPLACE INTO customers 
            (id, name, email, phone, type, loyalty_points, company_name, tax_id, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        with self._get_connection() as conn:
            conn.execute(query, fields)
            conn.commit()

    def get_all(self) -> List[Customer]:
        """Fetches all rows and rehydrates them into Customer objects."""
        customers = []
        query = "SELECT * FROM customers"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query).fetchall()
            
            for row in rows:
                # row is a tuple: (id, name, email, phone, type, loyalty, company, tax, pos)
                c_id, name, email, phone, class_name = row[0], row[1], row[2], row[3], row[4]
                
                if class_name == 'RegularCustomer':
                    obj = RegularCustomer(c_id, name, email, phone)
                elif class_name == 'PremiumCustomer':
                    obj = PremiumCustomer(c_id, name, email, phone, row[5] or 0)
                elif class_name == 'CorporateCustomer':
                    obj = CorporateCustomer(c_id, name, email, phone, row[6], row[7], row[8])
                else:
                    # For now, raise a custom exception and stop the program
                    # Later, we can ignore the unknown customer type and register it as a warning 
                    # in the log
                    raise SCMError(f'Unknown customer type: {class_name}')
                
                customers.append(obj)
        return customers

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Finds a single customer by ID using a WHERE clause."""
        query = "SELECT * FROM customers WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(query, (customer_id,)).fetchone()
            
            if not row:
                return None
            
            # Reuse the same rehydration logic (could be refactored later)
            class_name = row[4]
            if class_name == 'RegularCustomer':
                return RegularCustomer(row[0], row[1], row[2], row[3])
            elif class_name == 'PremiumCustomer':
                return PremiumCustomer(row[0], row[1], row[2], row[3], row[5])
            elif class_name == 'CorporateCustomer':
                return CorporateCustomer(row[0], row[1], row[2], row[3], row[6], row[7], row[8])
            else:
                # For now, raise a custom exception and stop the program
                raise SCMError(f'Unknown customer type: {class_name}')