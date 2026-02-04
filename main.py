from core.models import RegularCustomer, PremiumCustomer, CorporateCustomer
from utils.exceptions import SCMError, ValidationError
from utils.logger import log_error, log_info

def run_demonstration():
    log_info("Starting SMC demonstration...")
    print("--- Smart Customer Manager (SCM) - Phase 2 Demo ---\n")

    valid_customers = []
    
    # Creation of different types of customers
    raw_customers = [
        ("Regular", "R001", "Alice", "alice@email.com", "+56911111111"),
        ("Regular", "R002", "Daniel", "dan@email.com", "+56944444444"),
        ("Premium", "P001", "Bob Jones", "al|ce@email", "+56922222222", 20),   # Invalid email
        ("Corporate", "C001", "Carlos Ruiz", "cruiz@techcorp.com", "1234567890",  'SolutionTech', "1234567890", "CEO", 8), # Invalid phone
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
            msg = f'Successfully created {data[0]} customer: {customer.get_details()}'
            print(msg)
            log_info(msg)
        
        except ValidationError as e:
            error_msg = f'Validation error: {e}'
            print(error_msg)
            log_error(error_msg)
        except SCMError as e:
            error_msg = f'System error: {e}'
            print(error_msg)
            log_error(error_msg)
        except Exception as e:
            error_msg = f'Unexpected error: {type(e).__name__}: {e}'
            print(error_msg)
            log_error(error_msg)

    print("-" * 50)
    summary_msg = f'Total valid customers created: {len(valid_customers)}'
    print(summary_msg)
    log_info(summary_msg)

if __name__ == "__main__":
    run_demonstration()