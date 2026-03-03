# Ontario Public Sector Lead Generation

## Overview
Tool to extract and analyze privacy, compliance, legal, security, risk, and governance professionals from Ontario's Public Service Salary Disclosure data for targeted outreach.

## Dataset
- **Source**: Ontario Public Service Salary Disclosure 2024
- **Total Records**: 377,881 public servants
- **Filtered Leads**: 9,082 relevant contacts
- **File**: `data/tbs-pssd-compendium-salary-disclosed-2024-en-utf-8-2026-01-29.csv`

## Target Roles
- Privacy Officers & Data Protection
- Compliance Officers & Regulatory
- Legal Counsel & General Counsel
- Information Security (CISO, InfoSec)
- Risk Management Officers
- Governance, Policy & Audit

## Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Install Dependencies (if needed)
```bash
pip install pandas plotly streamlit
```

### 3. Generate Lead List
```bash
python lead_filter.py
```

### 4. Launch Dashboard
```bash
streamlit run lead_dashboard.py
```

Access at: http://localhost:8501

## Files

### `lead_filter.py`
Filters and processes the raw data:
- Searches for relevant job titles using keyword matching
- Removes duplicates
- Categorizes roles (Privacy, Compliance, Legal, Security, Risk, Governance)
- Calculates priority scores based on seniority and salary
- Outputs: `data/filtered_leads.csv`

### `lead_dashboard.py`
Interactive Streamlit dashboard with:
- **Filters**: Category, sector, salary range, priority threshold, search
- **Overview**: Distribution charts and top organizations
- **Lead List**: Paginated, searchable contact table
- **Analytics**: Salary distributions, priority scores, common titles
- **Export**: Download filtered results as CSV

### `data/filtered_leads.csv`
Columns:
- `Priority_Score` - Weighted score (seniority + salary)
- `Category` - Role classification
- `Sector` - Public sector category
- `First Name`, `Last Name`
- `Job Title`
- `Employer` - Organization name
- `Salary`

## Priority Scoring
Leads are ranked by:
- **Seniority**: Chief/CISO/CPO (+10), VP/Exec Director (+8), Director/GC (+6), Manager/Senior (+4), Lead/Coordinator (+2)
- **Salary**: Normalized contribution (+salary/100000 * 2)

Higher scores = more senior decision-makers

## Key Statistics
- **9,082 total leads** across all sectors
- **Average Salary**: $142,011
- **Top Organization**: Attorney General (988 leads)
- **Primary Categories**: Governance (39%), Legal (34%), Compliance (9%)
- **Main Sectors**: Gov Ministries (37%), Crown Agencies (17%), Municipalities (17%)

## Top Organizations
1. Attorney General - 988
2. City of Toronto - 399
3. Ontario Power Generation - 388
4. Environment, Conservation and Parks - 323
5. Legal Aid Ontario - 301
6. Treasury Board Secretariat - 285
7. University of Toronto - 222
8. Metrolinx - 202

## Export Options
From the dashboard's Export tab:
- **Full Export**: All columns including salary and priority
- **Contact List**: Name, title, employer, sector only

## Use Case
Target decision-makers at Ontario public organizations for privacy/compliance tool integration. Focus on high-priority leads (Chief/VP/Director level) in relevant departments.
