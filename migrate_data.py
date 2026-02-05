import os
from data.repository import JSONRepository, SQLiteRepository
from utils.logger import log_info, log_error

def run_migration():
    """
    Migrates data from JSON storage to a SQLite database.
    This ensures continuity for existing data.
    """
    json_path = "storage/scm_system.json"
    db_path = "storage/scm_system.db"

    print("--- SCM Data Migration Utility ---")
    
    # 1. Check if the source file exists
    if not os.path.exists(json_path):
        print(f"Error: Source file '{json_path}' not found. Nothing to migrate.")
        return

    try:
        # 2. Initialize repositories
        print(f"Reading data from {json_path}...")
        json_repo = JSONRepository(json_path)
        sqlite_repo = SQLiteRepository(db_path)

        # 3. Get customers from the JSON
        customers_to_migrate = json_repo.get_all()
        total = len(customers_to_migrate)

        if total == 0:
            print("The JSON file is empty. No records to migrate.")
            return

        print(f"Found {total} customers. Starting migration to SQLite...")
        print("-" * 40)

        # 4. Migration process
        migrated_count = 0
        for customer in customers_to_migrate:
            try:
                sqlite_repo.save(customer)
                print(f"Migrated: {customer.customer_id} - {customer.name}")
                migrated_count += 1
            except Exception as e:
                print(f"Failed to migrate {customer.customer_id}: {e}")
                log_error(f"Migration error for ID {customer.customer_id}: {e}")

        # 5. Final summary
        print("-" * 40)
        summary = f"Migration finished. Successfully moved {migrated_count}/{total} customers."
        print(summary)
        log_info(summary)

    except Exception as e:
        error_msg = f"Critical migration failure: {e}"
        print(f"{error_msg}")
        log_error(error_msg)

if __name__ == "__main__":
    run_migration()