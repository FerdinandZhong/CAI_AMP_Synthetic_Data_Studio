# Banking Multi-Dataset Example Project

This example project demonstrates how to generate three interconnected synthetic banking datasets with referential integrity:
1. **Customers** - Customer profile information
2. **Accounts** - Bank accounts linked to customers
3. **Transactions** - Financial transactions linked to accounts

## Features

- **Referential Integrity**: All foreign key relationships are maintained automatically
- **Realistic Banking Data**: Follows real-world banking business rules
- **Flexible Generation**: Control customer segments, account types, and transaction patterns
- **Quality Evaluation**: Built-in evaluation prompt for data quality assessment
- **Multiple Interfaces**: Use via Web UI, API, or CLI

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[UI_USAGE_GUIDE.md](UI_USAGE_GUIDE.md)** - Complete guide for using the Web UI ⭐ NEW
- **[UI_WORKFLOW.md](UI_WORKFLOW.md)** - Visual workflow diagrams for UI
- **README.md** (this file) - Comprehensive API and CLI documentation

## File Structure

```
banking_multi_dataset/
├── 📚 Documentation
│   ├── README.md                    # Comprehensive guide (API/CLI)
│   ├── QUICKSTART.md                # 5-minute quick start
│   ├── UI_USAGE_GUIDE.md            # Web UI step-by-step guide ⭐
│   ├── UI_WORKFLOW.md               # Visual UI workflow diagrams
│   ├── TEST_RESULTS.md              # Test validation report
│   └── SUMMARY.md                   # Implementation summary
├── 📄 Template Files
│   ├── examples.json                # Sample data (3 customers)
│   ├── custom_prompt.txt            # Generation instructions
│   ├── evaluation_prompt.txt        # Quality evaluation criteria
│   └── topics.txt                   # 70 suggested topics
└── 🛠  Utility Scripts
    ├── generate_data.py             # CLI generator
    ├── validate_data.py             # Validation tool
    ├── flatten_to_csv.py            # JSON → CSV converter
    └── api_example.py               # API usage examples
```

## Data Structure

### Customers Dataset
```json
{
  "cust_id": "C10001",
  "first_name": "Sarah",
  "last_name": "Johnson",
  "date_of_birth": "1995-03-15",
  "email": "sarah.j@email.com",
  "phone": "555-0123",
  "address": "123 Main St",
  "city": "San Francisco",
  "state": "CA",
  "zip_code": "94102",
  "customer_since": "2020-01-15",
  "customer_segment": "Young Professional",
  "credit_score": 720
}
```

### Accounts Dataset (nested under customer)
```json
{
  "account_id": "A10001",
  "cust_id": "C10001",
  "account_type": "Checking",
  "account_status": "Active",
  "open_date": "2020-01-15",
  "current_balance": 5420.50,
  "currency": "USD",
  "interest_rate": 0.01,
  "overdraft_limit": 500.00
}
```

### Transactions Dataset (nested under accounts)
```json
{
  "transaction_id": "T10001",
  "account_id": "A10001",
  "transaction_date": "2024-01-20",
  "transaction_time": "10:24:15",
  "transaction_type": "Debit",
  "transaction_category": "Groceries",
  "amount": -125.50,
  "merchant_name": "Whole Foods Market",
  "description": "Grocery purchase",
  "balance_after": 5420.50
}
```

## 🚀 How to Use This Template

There are **three ways** to generate banking datasets with this template:

### Method 1: Web UI (Best for beginners) 🌐
- **Guided 5-step wizard**
- Visual file browser
- Inline results preview
- No coding required

👉 **See [UI_USAGE_GUIDE.md](UI_USAGE_GUIDE.md)** for detailed steps

**Quick Summary:**
1. Open Web UI → Data Generator
2. Configure: Select "Custom" use case + "Freeform" workflow
3. Examples: Import `examples.json`
4. Prompt: Paste `custom_prompt.txt` + Add topics
5. Generate & Export

---

### Method 2: CLI Script (Best for automation) 🖥️
- **One-line command**
- Good for batch generation
- Repeatable workflows

👉 **See below for command examples**

**Quick Example:**
```bash
python generate_data.py --num-customers 10
```

---

### Method 3: Direct API (Best for integration) 🔧
- **Full programmatic control**
- Integrate into pipelines
- Custom workflows

👉 **See API examples below**

**Quick Example:**
```python
import requests, json
response = requests.post(
    "http://localhost:8000/api/v1/synthesize",
    json={...}
)
```

---

## Quick Start

### Option 1: Using Python Scripts (Recommended)

1. **Generate synthetic data:**
```bash
python generate_data.py --num-customers 10 --model claude-3-5-sonnet
```

2. **Evaluate generated data:**
```bash
python evaluate_data.py --input-file output/banking_data_20240126.json
```

### Option 2: Using API Directly

#### Generate Data with Custom Example

```python
import requests
import json

# Read the custom prompt
with open('custom_prompt.txt', 'r') as f:
    custom_prompt = f.read()

# Read example data
with open('examples.json', 'r') as f:
    examples = json.load(f)

# API request
response = requests.post(
    "http://localhost:8000/api/v1/synthesize",
    json={
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "inference_type": "aws_bedrock",
        "num_questions": 10,
        "technique": "freeform",
        "custom_prompt": custom_prompt,
        "example_custom": examples,
        "topics": [
            "Young Professional with multiple accounts",
            "Small Business owner",
            "Retiree with high net worth",
            "New customer with minimal history",
            "Customer with dormant accounts"
        ],
        "is_demo": True,
        "max_concurrent_topics": 5,
        "model_params": {
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 8192
        }
    }
)

result = response.json()
print(f"Generated {len(result['qa_pairs'])} customer records")
```

#### Generate Data with Example File Path

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/synthesize",
    json={
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "inference_type": "aws_bedrock",
        "num_questions": 5,
        "technique": "freeform",
        "custom_prompt": open('custom_prompt.txt').read(),
        "example_path": "examples/banking_multi_dataset/examples.json",
        "topics": ["High Net Worth Individuals", "Small Business Banking"],
        "is_demo": True
    }
)
```

### Option 3: Using Different Models

#### AWS Bedrock Claude
```python
request_data = {
    "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "inference_type": "aws_bedrock"
}
```

#### AWS Bedrock Llama
```python
request_data = {
    "model_id": "us.meta.llama3-2-90b-instruct-v1:0",
    "inference_type": "aws_bedrock"
}
```

#### Cloudera AI Inference (CAII)
```python
request_data = {
    "model_id": "your-model-id",
    "inference_type": "caii",
    "caii_endpoint": "https://your-caii-endpoint.cloudera.com"
}
```

#### OpenAI Compatible Endpoints
```python
request_data = {
    "model_id": "gpt-4",
    "inference_type": "openai_compatible",
    "openai_compatible_endpoint": "https://api.openai.com/v1"
}
```

## Suggested Topics for Data Generation

Use these topics to generate diverse banking scenarios:

**Customer Segments:**
- Young Professional with multiple accounts
- Small Business owner with high transaction volume
- Retiree with high net worth
- New customer with minimal history
- Family with joint accounts
- Student with basic checking account
- Freelancer with irregular income

**Account Patterns:**
- Customer with dormant accounts
- Multi-account holder (checking, savings, CD, money market)
- Business checking with frequent transactions
- Savings account with regular deposits
- Account with overdraft history

**Transaction Scenarios:**
- High frequency transaction account (20+ transactions/month)
- Low activity account (2-5 transactions/month)
- Salary and bill payment pattern
- Business revenue and expenses
- Investment and transfer patterns

## Data Validation Rules

The generated data follows these critical rules:

### Referential Integrity
- ✅ All `accounts.cust_id` → `customers.cust_id`
- ✅ All `transactions.account_id` → `accounts.account_id`
- ✅ No orphan records
- ✅ Unique IDs within each dataset

### Temporal Consistency
- ✅ `customer_since` ≤ `account.open_date`
- ✅ `account.open_date` ≤ `transaction.transaction_date`
- ✅ Transactions chronologically ordered per account

### Business Logic
- ✅ Savings accounts: balance ≥ 0
- ✅ Checking accounts: balance ≥ -overdraft_limit
- ✅ Closed accounts: balance = 0
- ✅ Interest rates match account types
- ✅ Credit scores: 300-850

## Post-Processing: Flatten to CSV

To convert the nested JSON structure to separate CSV files:

```python
python flatten_to_csv.py --input output/banking_data.json --output-dir output/csv/
```

This creates three files:
- `customers.csv` - One row per customer
- `accounts.csv` - One row per account
- `transactions.csv` - One row per transaction

## Evaluation

Evaluate the quality of generated data:

```python
import requests

with open('evaluation_prompt.txt', 'r') as f:
    eval_prompt = f.read()

response = requests.post(
    "http://localhost:8000/api/v1/evaluate",
    json={
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "inference_type": "aws_bedrock",
        "import_path": "output/banking_data_20240126.json",
        "import_type": "local",
        "custom_prompt": eval_prompt,
        "is_demo": True,
        "max_workers": 4
    }
)

evaluation_results = response.json()
print(f"Average Score: {evaluation_results['average_score']}")
```

## Example Output Structure

```json
{
  "customer": {
    "cust_id": "C10001",
    "first_name": "Sarah",
    ...
  },
  "accounts": [
    {
      "account_id": "A10001",
      "cust_id": "C10001",
      ...
    },
    {
      "account_id": "A10002",
      "cust_id": "C10001",
      ...
    }
  ],
  "transactions": [
    {
      "transaction_id": "T10001",
      "account_id": "A10001",
      ...
    },
    {
      "transaction_id": "T10002",
      "account_id": "A10001",
      ...
    }
  ]
}
```

## Extending the Template

### Add New Fields

Edit `custom_prompt.txt` to add new fields:

```
**DATASET 1: CUSTOMERS**
Fields:
- cust_id: ...
- ... (existing fields)
- loyalty_tier: One of ["Bronze", "Silver", "Gold", "Platinum"]  # NEW FIELD
- preferred_contact: One of ["Email", "Phone", "Mail"]            # NEW FIELD
```

Update `examples.json` with the new fields in all examples.

### Add New Datasets

To add a 4th dataset (e.g., Loans):

1. Add to `custom_prompt.txt`:
```
**DATASET 4: LOANS**
Fields:
- loan_id: Unique loan identifier (format: L10001, L10002, etc.)
- cust_id: Foreign key to customers.cust_id
- account_id: Foreign key to accounts.account_id (disbursement account)
- loan_type: One of ["Personal", "Auto", "Mortgage", "Student"]
...
```

2. Update examples with nested `loans` array
3. Update evaluation criteria

### Custom Business Rules

Modify `custom_prompt.txt` to add domain-specific rules:

```
**CONSISTENCY REQUIREMENTS:**

3. **Business Logic:**
   - Savings accounts cannot have negative balances
   - Mortgage loans must have loan_term >= 15 years          # CUSTOM RULE
   - High Net Worth customers must have total_balance > $250k # CUSTOM RULE
```

## Troubleshooting

### Issue: Foreign Key Violations
**Solution**: Check that `example_custom` or `example_path` contains examples with proper nesting. The LLM learns the referential structure from examples.

### Issue: Unrealistic Data
**Solution**: Add more specific constraints in `custom_prompt.txt` under "Business Logic" section.

### Issue: Inconsistent Formatting
**Solution**: Add explicit format requirements in the prompt:
```
- All dates must be in YYYY-MM-DD format
- All monetary values must have exactly 2 decimal places
- All IDs must follow the pattern (C|A|T)##### (e.g., C10001, A10234, T10999)
```

### Issue: Low Evaluation Scores
**Solution**:
1. Review evaluation output to identify specific violations
2. Update prompt to emphasize violated rules
3. Add more diverse examples showing correct patterns

## Use Cases

This template is ideal for:

- **Model Training**: Fine-tune LLMs on multi-table database queries
- **ETL Testing**: Generate test data for data pipeline development
- **Data Warehousing**: Create realistic fact and dimension tables
- **Database Tuning**: Generate data for query performance testing
- **Privacy-Compliant Testing**: Replace production data with synthetic data
- **Demo Environments**: Populate demo systems with realistic but fake data

## Contributing

To improve this template:

1. Add more example records to `examples.json` covering edge cases
2. Enhance `custom_prompt.txt` with additional validation rules
3. Update `evaluation_prompt.txt` with new quality checks
4. Share generated datasets that showcase interesting patterns

## License

This example project is part of the CAI AMP Synthetic Data Studio and follows the same license terms.

## Support

For issues or questions:
- Review the main project README
- Check the technical documentation in `/docs`
- Open an issue on GitHub: https://github.com/cloudera/CAI_AMP_Synthetic_Data_Studio/issues
