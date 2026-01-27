# Banking Multi-Dataset - UI Usage Guide

This guide explains how to generate banking datasets with referential integrity using the **Web UI** instead of the API/CLI.

---

## 🎯 Overview

The UI provides a **5-step wizard** for data generation:
1. **Configure** - Select template, model, and workflow type
2. **Examples** - Upload or manage example data
3. **Prompt** - Define generation prompt and parameters
4. **Summary** - Review all settings
5. **Finish** - Generate data and view results

---

## 📋 Prerequisites

1. **Synthetic Data Studio running:**
   ```bash
   cd /path/to/CAI_AMP_Synthetic_Data_Studio
   python build/start_application.py
   ```

2. **Access the UI:**
   - Open browser to: `http://localhost:8000` (or your configured URL)
   - Navigate to **"Data Generator"** or **"Generate Synthetic Data"**

3. **AWS Credentials configured** (if using AWS Bedrock):
   ```bash
   export AWS_ACCESS_KEY_ID="your-key"
   export AWS_SECRET_ACCESS_KEY="your-secret"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

---

## 🚀 Step-by-Step Instructions

### Step 1: Configure (Template & Model Selection)

1. **Click "Generate Synthetic Data"** or **"Data Generator"** in the UI

2. **Fill in the Configuration:**

   - **Display Name:** `Banking Multi-Dataset Test`
   - **Workflow Type:** Select **"Freeform Data Generation"** (automatically selected)
   - **Model Provider:** Select **"AWS Bedrock"**
   - **Model ID:** Select **"Claude 3.5 Haiku"** (or your preferred model)
     - Options: `us.anthropic.claude-3-5-haiku-20241022-v1:0`
     - Or: `us.anthropic.claude-3-5-sonnet-20241022-v2:0` for higher quality
   - **Use Case Template:** Select **"Custom"**
   - **Context:** **⚠️ LEAVE THIS EMPTY!** (see warning below)

3. **Click "Next"** to proceed to Examples step

> **⚠️ CRITICAL WARNING: Leave "Context" Field EMPTY**
>
> The **Context** field is for augmenting existing datasets, NOT for providing examples.
>
> - ❌ **DO NOT** select any files in Context
> - ❌ **DO NOT** upload examples.json as Context
> - ✅ **LEAVE IT COMPLETELY EMPTY**
>
> **Why?** If you fill in Context:
> - The "Seed Instructions" (topics) section will NOT appear in Step 3
> - You won't be able to add topics like "Young Professional", etc.
> - Generation will fail or produce incorrect results
>
> **What is Context for?**
> - Augmenting existing data with new fields (Custom Data Generation workflow)
> - Using PDFs as seed material
> - NOT for the Banking Multi-Dataset template!
>
> **See UI_TROUBLESHOOTING.md for details on this common issue.**

---

### Step 2: Examples (Upload Example Data)

This is the **critical step** where you upload the banking examples.

#### Option A: Upload via UI (Recommended)

1. **Click "Import"** button in the Examples section

2. **Navigate to the examples file:**
   - In the file browser, navigate to: `examples/banking_multi_dataset/`
   - Select: `examples.json`
   - Click "Select" or "Add"

3. **Verify examples loaded:**
   - You should see a table displaying the 3 customer examples
   - Each row shows nested customer, accounts, and transactions data
   - Columns will auto-detect from the JSON structure

#### Option B: Manual File Selection

If the file browser doesn't work:

1. Copy `examples.json` to a location accessible by the UI
2. Use the file selector to browse to that location
3. Select the file

#### Expected Format

The UI expects a **JSON array** of objects. Each object represents one customer with nested accounts and transactions:

```json
[
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
      }
    ],
    "transactions": [
      {
        "transaction_id": "T10001",
        "account_id": "A10001",
        ...
      }
    ]
  }
]
```

#### Troubleshooting Examples

- **404 Error / "File not found"**:
  - **Quick Fix:** Copy file to project root: `cp examples/banking_multi_dataset/examples.json .`
  - Then upload from root directory instead of subfolder
  - Or navigate FULLY into subdirectories: click `examples/` folder → `banking_multi_dataset/` folder → then select `examples.json`

- **"Invalid format"**: Verify the JSON is valid using `jq . examples.json`

- **"No examples shown"**: Check browser console for errors (F12)

**See UI_TROUBLESHOOTING.md for detailed solutions to file upload issues.**

4. **Click "Next"** to proceed to Prompt step

---

### Step 3: Prompt (Generation Instructions)

#### A. Custom Prompt

1. **Paste the custom prompt:**
   - Open `custom_prompt.txt` in a text editor
   - Copy the entire content (4,560 characters)
   - Paste into the **"Custom Prompt"** text area in the UI

   **OR** use the **AI-Assisted Prompt Generator:**
   - Click the "AI Generate Prompt" button (if available)
   - Paste a simplified instruction
   - Let the AI expand it

2. **Verify prompt appears correctly:**
   - Should show all dataset specifications
   - Should include referential integrity requirements
   - Should define all three datasets (Customers, Accounts, Transactions)

#### B. Seed Instructions (Topics)

> **✅ Seeds Section Should Now Be Visible!**
>
> If you followed Step 1 correctly and left the **Context field EMPTY**, the "Seed Instructions" section will appear here.
>
> **🚨 If you DON'T see "Seed Instructions":**
> - Go back to Step 1 (Configure)
> - Make sure Context field is completely EMPTY
> - Clear any files selected in Context
> - Then return to this step
>
> **See UI_TROUBLESHOOTING.md Issue #2 for details.**

1. **Add topics/seed instructions:**
   - Click **"Add Topic"** or use the dropdown
   - Select or add topics like:
     - `Young Professional with multiple accounts`
     - `Small Business owner`
     - `Retiree with high net worth`
     - `New customer with minimal history`
     - `Family with joint accounts`

   **Tips:**
   - You can add multiple topics
   - Each topic will generate separate customer records
   - Topics guide the AI to create diverse scenarios

2. **Or import topics from file:**
   - Click "Import Seeds" (if available)
   - Select `topics.txt`
   - Choose specific topics from the list

#### C. Model Parameters

Adjust model parameters (optional):

- **Temperature:** `0.7` (default, good balance)
  - Lower (0.0-0.4): More consistent, deterministic
  - Higher (0.8-1.0): More creative, diverse
- **Top P:** `1.0` (default)
- **Top K:** `150` (default)
- **Max Tokens:** `8192` (default)

#### D. Number of Questions

Set **"Number of Records"**:
- **For testing:** `5-10` records (demo mode, instant results)
- **For production:** `50-100+` records (batch mode, background job)

**Important:**
- **Demo Mode** (≤25 records): Results appear inline immediately
- **Batch Mode** (>25 records): Creates a background job, view in Jobs page

4. **Click "Next"** to proceed to Summary

---

### Step 4: Summary (Review Settings)

1. **Review all configurations:**
   - Display Name
   - Model and Provider
   - Use Case: Custom
   - Workflow Type: Freeform
   - Number of records
   - Topics selected
   - Examples loaded (should show count)
   - Custom prompt (preview available)

2. **Verify everything looks correct:**
   - Examples: Should show "3 examples loaded" or similar
   - Prompt: Should show custom banking prompt
   - Topics: Should list all selected topics

3. **Click "Generate"** or **"Next"** to start generation

---

### Step 5: Finish (Generate & View Results)

#### Generation Process

1. **Wait for generation:**
   - **Demo mode** (≤25): See a loading spinner, results appear in ~30-60 seconds
   - **Batch mode** (>25): Job is created, you'll see a link to the Jobs page

2. **View Results:**

   **For Demo Mode:**
   - Results appear as **tabs** (one per topic/seed)
   - Click on each tab to see generated customers for that topic
   - Data displayed in a table/grid format

   **For Batch Mode:**
   - Click "View Jobs" link
   - Find your job in the Jobs list
   - Wait for job to complete
   - Download or view results from job page

#### Understanding Results

Each generated record contains:
- **Customer data**: One customer profile
- **Accounts**: 1-5 accounts for that customer
- **Transactions**: 2-20 transactions across accounts

**Sample Output Structure:**
```json
{
  "customer": {
    "cust_id": "C10004",
    "first_name": "Jennifer",
    "last_name": "Williams",
    "credit_score": 750,
    ...
  },
  "accounts": [
    {
      "account_id": "A10007",
      "cust_id": "C10004",
      "account_type": "Checking",
      "current_balance": 3200.50,
      ...
    },
    {
      "account_id": "A10008",
      "cust_id": "C10004",
      "account_type": "Savings",
      "current_balance": 25000.00,
      ...
    }
  ],
  "transactions": [
    {
      "transaction_id": "T10010",
      "account_id": "A10007",
      "amount": -85.00,
      "transaction_category": "Groceries",
      ...
    },
    ...
  ]
}
```

#### Export Results

1. **Export to JSON:**
   - Click **"Export"** or **"Download"** button
   - Save as `banking_data_YYYYMMDD.json`

2. **View in Dataset Browser:**
   - Click **"View in Datasets"** link
   - Navigate to Datasets page
   - Find your dataset by display name

---

## 💾 Post-Generation: Validate & Process

After exporting the data from the UI:

### 1. Validate Data Quality

```bash
cd examples/banking_multi_dataset
python validate_data.py --input /path/to/exported_data.json --verbose
```

**Expected Output:**
```
✅ All validation checks passed!

Statistics:
  Customers:    10
  Accounts:     25
  Transactions: 187
```

### 2. Flatten to CSV

```bash
python flatten_to_csv.py --input /path/to/exported_data.json --output-dir csv/
```

**Output Files:**
- `csv/customers.csv`
- `csv/accounts.csv`
- `csv/transactions.csv`

### 3. Load into Database or Analysis Tool

```python
import pandas as pd

customers = pd.read_csv('csv/customers.csv')
accounts = pd.read_csv('csv/accounts.csv')
transactions = pd.read_csv('csv/transactions.csv')

# Verify referential integrity
print(f"Customers: {len(customers)}")
print(f"Accounts: {len(accounts)}")
print(f"Transactions: {len(transactions)}")

# Join datasets
full_data = customers.merge(accounts, on='cust_id') \
                     .merge(transactions, on='account_id')
print(f"Total joined records: {len(full_data)}")
```

---

## 🔧 Troubleshooting

### Issue: "Examples not loading"

**Cause:** File path or format issue

**Solutions:**
1. Verify `examples.json` is valid JSON: `jq . examples.json`
2. Check file is in accessible location
3. Try copying file to project root
4. Check browser console (F12) for errors

### Issue: "Invalid custom prompt"

**Cause:** Prompt too long or contains special characters

**Solutions:**
1. Verify prompt is plain text (no special encoding)
2. Check prompt length (should be ~4,500 characters)
3. Remove any HTML tags or special formatting
4. Try pasting in smaller chunks

### Issue: "Generation failed"

**Cause:** API error, model timeout, or invalid parameters

**Solutions:**
1. Check logs in terminal where server is running
2. Verify AWS credentials are valid
3. Try with fewer records (5 instead of 50)
4. Use Claude Haiku instead of Sonnet (faster)
5. Reduce temperature to 0.5 for more consistent results

### Issue: "Job stuck in 'Running' state"

**Cause:** Backend job hung or crashed

**Solutions:**
1. Check server logs for errors
2. Navigate to Jobs page and cancel job
3. Try generating smaller batch (10-15 records)
4. Restart the server if needed

### Issue: "Results missing foreign keys"

**Cause:** Model didn't follow example structure

**Solutions:**
1. Verify examples loaded correctly (Step 2)
2. Check custom prompt includes referential integrity requirements
3. Use more examples (add 1-2 more to examples.json)
4. Use Claude Sonnet for better quality
5. Increase temperature slightly (0.7 → 0.8)

---

## 📊 UI vs API Comparison

| Feature | UI | API/CLI |
|---------|-------|---------|
| **Ease of Use** | ✅ Guided wizard | ⚠️ Requires coding |
| **File Upload** | ✅ Visual browser | ⚠️ Manual paths |
| **Preview Results** | ✅ Inline tables | ❌ JSON only |
| **Batch Jobs** | ✅ Automatic | ⚠️ Manual monitoring |
| **Validation** | ⚠️ Manual post-export | ✅ Built-in script |
| **CSV Export** | ⚠️ Manual post-export | ✅ Built-in script |
| **Automation** | ❌ Manual process | ✅ Scriptable |
| **Best For** | Small datasets, testing | Large datasets, production |

---

## 💡 Tips for Best Results

### 1. Start Small
- Generate 5-10 records first to test
- Verify quality before scaling up
- Adjust prompt/parameters based on results

### 2. Use Good Examples
- Include diverse customer segments in examples
- Show different account combinations (1-5 accounts)
- Include various transaction patterns

### 3. Choose Right Model
- **Claude 3.5 Haiku**: Fast, good for testing, lower cost
- **Claude 3.5 Sonnet**: Higher quality, better consistency, slower
- **Llama 90B**: Fast, cost-effective, requires more examples

### 4. Optimize Topics
- Use specific, descriptive topics
- Vary customer segments to ensure diversity
- Aim for 3-5 topics for good variety

### 5. Monitor Results
- Check first few records immediately
- Verify referential integrity with validation script
- Adjust parameters if quality is low

---

## 🎯 Quick Reference

**File Locations:**
- Examples: `examples/banking_multi_dataset/examples.json`
- Custom Prompt: `examples/banking_multi_dataset/custom_prompt.txt`
- Topics: `examples/banking_multi_dataset/topics.txt`

**UI Steps:**
1. Configure → Select "Custom" + "Freeform"
2. Examples → Import `examples.json`
3. Prompt → Paste `custom_prompt.txt` + Add topics
4. Summary → Review
5. Finish → Generate & Export

**Post-Processing:**
```bash
# Validate
python validate_data.py --input exported_data.json

# Flatten
python flatten_to_csv.py --input exported_data.json

# Analyze
python -c "import pandas as pd; print(pd.read_csv('csv/customers.csv').info())"
```

---

## 📞 Need Help?

- **UI Issues**: Check browser console (F12 → Console tab)
- **Server Issues**: Check terminal logs where server is running
- **Data Quality**: Run validation script
- **Format Issues**: Verify JSON with `jq . examples.json`

---

**UI Version Tested:** React 18.3.1
**Last Updated:** 2026-01-26
**Compatible With:** Synthetic Data Studio v1.0+
