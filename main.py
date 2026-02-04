from core.models import RegularCustomer, PremiumCustomer, CorporateCustomer

def run_demonstration():
    print("--- Smart Customer Manager (SCM) - Phase 1 Demo ---\n")

    # 1. Creation of different types of customers
    customers = [
        RegularCustomer("R001", "Alice Smith", "alice@email.com", "+56911111111"),
        PremiumCustomer("P001", "Bob Jones", "bob@premium.com", "+56922222222", loyalty_points=150),
        CorporateCustomer(
            "C001", "Carlos Ruiz", "cruiz@techcorp.com", "+56933333333",
            company_name="Tech Corp", tax_id="77.777.777-7", position="CTO", seniority=10
        ),
        PremiumCustomer("P002", "Charlie Brown", "charlie@premium.com", "+56944444444", loyalty_points=200),
        CorporateCustomer(
            "C002", "Diana Martinez", "dmartinez@techcorp.com", "+56955555555",
            company_name="Tech Corp", tax_id="77.777.777-7", position="CEO", seniority=5
        ),
        RegularCustomer("R002", "Eve Johnson", "eve@email.com", "+56966666666"),
        PremiumCustomer("P003", "Frank Davis", "frank@premium.com", "+56977777777", loyalty_points=250),
        CorporateCustomer(
            "C003", "George Wilson", "gwilson@techcorp.com", "+56988888888",
            company_name="Tech Corp", tax_id="77.777.777-7", position="CFO", seniority=15
        )
    ]

    # 2. Polymorphism demonstration
    # All customers are 'Customer', so they all have get_details() and calculate_value()
    # but each one behaves differently.
    print("Listing Customers and their calculated values:")
    print("-" * 50)
    
    for client in customers:
        print(f"Details: {client.get_details()}")
        print(f"Value:   ${client.calculate_value():.2f}")
        print(f"JSON Export: {client.to_dict()}")
        print("-" * 50)

    # 3. Equality demonstration (__eq__)
    print("\nTesting Object Equality:")
    another_alice = RegularCustomer("R002", "Alice Smith", "alice@email.com", "+56911111111")
    print(f"Is same ID Alice equal to original Alice? {customers[0] == another_alice}")
    print(f"Hash comparison: {hash(customers[0]) == hash(another_alice)}")

if __name__ == "__main__":
    run_demonstration()