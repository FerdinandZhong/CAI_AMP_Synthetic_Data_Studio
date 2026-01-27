# End-to-End Banking Pipeline Guide

Complete pipeline for synthetic banking data generation, validation, and processing.

## Pipeline Stages

1. **Data Validation** - Check referential integrity and data quality
2. **CSV Flattening** - Convert nested JSON to flat CSV files
3. **Results Summary** - Generate comprehensive report

## Usage Modes

### Mode 1: CAI Job (Cloudera Environment)

Create a parameters JSON file:

```bash
cat > job_params.json << 'EOF'
{
  "job_name": "banking_pipeline_run",
  "request_id": "req_12345",
  "input_file": "data/banking_data.json",
  "output_dir": "output/results",
  "verbose": true
}
EOF
```

Run as CAI job:

```bash
file_name=job_params.json python end_to_end_pipeline.py
```

### Mode 2: Environment Variables

```bash
export INPUT_FILE="data/banking_data.json"
export OUTPUT_DIR="output/results"
python end_to_end_pipeline.py
```

### Mode 3: Command-Line Arguments

```bash
python end_to_end_pipeline.py \
  --input data/banking_data.json \
  --output output/results \
  --verbose
```

### Mode 4: IPython/Jupyter Notebook

```python
from end_to_end_pipeline import run_pipeline

result = run_pipeline(
    input_file="data/banking_data.json",
    output_dir="output/results",
    verbose=True
)

print(result)
```

## Input Data Format

The pipeline expects a JSON file with nested banking data:

```json
[
  {
    "customer": {
      "cust_id": "C001",
      "name": "John Doe",
      "email": "john@example.com",
      ...
    },
    "accounts": [
      {
        "account_id": "A001",
        "cust_id": "C001",
        "account_type": "Checking",
        ...
      }
    ],
    "transactions": [
      {
        "transaction_id": "T001",
        "account_id": "A001",
        "transaction_date": "2024-01-15",
        ...
      }
    ]
  }
]
```

## Output Files

The pipeline creates:

```
output/
├── csv/
│   ├── customers.csv      # Flattened customer records
│   ├── accounts.csv       # Flattened account records
│   └── transactions.csv   # Flattened transaction records
└── pipeline_results.json  # Detailed validation and stats
```

## Output Format

### `pipeline_results.json`

```json
{
  "timestamp": "2024-01-20T15:30:45.123456",
  "input_file": "data/banking_data.json",
  "output_dir": "output/results",
  "stages": {
    "validation": {
      "passed": true,
      "errors": 0,
      "warnings": 0,
      "stats": {
        "customers": 100,
        "accounts": 350,
        "transactions": 2500
      },
      "error_details": []
    },
    "flatten": {
      "customers": "output/results/csv/customers.csv",
      "accounts": "output/results/csv/accounts.csv",
      "transactions": "output/results/csv/transactions.csv",
      "stats": {
        "customers": 100,
        "accounts": 350,
        "transactions": 2500
      }
    }
  }
}
```

## Validation Checks

The pipeline validates:

1. **Referential Integrity**
   - Account `cust_id` references valid customers
   - Transaction `account_id` references valid accounts
   - No orphan records

2. **Data Presence**
   - Required fields present
   - Valid ID formats

3. **Data Consistency**
   - Account belongs to correct customer
   - Transactions belong to correct accounts

## Example: Complete Workflow

```bash
# 1. Use existing test data
cd examples/banking_multi_dataset

# 2. Create job parameters
cat > job_params.json << 'EOF'
{
  "job_name": "banking_pipeline_demo",
  "request_id": "demo_001",
  "input_file": "examples_flat.json",
  "output_dir": "pipeline_output",
  "verbose": true
}
EOF

# 3. Run the pipeline
file_name=job_params.json python end_to_end_pipeline.py

# 4. Check results
cat pipeline_output/pipeline_results.json | jq .

# 5. Review CSV files
head pipeline_output/csv/customers.csv
head pipeline_output/csv/accounts.csv
```

## Integration with CAI Jobs

To integrate with Cloudera's CAI job system:

```yaml
# In cai_job_config.yaml
jobs:
  banking_pipeline:
    name: "Banking Multi-Dataset Pipeline"
    script: "examples/banking_multi_dataset/end_to_end_pipeline.py"
    kernel: "python3"
    cpu: 4
    memory: 16
    timeout: 1800
```

## Troubleshooting

### Issue: "file_name environment variable not set for CAI job"

**Solution:** Set the `file_name` environment variable or run without CAI job mode:

```bash
python end_to_end_pipeline.py --input data.json --output output/
```

### Issue: "Input file not found"

**Solution:** Provide absolute or correct relative path:

```bash
python end_to_end_pipeline.py --input /absolute/path/data.json
```

### Issue: "Validation errors found"

**Solution:** Check `pipeline_results.json` for `error_details`:

```bash
cat pipeline_output/pipeline_results.json | jq '.stages.validation.error_details'
```

## Performance

- **Validation**: O(n) where n = total records
- **CSV Flattening**: O(n)
- **Total Time**: Scales linearly with data size

For 1000 customer records (3000+ accounts/transactions):
- Typical runtime: 2-5 seconds
- Memory usage: ~100-200 MB

## Next Steps

After running the pipeline:

1. **Review Results**: Check `pipeline_results.json`
2. **Analyze CSV Data**: Load into pandas for analysis
3. **Evaluate Quality**: Use `evaluation_prompt.txt` criteria
4. **Iterate**: Adjust generation parameters and re-run

```python
import pandas as pd

customers = pd.read_csv('pipeline_output/csv/customers.csv')
accounts = pd.read_csv('pipeline_output/csv/accounts.csv')
transactions = pd.read_csv('pipeline_output/csv/transactions.csv')

# Merge and analyze
merged = customers.merge(accounts, on='cust_id').merge(transactions, on='account_id')
print(merged.describe())
```
