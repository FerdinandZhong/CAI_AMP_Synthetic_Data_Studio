"""
Flatten Banking Multi-Dataset to Single Flat Structure

Converts nested JSON structure (customer -> accounts -> transactions)
into a single flat file where each row represents one customer with
aggregated account and transaction summaries.

Output format matches banking_datasets_examples_flat.json pattern:
- All customer fields
- num_accounts: count of accounts
- account_types: comma-separated list
- total_balance: sum of all account balances
- num_transactions: count of transactions
- sample_transaction_categories: unique categories (comma-separated)

Usage for IPython/Jupyter:
    # CAI Job (reads from JSON file specified by file_name env var)
    from flatten_to_csv_2 import run_cai_job
    result = run_cai_job()

    # Direct usage
    from flatten_to_csv_2 import DataFlattener
    flattener = DataFlattener("input.json", "output/")
    flattener.flatten()
"""

import json
import csv
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Set


class DataFlattener:
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def flatten(self) -> Dict[str, Any]:
        """Flatten nested JSON to single flat structure per customer"""
        print(f"Loading data from: {self.input_file}")

        with open(self.input_file, 'r') as f:
            data = json.load(f)

        flat_records = []

        print(f"Flattening {len(data)} customer records...")
        for record in data:
            flat_record = self._flatten_record(record)
            flat_records.append(flat_record)

        # Write output files
        json_file = self.output_dir / "customers_flat.json"
        csv_file = self.output_dir / "customers_flat.csv"

        self._write_json(json_file, flat_records)
        self._write_csv(csv_file, flat_records)

        print(f"\nExport complete!")
        print(f"Statistics:")
        print(f"   Total customers: {len(flat_records)}")
        print(f"   Total accounts: {sum(r['num_accounts'] for r in flat_records)}")
        print(f"   Total transactions: {sum(r['num_transactions'] for r in flat_records)}")
        print(f"\nOutput files:")
        print(f"   {json_file}")
        print(f"   {csv_file}")

        return {
            "json_file": str(json_file),
            "csv_file": str(csv_file),
            "stats": {
                "customers": len(flat_records),
                "total_accounts": sum(r['num_accounts'] for r in flat_records),
                "total_transactions": sum(r['num_transactions'] for r in flat_records)
            }
        }

    def _flatten_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten a single customer record with accounts and transactions"""
        customer = record.get("customer", {})
        accounts = record.get("accounts", [])
        transactions = record.get("transactions", [])

        # Start with customer fields
        flat = dict(customer)

        # Aggregate account information
        flat["num_accounts"] = len(accounts)
        flat["account_types"] = ", ".join(
            acc.get("account_type", "") for acc in accounts
        )
        flat["total_balance"] = sum(
            acc.get("current_balance", 0) for acc in accounts
        )

        # Aggregate transaction information
        flat["num_transactions"] = len(transactions)

        # Get unique transaction categories (preserve order of first occurrence)
        seen_categories: Set[str] = set()
        unique_categories: List[str] = []
        for txn in transactions:
            category = txn.get("transaction_category", "")
            if category and category not in seen_categories:
                seen_categories.add(category)
                unique_categories.append(category)

        flat["sample_transaction_categories"] = ", ".join(unique_categories)

        return flat

    def _write_json(self, file_path: Path, data: List[Dict[str, Any]]):
        """Write list of dicts to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Wrote {len(data)} records to {file_path.name}")

    def _write_csv(self, file_path: Path, data: List[Dict[str, Any]]):
        """Write list of dicts to CSV file"""
        if not data:
            print(f"Warning: No data to write to {file_path}")
            return

        # Define column order (customer fields first, then aggregates)
        customer_fields = [
            "cust_id", "first_name", "last_name", "date_of_birth",
            "email", "phone", "address", "postal_code", "nationality",
            "region", "customer_since", "customer_segment", "credit_score"
        ]
        aggregate_fields = [
            "num_accounts", "account_types", "total_balance",
            "num_transactions", "sample_transaction_categories"
        ]

        # Get any additional fields not in our predefined list
        all_keys = set()
        for record in data:
            all_keys.update(record.keys())

        extra_fields = sorted(
            all_keys - set(customer_fields) - set(aggregate_fields)
        )

        fieldnames = customer_fields + aggregate_fields + extra_fields

        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"Wrote {len(data)} records to {file_path.name}")


def run_cai_job() -> Dict[str, Any]:
    """Entry point for CAI job execution"""
    input_file = os.environ.get('INPUT_FILE')
    output_dir = os.environ.get('OUTPUT_DIR', 'output/flat')

    if not input_file:
        raise ValueError(
            "INPUT_FILE environment variable not set. "
            "Set INPUT_FILE to the path of your nested JSON data."
        )

    flattener = DataFlattener(input_file, output_dir)
    return flattener.flatten()


def main():
    """Main entry point for command line usage"""
    input_file = os.environ.get('INPUT_FILE')
    output_dir = os.environ.get('OUTPUT_DIR', 'output/flat')

    if not input_file:
        print("Error: INPUT_FILE environment variable not set")
        print("Usage: INPUT_FILE=data.json OUTPUT_DIR=output/ python flatten_to_csv_2.py")
        sys.exit(1)

    flattener = DataFlattener(input_file, output_dir)
    flattener.flatten()


if __name__ == "__main__":
    main()
