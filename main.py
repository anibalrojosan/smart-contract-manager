from core.models import RegularCustomer, PremiumCustomer, CorporateCustomer
from utils.exceptions import SCMError, ValidationError

def run_demonstration():
    print("--- Smart Customer Manager (SCM) - Phase 2 Demo ---\n")

    valid_customers = []
    
    # Creation of different types of customers
    raw_customers = [
        ("Regular", "R001", "Alice", "alice@email.com", "+56911111111"),
        ("Regular", "R002", "Daniel", "dan@email.com", "+56944444444"),
        ("Premium", "P001", "Bob Jones", "al|ce@email", "+56922222222", 20),   # Invalid email
        ("Corporate", "C001", "Carlos Ruiz", "cruiz@techcorp.com", "1234567890",  'SolutionTech', "1234567890", "CEO", 10), # Invalid phone
        ("Regular", "R003", "D", "dan@email.com", "+56944444444"),             # Too short name
        ('Corporate', 'C002', 'John Doe', 'john.doe@example.com', '+1234567890', 'Tech Corp', '1234567890', 'CEO', 10),
    ]

    print("Trying to create customers from raw data:")
    print("-" * 50)
    
    for data in raw_customers:
        try:
            if data[0] == "Regular":
                customer = RegularCustomer(data[1], data[2], data[3], data[4])
            elif data[0] == "Premium":
                customer = PremiumCustomer(data[1], data[2], data[3], data[4], data[5])
            elif data[0] == "Corporate":
                customer = CorporateCustomer(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
            
            valid_customers.append(customer)
            print(f'Successfully created {data[0]} customer: {customer.get_details()}')
        
        except ValidationError as e:
            print(f'Validation error: {e}')
        except SCMError as e:
            print(f'System error: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')

    print("-" * 50)
    print(f'Total valid customers created: {len(valid_customers)}')

if __name__ == "__main__":
    run_demonstration()