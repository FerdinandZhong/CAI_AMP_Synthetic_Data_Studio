# Banking Data Evaluation Examples

This document provides 5 realistic examples of synthetic banking data evaluation for Singapore, ranging from Excellent (9/10) to Unusable (1/10).

## Example 1: Excellent - Score 9/10

**Quality Level:** Excellent - Professional grade synthetic data

**Key Strengths:**
- Perfect referential integrity (all IDs properly linked)
- All phone numbers valid Singapore format (8765-4321, 9123-4560, 6234-5678)
- All postal codes valid 6-digit format (628554, 018981, 238823)
- Nationalities correct (Singaporean, Malaysian, Indian)
- Branches properly specified (Marina Bay Branch, Orchard Branch, Jurong Branch)
- Temporal consistency perfect (transactions → accounts → customers)
- Singapore interest rates realistic (Checking 0.10%, Savings 1.25-1.50%, FD 3.75%)
- SGD currency consistent with 2 decimal places
- No duplicate IDs

**Minor Issues:**
- One customer email uses real domain 'gmail.com' (-1 point)

**Use Case:** Ready for production datasets, model training, reference implementations

---

## Example 2: Good - Score 7/10

**Quality Level:** Good - Usable with minor fixes

**Key Strengths:**
- Referential integrity maintained
- Phone numbers: 9456-7890, 8234-5678, 6789-1234 ✓
- Postal codes: 456789, 123456, 789012 ✓
- Nationalities: Singaporean, Thai, Filipino ✓
- Branches: Clementi Branch, Tampines Branch ✓
- Most temporal consistency correct
- No duplicate IDs

**Issues Found:**
- Credit score alignment: Customer with score 820 marked as 'Young Professional' (should be 650-750) (-1 point)
- Interest rate mismatch: Savings account at 2.5% (exceeds 2% limit) (-1 point)
- Balance calculation: One transaction's balance_after doesn't match cumulative (-1 point)

**Use Case:** Good for testing, minor cleanup required before production

---

## Example 3: Acceptable - Score 5/10

**Quality Level:** Acceptable - Usable with significant fixes

**Key Issues:**
- Phone format: One customer '91234567' missing dash (-1 point)
- Postal code: One entry '12345' only 5 digits (-1 point)
- Nationality: One entry 'European' not in approved list (-1 point)
- Branch: One account missing location (just 'Branch') (-1 point)
- **Temporal violation: Customer created 2023-01-15 but account opened 2022-06-01** (-2 points)
- Interest rate: Checking account at 0.8% (exceeds 0.25% limit) (-1 point)

**Strengths:**
- Most referential integrity maintained
- No duplicate IDs
- No orphan records
- SGD currency consistent
- Mostly valid Singapore data

**Use Case:** Development/testing only, requires cleanup before production

---

## Example 4: Poor - Score 3/10

**Quality Level:** Poor - Multiple serious violations

**Critical Issues:**
- **Referential integrity failures:**
  - Transaction T30005 references non-existent account A99999 (-4 points)
  - Account A30020 references non-existent customer C50001 (-4 points)

- **Format violations:**
  - Phone '555-1234' (US format, not Singapore) (-1 point)
  - Postal code 'SG123456' (contains letters) (-1 point)
  - Nationality 'British' (not approved) (-1 point)

- **Temporal issues:**
  - Account opened 2015-09-20, customer created 2020-03-15 (4.5 year gap) (-2 points)

- **Business logic violations:**
  - Savings account with -350.50 SGD balance (-1 point)
  - Fixed Deposit at 5.2% (exceeds 4.5% max) (-1 point)

- **Data quality:**
  - 3 accounts missing branch field
  - Real email: john.smith@example.com

**Use Case:** NOT suitable for use - critical corrections needed

---

## Example 5: Unusable - Score 1/10

**Quality Level:** Unusable - Complete regeneration required

**Catastrophic Issues:**

**Referential Integrity Collapse:**
- 15+ transactions reference non-existent accounts (-60+ points)
- 8 accounts reference non-existent customers (-32+ points)
- Duplicate transaction IDs (T40001 appears 3 times) (-4 points)
- Duplicate account IDs (A40005 appears twice) (-4 points)

**Privacy Violations:**
- Real person names: 'John Smith', 'Mary Johnson' (-2 points)
- Real merchant names: 'DBS Bank', 'OCBC' (-2 points)
- Real addresses: 'Blk 123 Tiong Bahru Road' with real postal '160123' (-2 points)

**Format Failures:**
- ALL phone numbers missing dashes (91234567 not XXXX-XXXX)
- ALL postal codes wrong format (letters or incorrect)
- Invalid nationalities: 'American', 'European'

**Temporal Disasters:**
- Multiple accounts predate customer creation by years
- Transactions across entire dataset dated before account opening

**Business Logic:**
- Savings accounts frequently negative
- Checking accounts 50,000 SGD over limit
- Closed accounts with large balances

**Currency:**
- Mix of SGD and USD without consistency

**Use Case:** Completely unusable - delete and regenerate

---

## Evaluation Scoring Reference

| Score | Grade | Meaning | Action |
|-------|-------|---------|--------|
| 9-10 | Excellent | Production-ready | Deploy directly |
| 7-8 | Good | Minor fixes needed | Minor cleanup then deploy |
| 5-6 | Acceptable | Significant fixes needed | Development/testing use only |
| 3-4 | Poor | Critical issues present | Requires major rework |
| 1-2 | Unusable | Multiple catastrophic failures | Reject and regenerate |

---

## Common Mistakes to Avoid in Evaluation

### ❌ FALSE NEGATIVES (Don't flag these)
- Phone '9123-4560' ✓ (valid - starts with 9)
- Phone '8765-4321' ✓ (valid - starts with 8)
- Phone '6234-5678' ✓ (valid - starts with 6)
- Postal '589123' ✓ (valid - 6 digits)
- Postal '018981' ✓ (valid - 6 digits)
- Nationality 'Malaysian' ✓ (in approved list)
- Nationality 'Indian' ✓ (in approved list)

### ✅ REAL VIOLATIONS (Flag these)
- Phone '555-0123' ✗ (starts with 5, not 6/8/9)
- Phone '91234567' ✗ (missing dash)
- Postal '12345' ✗ (only 5 digits)
- Postal 'ABC1234' ✗ (contains letters)
- Nationality 'British' ✗ (not approved)
- Nationality 'American' ✗ (not approved)

---

## Tips for Writing Good Evaluations

1. **Always check referential integrity first** - This is the most critical aspect
2. **Verify format rules carefully** - Use the valid/invalid examples as reference
3. **Check temporal consistency** - Dates must flow logically
4. **Validate business rules** - Interest rates, balances, account types must align
5. **Group violations by category** - Make it clear what type each violation is
6. **Provide specific examples** - "Account A10005" is better than "an account"
7. **Explain point deductions** - Why was this -1 vs -4 points?
8. **Note positive aspects** - Acknowledge what's done well, not just problems

---

## Example Evaluation Template

```
Score: [X]/10

**Strengths:**
- [List 3-5 positive aspects]

**Issues Found:**
1. **Referential Integrity** (-X points)
   - [Specific examples]
2. **Format Violations** (-X points)
   - [Specific examples]
3. **Business Logic** (-X points)
   - [Specific examples]
4. **Temporal Issues** (-X points)
   - [Specific examples]

**Overall Assessment:**
[Summary sentence about usability and recommended action]
```
