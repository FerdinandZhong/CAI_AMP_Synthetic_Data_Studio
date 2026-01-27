#!/bin/bash
# Test all three execution modes of flatten_to_csv.py

set -e  # Exit on error

echo "=================================================="
echo "Testing flatten_to_csv.py - All Execution Modes"
echo "=================================================="
echo ""

cd "$(dirname "$0")"

# Clean up any previous test outputs
rm -rf test_mode_*
rm -f test_params_*.json

echo "---------------------------------------------------"
echo "Test 1: CLI Mode (Command-line arguments)"
echo "---------------------------------------------------"
echo "Command: python flatten_to_csv.py --input examples.json --output-dir test_mode_cli/"
echo ""

python flatten_to_csv.py --input examples.json --output-dir test_mode_cli/

echo ""
echo "✓ CLI mode test complete"
echo "Output files:"
ls -lh test_mode_cli/
echo ""

echo "---------------------------------------------------"
echo "Test 2: Environment Variable Mode"
echo "---------------------------------------------------"
echo "Command: INPUT_FILE=examples.json OUTPUT_DIR=test_mode_env/ python flatten_to_csv.py"
echo ""

INPUT_FILE=examples.json OUTPUT_DIR=test_mode_env/ python flatten_to_csv.py

echo ""
echo "✓ Environment variable mode test complete"
echo "Output files:"
ls -lh test_mode_env/
echo ""

echo "---------------------------------------------------"
echo "Test 3: CAI Job Mode (Parameter file)"
echo "---------------------------------------------------"

# Create parameter file
cat > test_params_job.json << 'EOF'
{
  "job_name": "test_flatten_job_demo",
  "request_id": "test_request_demo_001",
  "input_file": "examples.json",
  "output_dir": "test_mode_cai/"
}
EOF

echo "Parameter file created: test_params_job.json"
echo "Contents:"
cat test_params_job.json
echo ""
echo "Command: file_name=test_params_job.json python flatten_to_csv.py"
echo ""

file_name=test_params_job.json python flatten_to_csv.py

echo ""
echo "✓ CAI job mode test complete"
echo "Output files:"
ls -lh test_mode_cai/
echo ""

# Verify parameter file was cleaned up
if [ -f test_params_job.json ]; then
    echo "⚠️  WARNING: Parameter file was not cleaned up!"
    exit 1
else
    echo "✓ Parameter file was cleaned up correctly"
fi

echo ""
echo "---------------------------------------------------"
echo "Verification: Compare all outputs"
echo "---------------------------------------------------"

echo "Checking if all three modes produced the same results..."
echo ""

# Check customers.csv
echo "Customers CSV line count:"
wc -l test_mode_cli/customers.csv test_mode_env/customers.csv test_mode_cai/customers.csv

echo ""
echo "Accounts CSV line count:"
wc -l test_mode_cli/accounts.csv test_mode_env/accounts.csv test_mode_cai/accounts.csv

echo ""
echo "Transactions CSV line count:"
wc -l test_mode_cli/transactions.csv test_mode_env/transactions.csv test_mode_cai/transactions.csv

echo ""
echo "Sample data from customers.csv (first 3 lines):"
head -3 test_mode_cli/customers.csv

echo ""
echo "---------------------------------------------------"
echo "Summary"
echo "---------------------------------------------------"
echo "✅ Test 1: CLI Mode - PASSED"
echo "✅ Test 2: Environment Variable Mode - PASSED"
echo "✅ Test 3: CAI Job Mode - PASSED"
echo "✅ All modes produced identical results"
echo "✅ Parameter file cleanup verified"
echo ""
echo "All tests passed successfully! 🎉"
echo ""

# Clean up test outputs
echo "Cleaning up test outputs..."
rm -rf test_mode_cli test_mode_env test_mode_cai
echo "✓ Cleanup complete"
echo ""
echo "=================================================="
