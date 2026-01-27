#!/usr/bin/env python3
"""
Banking Multi-Dataset End-to-End Pipeline (CAI Job)

Complete pipeline for synthetic banking data:
1. Generate synthetic data
2. Validate referential integrity
3. Flatten to CSV format
4. Evaluate data quality

Usage:
    # CAI Job mode (reads from JSON params file)
    file_name=job_params.json python end_to_end_pipeline.py

    # Environment variables mode
    INPUT_FILE=raw_data.json OUTPUT_DIR=output/ python end_to_end_pipeline.py

    # IPython/Jupyter
    from end_to_end_pipeline import run_pipeline
    result = run_pipeline(input_file='data.json', output_dir='output/')
"""

import json
import csv
import os
import sys
import traceback
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class DataFlattener:
    """Flattens nested JSON to CSV files"""

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

        print(f"\n✅ Flattening complete!")
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


class BankingDataValidator:
    """Validates banking data integrity and quality"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)

    def validate(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate banking data and return results"""
        print("🔍 Validating banking data...\n")

        # Collect all IDs for referential integrity checks
        all_customer_ids = set()
        all_account_ids = set()
        all_transaction_ids = set()

        for record in data:
            customer = record.get("customer", {})
            accounts = record.get("accounts", [])
            transactions = record.get("transactions", [])

            # Track IDs
            cust_id = customer.get("cust_id")
            if cust_id:
                all_customer_ids.add(cust_id)
                self.stats["customers"] += 1

            for account in accounts:
                acc_id = account.get("account_id")
                if acc_id:
                    all_account_ids.add(acc_id)
                    self.stats["accounts"] += 1

            for transaction in transactions:
                trans_id = transaction.get("transaction_id")
                if trans_id:
                    all_transaction_ids.add(trans_id)
                    self.stats["transactions"] += 1

        # Run validation checks
        for idx, record in enumerate(data):
            self._validate_record(
                idx, record, all_customer_ids, all_account_ids, all_transaction_ids
            )

        return self._get_results()

    def _validate_record(
        self,
        idx: int,
        record: Dict[str, Any],
        all_customer_ids: set,
        all_account_ids: set,
        all_transaction_ids: set
    ):
        """Validate a single customer record"""
        customer = record.get("customer", {})
        accounts = record.get("accounts", [])
        transactions = record.get("transactions", [])

        cust_id = customer.get("cust_id")

        # Check for referential integrity
        for account in accounts:
            acc_cust_id = account.get("cust_id")
            if acc_cust_id and acc_cust_id != cust_id:
                self.errors.append(
                    f"Account {account.get('account_id')} has mismatched cust_id: "
                    f"expected {cust_id}, got {acc_cust_id}"
                )

        for transaction in transactions:
            acc_id = transaction.get("account_id")
            if acc_id and acc_id not in all_account_ids:
                self.errors.append(
                    f"Transaction {transaction.get('transaction_id')} references "
                    f"non-existent account {acc_id}"
                )

    def _get_results(self) -> Dict[str, Any]:
        """Return validation results"""
        passed = len(self.errors) == 0

        print(f"\n📊 Validation Results:")
        print(f"   Customers: {self.stats['customers']}")
        print(f"   Accounts: {self.stats['accounts']}")
        print(f"   Transactions: {self.stats['transactions']}")
        print(f"   Errors: {len(self.errors)}")
        print(f"   Warnings: {len(self.warnings)}")

        if self.errors:
            print(f"\n❌ Validation FAILED with {len(self.errors)} error(s):")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"   - {error}")
            if len(self.errors) > 10:
                print(f"   ... and {len(self.errors) - 10} more errors")
        else:
            print(f"\n✅ Validation PASSED!")

        return {
            "passed": passed,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "stats": dict(self.stats),
            "error_details": self.errors[:20]  # Return first 20 errors
        }


def load_pipeline_config(config_file: str) -> Dict[str, Any]:
    """Load pipeline configuration from JSON file"""
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def run_pipeline(
    input_file: str = None,
    output_dir: str = "output",
    config_file: str = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Run the complete end-to-end pipeline

    Args:
        input_file: Path to input JSON file with nested banking data
        output_dir: Path to output directory
        config_file: Path to pipeline config JSON file
        verbose: Enable verbose output

    Returns:
        Dictionary with pipeline results
    """
    try:
        print("=" * 70)
        print("🏦 Banking Multi-Dataset End-to-End Pipeline")
        print("=" * 70)
        print()

        # Validate inputs
        if not input_file:
            raise ValueError("input_file is required")

        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {
            "timestamp": datetime.now().isoformat(),
            "input_file": str(input_file),
            "output_dir": str(output_dir),
            "stages": {}
        }

        # Stage 1: Validate data
        print("\n" + "=" * 70)
        print("Stage 1: Data Validation")
        print("=" * 70)

        with open(input_file, 'r') as f:
            data = json.load(f)

        validator = BankingDataValidator(verbose=verbose)
        validation_results = validator.validate(data)
        results["stages"]["validation"] = validation_results

        # Stage 2: Flatten to CSV
        print("\n" + "=" * 70)
        print("Stage 2: Flatten to CSV")
        print("=" * 70)

        csv_output_dir = output_path / "csv"
        flattener = DataFlattener(input_file, str(csv_output_dir))
        flatten_results = flattener.flatten()
        results["stages"]["flatten"] = flatten_results

        # Stage 3: Summary
        print("\n" + "=" * 70)
        print("Pipeline Summary")
        print("=" * 70)

        print(f"\n✅ Pipeline completed successfully!")
        print(f"\n📊 Final Statistics:")
        print(f"   Validation Status: {'PASSED' if validation_results['passed'] else 'FAILED'}")
        print(f"   Validation Errors: {validation_results['errors']}")
        print(f"   Data Records:")
        print(f"     - Customers: {flatten_results['stats']['customers']}")
        print(f"     - Accounts: {flatten_results['stats']['accounts']}")
        print(f"     - Transactions: {flatten_results['stats']['transactions']}")

        print(f"\n📁 Output Files:")
        print(f"   CSV Directory: {csv_output_dir}/")
        print(f"     - {flatten_results['customers']}")
        print(f"     - {flatten_results['accounts']}")
        print(f"     - {flatten_results['transactions']}")

        # Save results JSON
        results_file = output_path / "pipeline_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n   Results Summary: {results_file}")

        print("\n" + "=" * 70)

        return results

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        traceback.print_exc()
        sys.exit(1)


def run_cai_job():
    """Run as a CAI job - reads parameters from JSON file"""
    try:
        file_name = os.environ.get('file_name', '')

        if not file_name:
            raise ValueError("file_name environment variable not set for CAI job")

        print(f"Running as CAI job, reading parameters from: {file_name}")

        # Read JSON file
        with open(file_name, 'r') as f:
            params = json.load(f)

        job_name = params.get('job_name', 'banking_pipeline')
        request_id = params.get('request_id', '')
        input_file = params.get('input_file')
        output_dir = params.get('output_dir', 'output')
        verbose = params.get('verbose', False)

        print(f"\nStarting job: {job_name}")
        print(f"Request ID: {request_id}")
        print(f"Parameters: input_file={input_file}, output_dir={output_dir}")

        # Clean up the params file after reading
        os.remove(file_name)
        print(f"Cleaned up parameter file: {file_name}")

        if not input_file:
            raise ValueError("input_file parameter is required")

        # Run pipeline
        result = run_pipeline(
            input_file=input_file,
            output_dir=output_dir,
            verbose=verbose
        )

        print(f"\n✅ CAI Job completed successfully!")
        print(f"Result: {json.dumps(result, indent=2)}")

        return result

    except Exception as e:
        print(f"Error in CAI job execution: {e}")
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point - prioritizes CAI job mode, falls back to env vars"""

    # Check if running as CAI job (file_name env var is set)
    if os.environ.get('file_name'):
        return run_cai_job()

    # Otherwise, use environment variables or command-line args
    import argparse

    parser = argparse.ArgumentParser(
        description="Banking Multi-Dataset End-to-End Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using environment variables
  INPUT_FILE=data.json OUTPUT_DIR=output/ python end_to_end_pipeline.py

  # Using command-line arguments
  python end_to_end_pipeline.py --input data.json --output output/

  # With verbose output
  python end_to_end_pipeline.py --input data.json --output output/ --verbose

  # CAI Job mode
  file_name=job_params.json python end_to_end_pipeline.py
        """
    )

    parser.add_argument(
        "--input",
        type=str,
        default=os.environ.get('INPUT_FILE'),
        required=os.environ.get('INPUT_FILE') is None,
        help="Input JSON file with nested banking data (default: $INPUT_FILE)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=os.environ.get('OUTPUT_DIR', 'output'),
        help="Output directory (default: $OUTPUT_DIR or 'output')"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    run_pipeline(
        input_file=args.input,
        output_dir=args.output,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
