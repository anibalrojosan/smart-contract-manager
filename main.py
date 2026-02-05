import os
from core.models import RegularCustomer, PremiumCustomer, CorporateCustomer
from utils.exceptions import SCMError, ValidationError
from utils.logger import log_error, log_info
from data.repository import JSONRepository, SQLiteRepository

def run_demonstration():
    log_info("Starting SCM Phase 3 (JSON Persistence) demonstration...")
    print("--- Smart Customer Manager (SCM) - Phase 3 Demo ---\n")

    # 1. Initialize the Repository
    # Create the storage folder if it doesn't exist
    if not os.path.exists('storage'):
        os.makedirs('storage')
    
    # repo = JSONRepository("storage/scm_system.json")
    repo = SQLiteRepository("storage/scm_system.db")

    # 2. Try to load existing customers
    existing_customers = repo.get_all()
    print(f"Loaded {len(existing_customers)} customers from storage.")
    log_info(f"Loaded {len(existing_customers)} customers from JSON.")

    # 3. Test data (Raw Data)
    raw_customers = [
        ("Regular", "R001", "Alice", "alice@email.com", "+56911111111"),
        ("Regular", "R002", "Daniel", "dan@email.com", "+56944444444"),
        ("Premium", "P001", "Bob Jones", "al|ce@email", "+56922222222", 20),   # Invalid email
        ("Corporate", "C001", "Carlos Ruiz", "cruiz@techcorp.com", "1234567890",  'SolutionTech', "1234567890", "CEO", 8), # Invalid phone
        ("Regular", "R003", "D", "dan@email.com", "+56944444444"),             # Too short name
        ('Corporate', 'C002', 'John Doe', 'john.doe@example.com', '+1234567890', 'Tech Corp', '1234567890', 'CEO', 10),
    ]

    print("\nProcessing new data and saving to storage:")
    print("-" * 50)
    
    for data in raw_customers:
        try:
            c_type = data[0]
            if c_type == "Regular":
                customer = RegularCustomer(data[1], data[2], data[3], data[4])
            elif c_type == "Premium":
                customer = PremiumCustomer(data[1], data[2], data[3], data[4], data[5])
            elif c_type == "Corporate":
                customer = CorporateCustomer(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            
            # Save the customer to the repository
            repo.save(customer)
            
            msg = f"Saved {c_type} customer: {customer.name} (ID: {customer.customer_id})"
            print(f"{msg}")
            log_info(msg)
        
        except ValidationError as e:
            error_msg = f"Validation error: {e}"
            print(f"{error_msg}")
            log_error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {type(e).__name__}: {e}"
            print(f"{error_msg}")
            log_error(error_msg)

    # 4. Final verification: List all customers in the repository now
    final_list = repo.get_all()
    print("-" * 50)
    print(f"\nFinal count in storage: {len(final_list)} customers.")
    
    # Show an example of successful rehydration
    if final_list:
        sample = final_list[0]
        print(f"Sample from storage: {sample.get_details()} (Type: {type(sample).__name__})")

if __name__ == "__main__":
    run_demonstration()