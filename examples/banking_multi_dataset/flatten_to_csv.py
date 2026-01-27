"""
Flatten Banking Multi-Dataset to CSV

Converts nested JSON structure (customer -> accounts -> transactions)
into three separate CSV files with proper foreign key relationships.

Usage for IPython/Jupyter:
    # CAI Job (reads from JSON file specified by file_name env var)
    from flatten_to_csv import run_cai_job
    result = run_cai_job()
"""

import json
import csv
import os
import sys
import traceback
from pathlib import Path
from typing import List, Dict, Any


class DataFlattener:
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def flatten(self):
        """Flatten nested JSON to three CSV files"""
        print(f"📂 Loading data from: {self.input_file}")

        with open(self.input_file, 'r') as f:
            data = json.load(f)

        customers = []
        accounts = []
        transactions = []

        # Extract data from nested structure
        print(f"🔄 Flattening data...")
        for record in data:
            # Customer data
            customer = record.get("customer", {})
            customers.append(customer)

            # Accounts data
            for account in record.get("accounts", []):
                accounts.append(account)

                # Transactions data
                for transaction in record.get("transactions", []):
                    # Only include transactions for this account
                    if transaction.get("account_id") == account.get("account_id"):
                        transactions.append(transaction)

        # Write CSV files
        customers_file = self.output_dir / "customers.csv"
        accounts_file = self.output_dir / "accounts.csv"
        transactions_file = self.output_dir / "transactions.csv"

        self._write_csv(customers_file, customers)
        self._write_csv(accounts_file, accounts)
        self._write_csv(transactions_file, transactions)

        print(f"\n✅ Export complete!")
        print(f"📊 Statistics:")
        print(f"   Customers: {len(customers)}")
        print(f"   Accounts: {len(accounts)}")
        print(f"   Transactions: {len(transactions)}")
        print(f"\n📁 Output files:")
        print(f"   {customers_file}")
        print(f"   {accounts_file}")
        print(f"   {transactions_file}")

        return {
            "customers": str(customers_file),
            "accounts": str(accounts_file),
            "transactions": str(transactions_file),
            "stats": {
                "customers": len(customers),
                "accounts": len(accounts),
                "transactions": len(transactions)
            }
        }

    def _write_csv(self, file_path: Path, data: List[Dict[str, Any]]):
        """Write list of dicts to CSV file"""
        if not data:
            print(f"⚠️  Warning: No data to write to {file_path}")
            return

        # Get all unique keys across all records
        fieldnames = set()
        for record in data:
            fieldnames.update(record.keys())
        fieldnames = sorted(fieldnames)

        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"✓ Wrote {len(data)} records to {file_path.name}")


def main():
    """Main entry point - prioritizes CAI job mode, falls back to env vars"""

    # Otherwise, use environment variables
    input_file = os.environ.get('INPUT_FILE')
    output_dir = os.environ.get('OUTPUT_DIR', 'output/csv')

    if not input_file:
        print("Error: INPUT_FILE environment variable not set")
        print("Usage: INPUT_FILE=data.json OUTPUT_DIR=output/ python flatten_to_csv.py")
        sys.exit(1)

    flattener = DataFlattener(input_file, output_dir)
    flattener.flatten()


if __name__ == "__main__":
    main()
