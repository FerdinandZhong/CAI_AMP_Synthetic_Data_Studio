# Quick Start Guide - Banking Multi-Dataset

Get started with the Banking Multi-Dataset example in 5 minutes.

## Prerequisites

1. **Synthetic Data Studio running:**
   ```bash
   cd /path/to/CAI_AMP_Synthetic_Data_Studio
   python build/start_application.py
   ```

2. **AWS Credentials configured** (if using AWS Bedrock):
   ```bash
   export AWS_ACCESS_KEY_ID="your-key"
   export AWS_SECRET_ACCESS_KEY="your-secret"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

## 5-Minute Quick Start

### Method 1: Use the Helper Script (Easiest)

```bash
# Generate 10 customer records with default topics
python generate_data.py --num-customers 10

# Output: banking_data_TIMESTAMP.json
```

That's it! The script handles everything automatically.

### Method 2: Use the API Example

```bash
# Run the example script
python api_example.py

# Output: banking_data_output.json
```

### Method 3: Direct API Call (Most Control)

```python
import requests
import json

# Load the files
with open('custom_prompt.txt', 'r') as f:
    prompt = f.read()

with open('examples.json', 'r') as f:
    examples = json.load(f)

# Generate data
response = requests.post(
    "http://localhost:8000/api/v1/synthesize",
    json={
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "inference_type": "aws_bedrock",
        "num_questions": 10,
        "technique": "freeform",
        "custom_prompt": prompt,
        "example_custom": examples,
        "topics": [
            "Young Professional",
            "Small Business",
            "Retiree"
        ],
        "is_demo": True
    }
)

print(response.json())
```

## Next Steps

### 1. Validate Your Data

Check for referential integrity and business rule violations:

```bash
python validate_data.py --input banking_data_20240126.json --verbose
```

Expected output:
```
✅ All validation checks passed!

Statistics:
  Customers:    10
  Accounts:     25
  Transactions: 187
```

### 2. Flatten to CSV

Convert nested JSON to separate CSV files:

```bash
python flatten_to_csv.py --input banking_data_20240126.json --output-dir csv/
```

Output:
- `csv/customers.csv`
- `csv/accounts.csv`
- `csv/transactions.csv`

### 3. Inspect the Data

```bash
# Pretty print JSON
cat banking_data_20240126.json | jq '.[0]'

# View CSV files
head -20 csv/customers.csv
head -20 csv/accounts.csv
head -20 csv/transactions.csv
```

## Common Use Cases

### Generate Specific Customer Segments

```bash
python generate_data.py \
  --num-customers 20 \
  --topics "High Net Worth,Small Business,Young Professional"
```

### Use Different Models

```bash
# Claude Sonnet (highest quality)
python generate_data.py --num-customers 10 --model claude-3-5-sonnet

# Llama (faster, cost-effective)
python generate_data.py --num-customers 10 --model llama-3-90b
```

### Generate Large Datasets

```bash
# Generate 100 customers with diverse profiles
python generate_data.py \
  --num-customers 100 \
  --topics "$(cat topics.txt | grep -v '^#' | head -20 | tr '\n' ',')" \
  --output data/banking_large.json
```

## Understanding the Output

Each record represents one customer with nested accounts and transactions:

```json
{
  "customer": {
    "cust_id": "C10001",           // Primary key
    "first_name": "Sarah",
    "credit_score": 720,
    ...
  },
  "accounts": [
    {
      "account_id": "A10001",      // Primary key
      "cust_id": "C10001",         // Foreign key → customer
      "account_type": "Checking",
      "current_balance": 5420.50,
      ...
    }
  ],
  "transactions": [
    {
      "transaction_id": "T10001",  // Primary key
      "account_id": "A10001",      // Foreign key → account
      "amount": -125.50,
      ...
    }
  ]
}
```

## Troubleshooting

### Error: "Connection refused"
**Solution:** Make sure the Synthetic Data Studio server is running:
```bash
python build/start_application.py
```

### Error: "Authentication failed"
**Solution:** Check AWS credentials:
```bash
echo $AWS_ACCESS_KEY_ID
echo $AWS_DEFAULT_REGION
```

### Error: "Invalid custom_prompt"
**Solution:** Ensure you're in the `examples/banking_multi_dataset/` directory, or provide full paths:
```bash
cd examples/banking_multi_dataset/
python generate_data.py --num-customers 10
```

### Low Quality Data
**Solution:**
1. Run validation to identify issues:
   ```bash
   python validate_data.py --input your_data.json --verbose
   ```
2. Use Claude Sonnet for higher quality:
   ```bash
   python generate_data.py --model claude-3-5-sonnet
   ```
3. Review and enhance the `custom_prompt.txt` with more specific requirements

## Advanced Usage

### Customize Topics

Edit `topics.txt` or provide inline:

```bash
python generate_data.py \
  --num-customers 10 \
  --topics "Customer with mortgage loan,Customer with investment accounts,High frequency trader"
```

### Adjust Generation Temperature

```bash
# More creative/diverse (0.8-1.0)
python generate_data.py --num-customers 10 --temperature 0.9

# More consistent (0.0-0.4)
python generate_data.py --num-customers 10 --temperature 0.2
```

### Use Custom Inference Endpoints

For Cloudera AI Inference or OpenAI-compatible endpoints, edit `api_example.py` or `generate_data.py` to set:

```python
"inference_type": "caii",
"caii_endpoint": "https://your-endpoint.cloudera.com"
```

## Integration Examples

### Load into Pandas

```python
import pandas as pd
import json

# Load nested JSON
with open('banking_data.json', 'r') as f:
    data = json.load(f)

# Or load CSV
customers = pd.read_csv('csv/customers.csv')
accounts = pd.read_csv('csv/accounts.csv')
transactions = pd.read_csv('csv/transactions.csv')

# Join datasets
full_data = customers.merge(accounts, on='cust_id') \
                     .merge(transactions, on='account_id')

print(f"Total records: {len(full_data)}")
```

### Load into Database

```python
import sqlite3
import pandas as pd

# Load CSV files
customers = pd.read_csv('csv/customers.csv')
accounts = pd.read_csv('csv/accounts.csv')
transactions = pd.read_csv('csv/transactions.csv')

# Create SQLite database
conn = sqlite3.connect('banking.db')

# Load into tables
customers.to_sql('customers', conn, if_exists='replace', index=False)
accounts.to_sql('accounts', conn, if_exists='replace', index=False)
transactions.to_sql('transactions', conn, if_exists='replace', index=False)

# Query
result = pd.read_sql("""
    SELECT c.customer_segment, COUNT(DISTINCT c.cust_id) as num_customers,
           AVG(a.current_balance) as avg_balance
    FROM customers c
    JOIN accounts a ON c.cust_id = a.cust_id
    GROUP BY c.customer_segment
""", conn)

print(result)
```

## What's Next?

1. **Extend the template** - Add more fields or datasets (loans, credit cards)
2. **Create domain-specific versions** - Healthcare, retail, insurance
3. **Train ML models** - Use the data for credit scoring, fraud detection
4. **Build dashboards** - Visualize the synthetic data
5. **Test ETL pipelines** - Use as test data for data engineering

## Need Help?

- **Documentation:** See `README.md` for detailed information
- **Issues:** https://github.com/cloudera/CAI_AMP_Synthetic_Data_Studio/issues
- **Examples:** Review `api_example.py` for more code examples
