"""Generate a synthetic HR analytics dataset (5,000 employees)."""
import os
import numpy as np
import pandas as pd

RNG      = np.random.default_rng(42)
N        = 5_000
DATA_DIR = 'data'

DEPT_ROLES = {
    'Sales':                  ['Sales Executive', 'Sales Representative', 'Sales Manager'],
    'Research & Development': ['Research Scientist', 'Lab Technician', 'R&D Manager', 'Research Director'],
    'Human Resources':        ['HR Representative', 'HR Manager', 'HR Director'],
    'Finance':                ['Financial Analyst', 'Finance Manager', 'Finance Director'],
    'Technology':             ['Software Engineer', 'Senior Engineer', 'Tech Lead', 'Engineering Manager'],
    'Marketing':              ['Marketing Analyst', 'Marketing Manager', 'VP Marketing'],
    'Operations':             ['Operations Analyst', 'Operations Manager', 'VP Operations'],
}

DEPT_BASE_SALARY = {
    'Sales': 55_000, 'Research & Development': 70_000, 'Human Resources': 52_000,
    'Finance': 72_000, 'Technology': 80_000, 'Marketing': 60_000, 'Operations': 58_000,
}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Demographics
    dept_arr    = RNG.choice(list(DEPT_ROLES), N, p=[0.22, 0.30, 0.08, 0.12, 0.15, 0.08, 0.05])
    age         = RNG.integers(22, 61, N)
    gender      = RNG.choice(['Male', 'Female'], N, p=[0.52, 0.48])
    marital     = RNG.choice(['Single', 'Married', 'Divorced'], N, p=[0.32, 0.55, 0.13])
    education   = RNG.choice(
        ['High School', 'Associate', 'Bachelor', 'Master', 'PhD'],
        N, p=[0.08, 0.12, 0.45, 0.28, 0.07],
    )

    # Job attributes
    job_level           = np.clip(((age - 22) // 8) + RNG.integers(0, 2, N), 1, 5)
    years_at_company    = np.clip(RNG.integers(0, 21, N), 0, age - 22)
    years_in_role       = np.clip(RNG.integers(0, years_at_company + 1), 0, years_at_company)
    years_with_mgr      = np.clip(RNG.integers(0, years_in_role + 1), 0, years_in_role)
    num_companies       = RNG.integers(0, 10, N)
    training            = RNG.integers(0, 7, N)

    # Compensation
    dept_base     = np.array([DEPT_BASE_SALARY[d] for d in dept_arr])
    annual_salary = (
        (dept_base + job_level * 8_000 + years_at_company * 500)
        * (1 + RNG.normal(0, 0.08, N))
    ).clip(30_000, 300_000).round(-2).astype(int)
    monthly_salary = (annual_salary / 12).round(0).astype(int)

    # Satisfaction & performance (1-4 scale)
    job_sat  = RNG.integers(1, 5, N)
    env_sat  = RNG.integers(1, 5, N)
    wlb      = RNG.integers(1, 5, N)
    perf     = RNG.choice([1, 2, 3, 4], N, p=[0.02, 0.12, 0.60, 0.26])

    # Work conditions
    overtime = RNG.choice(['Yes', 'No'], N, p=[0.28, 0.72])
    travel   = RNG.choice(
        ['Non-Travel', 'Travel Rarely', 'Travel Frequently'],
        N, p=[0.15, 0.70, 0.15],
    )
    dist_home = RNG.integers(1, 30, N)

    # Attrition — correlated with known risk factors
    attrition_prob = (
        0.07
        + (job_level == 1)                      * 0.14
        + (job_sat  <= 2)                        * 0.12
        + (overtime == 'Yes')                    * 0.10
        + (travel   == 'Travel Frequently')      * 0.08
        + (wlb      <= 2)                        * 0.08
        + (years_at_company <= 2)               * 0.10
        + (dist_home > 20)                       * 0.04
        + (num_companies > 5)                    * 0.05
        + RNG.normal(0, 0.04, N)
    ).clip(0, 0.95)
    attrition = np.where(RNG.uniform(0, 1, N) < attrition_prob, 'Yes', 'No')

    # Hire date
    hire_year  = 2024 - years_at_company
    hire_month = RNG.integers(1, 13, N)
    hire_date  = [f'{y}-{m:02d}-01' for y, m in zip(hire_year, hire_month)]

    job_roles = [RNG.choice(DEPT_ROLES[d]) for d in dept_arr]

    df = pd.DataFrame({
        'employee_id':               [f'EMP{i:05d}' for i in range(1, N + 1)],
        'age':                       age,
        'gender':                    gender,
        'marital_status':            marital,
        'education_level':           education,
        'department':                dept_arr,
        'job_role':                  job_roles,
        'job_level':                 job_level,
        'hire_date':                 hire_date,
        'years_at_company':          years_at_company,
        'years_in_current_role':     years_in_role,
        'years_with_current_manager': years_with_mgr,
        'monthly_salary':            monthly_salary,
        'annual_salary':             annual_salary,
        'performance_rating':        perf,
        'job_satisfaction':          job_sat,
        'environment_satisfaction':  env_sat,
        'work_life_balance':         wlb,
        'overtime':                  overtime,
        'business_travel':           travel,
        'distance_from_home':        dist_home,
        'training_last_year':        training,
        'num_companies_worked':      num_companies,
        'attrition':                 attrition,
    })

    df.to_csv(f'{DATA_DIR}/hr_analytics.csv', index=False)
    rate = (attrition == 'Yes').mean() * 100
    print(f'Generated {N:,} employees | Attrition rate: {rate:.1f}%')
    print(df.groupby('department')['attrition'].apply(lambda x: f'{(x=="Yes").mean()*100:.1f}%'))


if __name__ == '__main__':
    main()
