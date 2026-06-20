# HR Analytics Dashboard — Tableau Public

Workforce analytics built on a synthetic 5,000-employee dataset. Four Tableau dashboards covering executive headcount KPIs, attrition deep-dive, compensation equity, and employee wellbeing scores.

> **Tableau Public:** *(link once published)*

---

## Dashboards

| # | Dashboard | Key Question |
|---|-----------|-------------|
| 1 | Executive Overview | What is our current workforce health? |
| 2 | Attrition Analysis | Who is leaving, and why? |
| 3 | Compensation Analysis | Are we paying fairly and competitively? |
| 4 | Wellbeing & Performance | Where are engagement and performance risks? |

## Dataset

`data/hr_analytics.csv` — 5,000 synthetic employees, seed=42.

| Column | Type | Description |
|--------|------|-------------|
| employee_id | string | Unique ID |
| age | int | 22–60 |
| gender | string | Male / Female |
| marital_status | string | Single / Married / Divorced |
| education_level | string | High School → PhD |
| department | string | 7 departments |
| job_role | string | Role within department |
| job_level | int | 1 (Junior) → 5 (Executive) |
| hire_date | date | YYYY-MM-DD |
| years_at_company | int | 0–20 |
| years_in_current_role | int | |
| years_with_current_manager | int | |
| monthly_salary | int | USD |
| annual_salary | int | USD |
| performance_rating | int | 1–4 |
| job_satisfaction | int | 1–4 |
| environment_satisfaction | int | 1–4 |
| work_life_balance | int | 1–4 |
| overtime | string | Yes / No |
| business_travel | string | Non-Travel / Travel Rarely / Travel Frequently |
| distance_from_home | int | Miles, 1–29 |
| training_last_year | int | Sessions, 0–6 |
| num_companies_worked | int | Prior employers |
| attrition | string | Yes / No |

## Tech Stack

`Python` · `Pandas` · `NumPy` · `Tableau Public`

## Quick Start

```bash
pip install pandas numpy
python scripts/generate_data.py   # creates data/hr_analytics.csv
```

Then open Tableau Public → Connect to Text File → `hr_analytics.csv`

See `tableau/dashboard_spec.md` for the full build guide.
