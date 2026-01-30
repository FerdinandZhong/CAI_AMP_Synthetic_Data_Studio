# Text to SQL Evaluation Examples

This document provides 6 detailed examples of SQL query evaluation for training data, ranging from Excellent (9/10) to Unusable (1/10). These examples demonstrate how to assess whether a question-query pair is suitable for training.

## Schema Reference

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2)
);

CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT,
    budget DECIMAL(15,2)
);
```

---

## Example 1: Excellent - Score 9/10

**Question:** Find all employees from the Engineering department who earn more than 60000

**Query:**
```sql
SELECT *
FROM employees
WHERE department = 'Engineering' AND salary > 60000;
```

**Quality Level:** Excellent - Production-grade training example

**Key Strengths:**
- Question is clear and specific (Engineering department, salary threshold 60000)
- Query directly answers the question without ambiguity
- Schema validity: employees table exists, both columns exist
- Syntax is correct with proper WHERE clause using AND operator
- Teaches fundamental SQL pattern: filtered SELECT with multiple conditions
- SELECT * is acceptable here for comprehensive employee information

**Pattern Demonstrated:**
- Basic SELECT/WHERE with AND conditions
- Foundation for all subsequent SQL learning

**Use Case:** Production training dataset, foundational SQL curriculum

---

## Example 2: Good - Score 7/10

**Question:** What is the average salary for each department? Show department name and average salary

**Query:**
```sql
SELECT d.name, AVG(e.salary) as avg_salary
FROM employees e
JOIN departments d ON e.department = d.name
GROUP BY d.name;
```

**Quality Level:** Good - Educationally valuable with minor design note

**Key Strengths:**
- Question is specific about expected outputs (department name, average salary)
- Query demonstrates important patterns: JOIN and GROUP BY with aggregation
- Schema references are valid
- Uses table aliases (e, d) for clarity
- Syntax is correct
- Teaches multi-table queries

**Minor Design Issue:**
- JOIN condition `e.department = d.name` assumes department stores name strings
- Ideally, employees would have `department_id` as foreign key
- This works for training but represents a schema assumption rather than best practice

**Pattern Demonstrated:**
- INNER JOIN between two tables
- GROUP BY with aggregate function (AVG)
- Column aliasing for readability
- Multi-table query construction

**Use Case:** Intermediate SQL training, JOIN and aggregation patterns

---

## Example 3: Acceptable - Score 5/10

**Question:** Get employees

**Query:**
```sql
SELECT name, salary, department
FROM employees
WHERE department IN ('Sales', 'Marketing')
ORDER BY salary DESC;
```

**Quality Level:** Acceptable - Works but has clarity issues

**Key Strengths:**
- Query syntax is correct
- Schema references are valid
- Demonstrates IN operator and ORDER BY clause
- Teaches multiple patterns in one query

**Critical Issue - Misalignment:**
- Question is too vague: "Get employees" doesn't specify which employees
- Query adds filtering criteria (Sales/Marketing departments) that aren't in the question
- This creates training ambiguity: Is the model learning to infer missing criteria or to match questions?

**Pattern Demonstrated:**
- IN operator for multiple values
- WHERE clause with operator
- ORDER BY with DESC sorting

**Use Case:** Training only with caution - demonstrates patterns but unclear question-query relationship. Better practice would be explicit question: "Find employees in Sales or Marketing departments, sorted by salary"

---

## Example 4: Poor - Score 3/10

**Question:** Find managers and their average employee salary

**Query:**
```sql
SELECT m.name, AVG(e.salary)
FROM departments m
JOIN employees e ON m.id = e.manager_id
GROUP BY m.id;
```

**Quality Level:** Poor - Critical schema validity issue

**Critical Issues:**
- Query references `e.manager_id` column which doesn't exist in employees table
- The employees schema only has: id, name, department, salary
- manager_id exists in departments table, not employees
- Query will fail at execution with column not found error

**Schema Analysis:**
- Managers are identified in departments table (manager_id column)
- Employees don't have a manager_id field
- This represents a misunderstanding of the schema structure

**Pattern Attempted:**
- JOIN between managers and employees
- GROUP BY with aggregation
- (Patterns are conceptually sound but implementation is broken)

**Use Case:** NOT suitable for training - teaches incorrect schema understanding and won't execute

---

## Example 5: Unusable - Score 1/10

**Question:** Get employee data

**Query:**
```sql
SELCT name, salary FORM employees WHERE department = 'IT';
```

**Quality Level:** Unusable - Multiple syntax errors

**Critical Issues:**
- Syntax error: `SELCT` instead of `SELECT`
- Syntax error: `FORM` instead of `FROM`
- Query will not execute due to these typos
- Question is vague ("Get employee data" without specifics)

**Schema Assessment:**
- Tables and columns referenced are correct IF syntax were fixed
- But syntax errors prevent any execution

**Use Case:** Completely unusable - delete and regenerate. Teaches how NOT to write SQL

---

## Example 6: Excellent Advanced - Score 9/10

**Question:** Show department names with their total budget and number of employees in that department

**Query:**
```sql
SELECT d.name, d.budget, COUNT(e.id) as employee_count
FROM departments d
LEFT JOIN employees e ON d.name = e.department
GROUP BY d.id, d.name, d.budget;
```

**Quality Level:** Excellent - Advanced training example

**Key Strengths:**
- Question is specific and lists three exact outputs (department names, budgets, employee counts)
- Query implements exactly what's requested
- Demonstrates advanced patterns: LEFT JOIN (important distinction from INNER JOIN)
- LEFT JOIN ensures all departments included even without employees
- Proper use of COUNT for aggregation
- GROUP BY uses multiple columns correctly
- Uses table aliases for clarity
- Syntax is perfect

**Advanced Concepts:**
- LEFT JOIN semantics: preserves all rows from left table
- When to use LEFT vs INNER JOIN
- COUNT with primary key (COUNT(e.id) versus COUNT(*))
- Defensive GROUP BY including all selected non-aggregate columns

**Pattern Demonstrated:**
- Advanced JOIN patterns
- Multi-column GROUP BY
- COUNT aggregation (vs SUM/AVG)
- Handling nulls in aggregate functions

**Use Case:** Advanced SQL training, production datasets, interview preparation

---

## Evaluation Scoring Reference

| Score | Grade | Meaning | Training Suitability |
|-------|-------|---------|-----|
| 9-10 | Excellent | Perfect training data | Ideal - use in curriculum |
| 7-8 | Good | Minor issues only | Good - educationally sound |
| 5-6 | Acceptable | Some clarity issues | Acceptable - use with caveats |
| 3-4 | Poor | Schema/logic errors | Poor - requires major fix |
| 1-2 | Unusable | Syntax or critical errors | Reject - regenerate |

---

## Evaluation Checklist

When evaluating a question-query pair, check in this order:

### 1. Schema Validity (Critical)
- [ ] Do all table names exist?
- [ ] Do all column names exist in their respective tables?
- [ ] Are JOINs using valid relationships?
- [ ] Are data types used appropriately?

**Scoring:** -4 points per critical schema error

### 2. Question-Query Alignment (Critical)
- [ ] Does the query answer the question asked?
- [ ] Is the question unambiguous?
- [ ] Does the query return all required information?
- [ ] Does the query over-select unnecessary columns?

**Scoring:** -4 points if misaligned, -2 for ambiguity

### 3. SQL Correctness (Critical)
- [ ] Is the syntax correct (no typos, valid keywords)?
- [ ] Are GROUP BY columns sufficient?
- [ ] Are aggregate functions used correctly?
- [ ] Are column references unambiguous?

**Scoring:** -4 for syntax errors, -2 for logic errors, -1 for ambiguity

### 4. Educational Value (Learning)
- [ ] What SQL patterns does this teach?
- [ ] Is it appropriate for the skill level?
- [ ] Does it avoid unnecessary complexity?
- [ ] Does it demonstrate best practices?

### 5. Clarity & Simplicity (Pedagogical)
- [ ] Is the question clear and unambiguous?
- [ ] Is the query straightforward and readable?
- [ ] Would a student understand the intent?

---

## Common Mistakes in Evaluation

### ❌ FALSE NEGATIVES (Don't flag these)

**Schema Assumptions:**
- Using string-based JOINs (e.g., `ON e.department = d.name`) is acceptable if it works with the schema ✓
- SELECT * is fine for simple training queries ✓
- Using aliases (e, d) is good practice, not a violation ✓

**Advanced Patterns:**
- LEFT JOIN producing NULLs is intentional, not an error ✓
- COUNT(e.id) vs COUNT(*) both acceptable ✓
- Including extra columns in GROUP BY is defensive SQL ✓

### ✅ REAL VIOLATIONS (Flag these)

**Schema Errors:**
- Referencing non-existent tables ✗
- Referencing non-existent columns ✗
- Invalid JOIN relationships ✗

**Syntax Errors:**
- Misspelled keywords (SELCT, FORM, etc) ✗
- Unmatched parentheses ✗
- Missing commas in SELECT list ✗

**Alignment Issues:**
- Question asks for X but query returns Y ✗
- Vague questions without specificity ✗
- Queries that add unstated assumptions ✗

---

## Tips for Writing Good Training Examples

1. **Start with schema-valid concepts** - Understand the table structure first
2. **Write clear questions** - Be specific about what data is requested
3. **Match question to query** - Query should directly answer the question
4. **Teach one pattern well** - Examples should have clear pedagogical focus
5. **Avoid unnecessary complexity** - Basic patterns should be simple
6. **Use proper formatting** - Consistent indentation and capitalization
7. **Include aliases** - Make multi-table queries readable
8. **Comment if needed** - Clarify non-obvious logic

---

## Example Evaluation Template

```json
{
  "id": "example_name",
  "score": X,
  "quality": "[Excellent/Good/Acceptable/Poor/Unusable]",
  "question": "...",
  "query": "...",
  "validity": "[Schema assessment]",
  "question_alignment": "[Does query match question?]",
  "patterns": "[SQL patterns taught]",
  "issues": "[Any problems found]",
  "justification": "[Explanation of score]"
}
```
