# Tableau Calculated Fields

Create each of these in Tableau via **Analysis → Create Calculated Field**.

---

## Core KPI Fields

### Total Employees
```
COUNT([Employee Id])
```

### Active Employees
```
COUNT(IF [Attrition] = 'No' THEN [Employee Id] END)
```

### Employees Who Left
```
COUNT(IF [Attrition] = 'Yes' THEN [Employee Id] END)
```

### Attrition Rate
```
COUNT(IF [Attrition] = 'Yes' THEN [Employee Id] END)
/
COUNT([Employee Id])
```
*Format as Percentage, 1 decimal place.*

### Avg Monthly Salary
```
AVG([Monthly Salary])
```

### Avg Annual Salary
```
AVG([Annual Salary])
```

### Avg Tenure (Years)
```
AVG([Years At Company])
```

---

## Dimension Bins & Labels

### Age Band
```
IF [Age] < 30      THEN 'Under 30'
ELSEIF [Age] < 40  THEN '30–39'
ELSEIF [Age] < 50  THEN '40–49'
ELSE '50+'
END
```
*Sort order: Under 30, 30–39, 40–49, 50+*

### Tenure Band
```
IF [Years At Company] < 2   THEN '0–1 Years'
ELSEIF [Years At Company] < 5  THEN '2–4 Years'
ELSEIF [Years At Company] < 10 THEN '5–9 Years'
ELSE '10+ Years'
END
```

### Salary Band
```
IF [Annual Salary] < 50000   THEN 'Under $50K'
ELSEIF [Annual Salary] < 75000  THEN '$50K–$75K'
ELSEIF [Annual Salary] < 100000 THEN '$75K–$100K'
ELSEIF [Annual Salary] < 150000 THEN '$100K–$150K'
ELSE '$150K+'
END
```

### Job Level Label
```
IF [Job Level] = 1 THEN 'Junior'
ELSEIF [Job Level] = 2 THEN 'Mid'
ELSEIF [Job Level] = 3 THEN 'Senior'
ELSEIF [Job Level] = 4 THEN 'Lead'
ELSE 'Executive'
END
```

### Performance Label
```
IF [Performance Rating] = 1 THEN '1 – Low'
ELSEIF [Performance Rating] = 2 THEN '2 – Good'
ELSEIF [Performance Rating] = 3 THEN '3 – Excellent'
ELSE '4 – Outstanding'
END
```

### Satisfaction Score (Composite)
```
AVG(
  ([Job Satisfaction] + [Environment Satisfaction] + [Work Life Balance])
  / 3.0
)
```
*Round to 2 decimals.*

---

## Risk & Analysis Fields

### High Attrition Risk Flag
```
IF  [Attrition] = 'Yes'
AND [Job Level] = 1
AND [Job Satisfaction] <= 2
THEN 'High Risk'
ELSEIF [Attrition] = 'Yes' THEN 'Churned'
ELSE 'Retained'
END
```

### Overtime Attrition Rate
```
COUNT(IF [Attrition] = 'Yes' AND [Overtime] = 'Yes' THEN [Employee Id] END)
/
COUNT(IF [Overtime] = 'Yes' THEN [Employee Id] END)
```

### Pay Equity Gap (Gender)
*Create a dual-axis view — no calculated field needed. Drag Gender to Color, Avg Annual Salary to Columns.*

### Salary vs Market (Deviation from Dept Avg)
```
[Annual Salary] - WINDOW_AVG(AVG([Annual Salary]))
```
*Use as a table calculation partitioned by Department.*
