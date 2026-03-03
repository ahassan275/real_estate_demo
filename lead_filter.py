import pandas as pd
import re

# Load the CSV
df = pd.read_csv('data/tbs-pssd-compendium-salary-disclosed-2024-en-utf-8-2026-01-29.csv')

# Define relevant keywords for filtering
keywords = [
    # Privacy roles
    'Privacy', 'Data Protection', 'Privacy Officer', 'Chief Privacy',
    # Compliance roles
    'Compliance', 'Compliance Officer', 'Regulatory',
    # Legal roles
    'Legal', 'Counsel', 'General Counsel', 'Legal Services', 'Paralegal', 'Law Clerk',
    # Security roles
    'Information Security', 'Cyber Security', 'CISO', 'Chief Information Security',
    'Security Officer', 'InfoSec',
    # Risk roles
    'Risk', 'Risk Management', 'Risk Officer', 'Chief Risk',
    # Governance roles
    'Governance', 'Policy', 'Audit', 'Internal Audit',
    # Director/Executive roles that might be relevant
    'Chief Legal', 'Chief Compliance', 'VP Legal', 'Vice President Legal',
    'Associate General Counsel', 'Assistant General Counsel'
]

# Create a regex pattern (case-insensitive)
pattern = '|'.join(keywords)

# Filter the dataframe
filtered_df = df[df['Job Title'].str.contains(pattern, case=False, na=False)]

# Remove duplicate people (same first name, last name, employer)
filtered_df = filtered_df.drop_duplicates(subset=['First Name', 'Last Name', 'Employer'])

# Sort by sector, employer, and salary (descending) to prioritize senior roles
filtered_df = filtered_df.sort_values(['Sector', 'Employer', 'Salary'], ascending=[True, True, False])

# Create a clean contact list
contact_list = filtered_df[['Sector', 'First Name', 'Last Name', 'Job Title', 'Employer', 'Salary']].copy()

# Add a category column to classify the type of role
def categorize_role(title):
    title_lower = str(title).lower()
    categories = []

    if any(word in title_lower for word in ['privacy', 'data protection']):
        categories.append('Privacy')
    if any(word in title_lower for word in ['compliance', 'regulatory']):
        categories.append('Compliance')
    if any(word in title_lower for word in ['legal', 'counsel', 'paralegal', 'law clerk']):
        categories.append('Legal')
    if any(word in title_lower for word in ['security', 'ciso', 'infosec']):
        categories.append('Security')
    if any(word in title_lower for word in ['risk']):
        categories.append('Risk')
    if any(word in title_lower for word in ['governance', 'policy', 'audit']):
        categories.append('Governance')

    return ', '.join(categories) if categories else 'Other'

contact_list['Category'] = contact_list['Job Title'].apply(categorize_role)

# Add priority score (higher salary and more senior titles get higher priority)
def calculate_priority(row):
    score = 0
    title = str(row['Job Title']).lower()

    # Seniority bonuses
    if 'chief' in title or 'ciso' in title or 'cpo' in title:
        score += 10
    elif 'vice president' in title or 'vp' in title or 'executive director' in title:
        score += 8
    elif 'director' in title or 'general counsel' in title:
        score += 6
    elif 'manager' in title or 'senior' in title:
        score += 4
    elif 'lead' in title or 'coordinator' in title:
        score += 2

    # Salary bonus (normalized)
    score += (row['Salary'] / 100000) * 2

    return round(score, 2)

contact_list['Priority_Score'] = contact_list.apply(calculate_priority, axis=1)

# Reorder columns
contact_list = contact_list[['Priority_Score', 'Category', 'Sector', 'First Name', 'Last Name',
                              'Job Title', 'Employer', 'Salary']]

# Sort by priority score
contact_list = contact_list.sort_values('Priority_Score', ascending=False)

# Save to CSV
contact_list.to_csv('data/filtered_leads.csv', index=False)

# Print summary statistics
print(f"Total records in original dataset: {len(df):,}")
print(f"Total filtered leads: {len(contact_list):,}")
print(f"\nBreakdown by Category:")
print(contact_list['Category'].value_counts())
print(f"\nBreakdown by Sector:")
print(contact_list['Sector'].value_counts())
print(f"\nTop 10 Organizations by Number of Leads:")
print(contact_list['Employer'].value_counts().head(10))
print(f"\nSalary Statistics:")
print(f"Average Salary: ${contact_list['Salary'].mean():,.2f}")
print(f"Median Salary: ${contact_list['Salary'].median():,.2f}")
print(f"\nData saved to: data/filtered_leads.csv")
