# Tableau Dashboard Build Guide

Four dashboards, each 1200×800 px. Use a consistent colour palette:
- **Primary blue**: #1565C0
- **Attrition red**: #E53935
- **Safe green**: #43A047
- **Warning amber**: #FB8C00
- **Background**: #F5F7FA

---

## Dashboard 1 — Executive Overview

**Purpose**: Single-screen snapshot of current workforce health for C-suite.

### KPI Row (4 BANs across the top)
| Metric | Calculated Field | Format |
|--------|-----------------|--------|
| Total Employees | `COUNT([Employee Id])` | Integer, comma |
| Active Employees | `Active Employees` | Integer, comma |
| Overall Attrition Rate | `Attrition Rate` | %, 1 dp |
| Avg Annual Salary | `AVG([Annual Salary])` | $, 0 dp |

**How to build a BAN**: Sheet → drag measure to Text mark → adjust font size to 36pt bold → remove headers/gridlines.

### Chart 1 — Headcount by Department (Horizontal Bar)
- **Rows**: Department
- **Columns**: COUNT([Employee Id])
- **Color**: Department
- **Sort**: Descending by headcount
- **Label**: On bars

### Chart 2 — Age Distribution by Gender (Grouped Bar / Histogram)
- **Columns**: Age Band (calculated field)
- **Rows**: COUNT([Employee Id])
- **Color**: Gender (Male=#2196F3, Female=#E91E63)
- **Mark type**: Bar, side-by-side (Marks → Color → separate)
- **Sort**: Under 30 → 30–39 → 40–49 → 50+

### Chart 3 — Headcount by Job Level (Donut Chart)
- **Rows**: 2× AVG(0) → dual axis → synchronise
- **Color**: Job Level Label
- **Size**: CNT([Employee Id]) on outer ring, set inner ring size to 90%
- **Label**: Job Level + % of total

### Chart 4 — Department × Gender Heatmap
- **Rows**: Department
- **Columns**: Gender
- **Color**: COUNT([Employee Id]) → Blue sequential
- **Text**: COUNT([Employee Id])
- **Mark type**: Square

### Filters (global, applied to all sheets on this dashboard)
- Department (multi-select)
- Gender
- Education Level

---

## Dashboard 2 — Attrition Analysis

**Purpose**: Identify WHO is leaving and WHAT drives it.

### KPI Row
| Metric | Note |
|--------|------|
| Employees Left | `Employees Who Left` |
| Attrition Rate | `Attrition Rate` — colour red if > 15% |
| Avg Tenure of Leavers | `AVG([Years At Company])` filtered to Attrition=Yes |
| Est. Annual Cost | `Employees Who Left * AVG([Annual Salary]) * 0.5` |

### Chart 1 — Attrition Rate by Department (Bar)
- **Rows**: Department
- **Columns**: Attrition Rate (calculated field)
- **Color**: Red–Green diverging on Attrition Rate, midpoint 15%
- **Reference line**: Add average line
- **Sort**: Descending

### Chart 2 — Attrition by Tenure Band (Bar)
- **Rows**: Tenure Band
- **Columns**: Attrition Rate
- **Color**: Attrition Rate (same diverging)
- **Insight to highlight**: 0–1 years almost always highest

### Chart 3 — Attrition by Job Level (Line or Lollipop)
- **Columns**: Job Level Label
- **Rows**: Attrition Rate
- **Sort**: Junior → Executive
- **Color**: Single blue, add circle marks

### Chart 4 — Risk Factor Comparison (Side-by-Side Bars)
Create two measures:
- `Overtime Attrition Rate` = attrition rate for Overtime=Yes vs No
- Same for Travel Frequently vs Non-Travel

Build as a grouped bar:
- **Columns**: Risk Factor (create a string parameter or use two separate sheets)
- **Rows**: Attrition Rate
- **Color**: Yes/No or High/Low

### Chart 5 — Attrition by Satisfaction Quadrant (Scatter)
- **Columns**: AVG([Job Satisfaction])
- **Rows**: AVG([Work Life Balance])
- **Detail**: Department
- **Color**: Attrition Rate
- **Size**: COUNT([Employee Id])
- **Add reference lines** at x=2.5 and y=2.5 to create quadrants

### Filters
- Department, Gender, Overtime, Business Travel

---

## Dashboard 3 — Compensation Analysis

**Purpose**: Surface pay equity issues and compensation distribution.

### KPI Row
| Metric | |
|--------|--|
| Avg Annual Salary | Overall |
| Median Salary | Use `MEDIAN([Annual Salary])` |
| Salary Range | `MAX([Annual Salary]) - MIN([Annual Salary])` |
| Gender Pay Gap % | `(AVG(IF [Gender]='Male' THEN [Annual Salary] END) - AVG(IF [Gender]='Female' THEN [Annual Salary] END)) / AVG(IF [Gender]='Male' THEN [Annual Salary] END)` |

### Chart 1 — Salary by Department & Job Level (Heatmap)
- **Rows**: Department
- **Columns**: Job Level Label
- **Color**: AVG([Annual Salary]) — Blue sequential
- **Text**: `$` + AVG([Annual Salary]) formatted
- **Mark type**: Square

### Chart 2 — Salary Distribution (Box Plot)
- **Columns**: Department
- **Rows**: Annual Salary
- **Mark type**: Circle
- **Analytics pane**: Drag "Box Plot" onto the view
- **Color**: Department

### Chart 3 — Gender Pay Equity by Department (Dual Bar)
- **Rows**: Department
- **Columns**: AVG([Annual Salary])
- **Color**: Gender
- **Mark type**: Bar, side-by-side
- **Reference line**: Parity line

### Chart 4 — Salary vs Performance (Scatter)
- **Columns**: Performance Label
- **Rows**: AVG([Annual Salary])
- **Color**: Department
- **Size**: COUNT([Employee Id])

### Chart 5 — Salary Band Distribution (Treemap)
- **Color + Label + Size**: COUNT([Employee Id])
- **Detail**: Salary Band
- **Label**: Salary Band + COUNT

### Filters
- Department, Gender, Job Level, Education Level

---

## Dashboard 4 — Wellbeing & Performance

**Purpose**: Identify engagement risks and performance distribution.

### KPI Row
| Metric | |
|--------|--|
| Avg Job Satisfaction | AVG([Job Satisfaction]) / 4 — format as % |
| Avg Work-Life Balance | AVG([Work Life Balance]) / 4 |
| Avg Environment Satisfaction | AVG([Environment Satisfaction]) / 4 |
| % High Performers | `COUNT(IF [Performance Rating] >= 3 THEN 1 END) / COUNT(1)` |

### Chart 1 — Satisfaction Scores by Department (Grouped Bar)
- 3 measures on Columns: AVG Job Sat, AVG Env Sat, AVG WLB
- Department on Rows
- Use Measure Names/Values trick for grouped bars
- Color: Measure Names

### Chart 2 — Performance Distribution (Bar)
- **Columns**: Performance Label
- **Rows**: COUNT([Employee Id])
- **Color**: Performance Label
  - 1=Low → Red, 2=Good → Amber, 3=Excellent → Blue, 4=Outstanding → Green
- **Label**: COUNT + % of total

### Chart 3 — Overtime vs Satisfaction (Heatmap)
- **Rows**: Overtime
- **Columns**: Job Satisfaction (discrete)
- **Color**: COUNT([Employee Id]) — highlight high-risk (Overtime=Yes, Sat=1)
- **Text**: COUNT([Employee Id])

### Chart 4 — Training vs Performance (Scatter)
- **Columns**: AVG([Training Last Year])
- **Rows**: AVG([Performance Rating])
- **Color**: Department
- **Size**: COUNT([Employee Id])
- **Trend line**: Add linear trend (Analytics pane)
- **Insight**: More training → higher performance?

### Chart 5 — Satisfaction vs Attrition (Bullet Chart / Side-by-Side)
- **Columns**: Attrition
- **Rows**: AVG([Composite Satisfaction Score])
- **Color**: Attrition (Green=No, Red=Yes)
- Expected: Leavers have lower satisfaction

### Filters
- Department, Overtime, Performance Rating, Business Travel

---

## Final Steps

1. Create a **Story** in Tableau linking all 4 dashboards in narrative order
2. Add a **title banner** to each dashboard with your name and dataset info
3. **Publish to Tableau Public**: Server → Tableau Public → Save to Tableau Public
4. Copy the Tableau Public URL and paste it into the GitHub `README.md`
5. Add topics in GitHub: `tableau`, `hr-analytics`, `data-visualization`, `workforce-analytics`
