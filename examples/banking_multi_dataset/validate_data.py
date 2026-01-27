#!/usr/bin/env python3
"""
Banking Data Validator

Performs local validation checks on generated banking data:
- Referential integrity (foreign keys)
- Temporal consistency
- Business logic rules
- Data formatting

Usage:
    python validate_data.py --input banking_data.json
    python validate_data.py --input banking_data.json --verbose
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Set
from collections import defaultdict


class BankingDataValidator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)

    def validate(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate banking data

        Returns:
            True if data passes all critical checks, False otherwise
        """
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

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _validate_record(
        self,
        idx: int,
        record: Dict[str, Any],
        all_customer_ids: Set[str],
        all_account_ids: Set[str],
        all_transaction_ids: Set[str]
    ):
        """Validate a single customer record"""
        customer = record.get("customer", {})
        accounts = record.get("accounts", [])
        transactions = record.get("transactions", [])

        cust_id = customer.get("cust_id")
        record_prefix = f"Record {idx} (Customer {cust_id})"

        # Validate customer
        self._validate_customer(record_prefix, customer)

        # Validate accounts
        for acc_idx, account in enumerate(accounts):
            self._validate_account(
                f"{record_prefix}, Account {acc_idx}",
                account,
                customer,
                all_customer_ids
            )

        # Validate transactions
        for trans_idx, transaction in enumerate(transactions):
            self._validate_transaction(
                f"{record_prefix}, Transaction {trans_idx}",
                transaction,
                accounts,
                all_account_ids
            )

    def _validate_customer(self, prefix: str, customer: Dict[str, Any]):
        """Validate customer data"""
        required_fields = [
            "cust_id", "first_name", "last_name", "date_of_birth",
            "email", "phone", "customer_since", "customer_segment", "credit_score"
        ]

        for field in required_fields:
            if not customer.get(field):
                self.errors.append(f"{prefix}: Missing required field '{field}'")

        # Validate credit score
        credit_score = customer.get("credit_score")
        if credit_score:
            if not isinstance(credit_score, int) or credit_score < 300 or credit_score > 850:
                self.errors.append(
                    f"{prefix}: Invalid credit_score {credit_score} (must be 300-850)"
                )

        # Validate date format
        dob = customer.get("date_of_birth")
        if dob:
            try:
                dob_date = datetime.strptime(dob, "%Y-%m-%d")
                age = (datetime.now() - dob_date).days / 365.25
                if age < 18 or age > 120:
                    self.warnings.append(
                        f"{prefix}: Unusual age {age:.0f} years"
                    )
            except ValueError:
                self.errors.append(
                    f"{prefix}: Invalid date_of_birth format '{dob}' (expected YYYY-MM-DD)"
                )

        # Validate customer_since
        customer_since = customer.get("customer_since")
        if customer_since:
            try:
                datetime.strptime(customer_since, "%Y-%m-%d")
            except ValueError:
                self.errors.append(
                    f"{prefix}: Invalid customer_since format '{customer_since}'"
                )

        # Validate phone format
        phone = customer.get("phone")
        if phone and not phone.startswith("555-"):
            self.warnings.append(
                f"{prefix}: Phone '{phone}' doesn't use 555 prefix (privacy guideline)"
            )

    def _validate_account(
        self,
        prefix: str,
        account: Dict[str, Any],
        customer: Dict[str, Any],
        all_customer_ids: Set[str]
    ):
        """Validate account data"""
        required_fields = [
            "account_id", "cust_id", "account_type", "account_status",
            "open_date", "current_balance", "currency", "interest_rate"
        ]

        for field in required_fields:
            if account.get(field) is None:
                self.errors.append(f"{prefix}: Missing required field '{field}'")

        # Referential integrity: cust_id must exist
        acc_cust_id = account.get("cust_id")
        if acc_cust_id and acc_cust_id not in all_customer_ids:
            self.errors.append(
                f"{prefix}: Foreign key violation - cust_id '{acc_cust_id}' not found"
            )

        # Check cust_id matches parent customer
        if acc_cust_id and customer.get("cust_id") != acc_cust_id:
            self.errors.append(
                f"{prefix}: cust_id mismatch - account has '{acc_cust_id}' "
                f"but parent customer is '{customer.get('cust_id')}'"
            )

        # Temporal consistency
        customer_since = customer.get("customer_since")
        open_date = account.get("open_date")
        if customer_since and open_date:
            try:
                cs_date = datetime.strptime(customer_since, "%Y-%m-%d")
                od_date = datetime.strptime(open_date, "%Y-%m-%d")
                if od_date < cs_date:
                    self.errors.append(
                        f"{prefix}: Temporal violation - open_date {open_date} "
                        f"before customer_since {customer_since}"
                    )
            except ValueError as e:
                self.errors.append(f"{prefix}: Date parsing error - {e}")

        # Business logic: Savings accounts can't be negative
        account_type = account.get("account_type")
        balance = account.get("current_balance")
        overdraft = account.get("overdraft_limit", 0)

        if account_type in ["Savings", "CD", "Money Market"] and balance is not None:
            if balance < 0:
                self.errors.append(
                    f"{prefix}: Business rule violation - {account_type} "
                    f"has negative balance {balance}"
                )

        # Checking accounts shouldn't exceed overdraft limit
        if account_type == "Checking" and balance is not None and overdraft is not None:
            if balance < -overdraft:
                self.errors.append(
                    f"{prefix}: Business rule violation - balance {balance} "
                    f"exceeds overdraft_limit {overdraft}"
                )

        # Closed accounts should have zero balance
        status = account.get("account_status")
        if status == "Closed" and balance != 0:
            self.warnings.append(
                f"{prefix}: Closed account has non-zero balance {balance}"
            )

        # Interest rate should match account type
        interest_rate = account.get("interest_rate")
        if interest_rate is not None:
            if account_type == "Checking" and interest_rate > 1.0:
                self.warnings.append(
                    f"{prefix}: Unusual interest_rate {interest_rate}% for Checking"
                )
            elif account_type == "Savings" and interest_rate > 5.0:
                self.warnings.append(
                    f"{prefix}: Unusual interest_rate {interest_rate}% for Savings"
                )

    def _validate_transaction(
        self,
        prefix: str,
        transaction: Dict[str, Any],
        accounts: List[Dict[str, Any]],
        all_account_ids: Set[str]
    ):
        """Validate transaction data"""
        required_fields = [
            "transaction_id", "account_id", "transaction_date",
            "transaction_type", "amount"
        ]

        for field in required_fields:
            if transaction.get(field) is None:
                self.errors.append(f"{prefix}: Missing required field '{field}'")

        # Referential integrity: account_id must exist
        trans_acc_id = transaction.get("account_id")
        if trans_acc_id and trans_acc_id not in all_account_ids:
            self.errors.append(
                f"{prefix}: Foreign key violation - account_id '{trans_acc_id}' not found"
            )

        # Find parent account
        parent_account = None
        for account in accounts:
            if account.get("account_id") == trans_acc_id:
                parent_account = account
                break

        if not parent_account:
            self.errors.append(
                f"{prefix}: Transaction references account_id '{trans_acc_id}' "
                f"not in parent customer's accounts"
            )
            return

        # Temporal consistency: transaction_date >= account.open_date
        trans_date = transaction.get("transaction_date")
        open_date = parent_account.get("open_date")
        if trans_date and open_date:
            try:
                td = datetime.strptime(trans_date, "%Y-%m-%d")
                od = datetime.strptime(open_date, "%Y-%m-%d")
                if td < od:
                    self.errors.append(
                        f"{prefix}: Temporal violation - transaction_date {trans_date} "
                        f"before account open_date {open_date}"
                    )
            except ValueError as e:
                self.errors.append(f"{prefix}: Date parsing error - {e}")

        # Validate transaction_type
        trans_type = transaction.get("transaction_type")
        amount = transaction.get("amount")
        if trans_type == "Debit" and amount is not None and amount > 0:
            self.warnings.append(
                f"{prefix}: Debit transaction has positive amount {amount}"
            )
        elif trans_type == "Credit" and amount is not None and amount < 0:
            self.warnings.append(
                f"{prefix}: Credit transaction has negative amount {amount}"
            )

    def _print_results(self):
        """Print validation results"""
        print("=" * 60)
        print("📊 Validation Results")
        print("=" * 60)

        print(f"\nStatistics:")
        print(f"  Customers:    {self.stats['customers']}")
        print(f"  Accounts:     {self.stats['accounts']}")
        print(f"  Transactions: {self.stats['transactions']}")

        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for error in self.errors[:20]:  # Show first 20
                print(f"  • {error}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more errors")

        if self.warnings:
            print(f"\n⚠️  Warnings: {len(self.warnings)}")
            if self.verbose:
                for warning in self.warnings[:20]:
                    print(f"  • {warning}")
                if len(self.warnings) > 20:
                    print(f"  ... and {len(self.warnings) - 20} more warnings")
            else:
                print(f"  (Use --verbose to see warnings)")

        if not self.errors and not self.warnings:
            print("\n✅ All validation checks passed!")
        elif not self.errors:
            print(f"\n✅ No critical errors found (but {len(self.warnings)} warnings)")
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} errors")


def main():
    parser = argparse.ArgumentParser(
        description="Validate generated banking data",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input JSON file with banking data"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed warnings"
    )

    args = parser.parse_args()

    # Load data
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        return 1

    with open(input_path, 'r') as f:
        data = json.load(f)

    # Validate
    validator = BankingDataValidator(verbose=args.verbose)
    is_valid = validator.validate(data)

    return 0 if is_valid else 1


if __name__ == "__main__":
    exit(main())
