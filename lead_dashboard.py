import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Ontario Public Sector Lead List", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/filtered_leads.csv')

df = load_data()

# Header
st.title("🎯 Ontario Public Sector Lead List")
st.markdown("### Privacy, Compliance, Legal & Security Professionals")

# Sidebar filters
st.sidebar.header("Filters")

# Category filter
categories = ['All'] + sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=['All']
)

# Sector filter
sectors = ['All'] + sorted(df['Sector'].unique().tolist())
selected_sector = st.sidebar.multiselect(
    "Sector",
    options=sectors,
    default=['All']
)

# Salary range
min_salary = int(df['Salary'].min())
max_salary = int(df['Salary'].max())
salary_range = st.sidebar.slider(
    "Salary Range",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary),
    format="$%d"
)

# Priority score filter
min_priority = float(df['Priority_Score'].min())
max_priority = float(df['Priority_Score'].max())
priority_threshold = st.sidebar.slider(
    "Minimum Priority Score",
    min_value=min_priority,
    max_value=max_priority,
    value=min_priority,
    step=0.5
)

# Search box
search_term = st.sidebar.text_input("Search (Name, Title, Employer)")

# Apply filters
filtered_df = df.copy()

if 'All' not in selected_category:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_category)]

if 'All' not in selected_sector:
    filtered_df = filtered_df[filtered_df['Sector'].isin(selected_sector)]

filtered_df = filtered_df[
    (filtered_df['Salary'] >= salary_range[0]) &
    (filtered_df['Salary'] <= salary_range[1]) &
    (filtered_df['Priority_Score'] >= priority_threshold)
]

if search_term:
    mask = (
        filtered_df['First Name'].str.contains(search_term, case=False, na=False) |
        filtered_df['Last Name'].str.contains(search_term, case=False, na=False) |
        filtered_df['Job Title'].str.contains(search_term, case=False, na=False) |
        filtered_df['Employer'].str.contains(search_term, case=False, na=False)
    )
    filtered_df = filtered_df[mask]

# Top metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Leads", f"{len(filtered_df):,}")
with col2:
    st.metric("Avg Salary", f"${filtered_df['Salary'].mean():,.0f}")
with col3:
    st.metric("Organizations", filtered_df['Employer'].nunique())
with col4:
    st.metric("Avg Priority", f"{filtered_df['Priority_Score'].mean():.2f}")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📋 Lead List", "📈 Analytics", "💾 Export"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Category distribution
        category_counts = filtered_df['Category'].value_counts()
        fig_cat = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Distribution by Category",
            hole=0.4
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        # Sector distribution
        sector_counts = filtered_df['Sector'].value_counts()
        fig_sector = px.bar(
            x=sector_counts.index,
            y=sector_counts.values,
            title="Distribution by Sector",
            labels={'x': 'Sector', 'y': 'Count'}
        )
        st.plotly_chart(fig_sector, use_container_width=True)

    # Top organizations
    st.subheader("Top 20 Organizations by Lead Count")
    top_orgs = filtered_df['Employer'].value_counts().head(20)
    fig_orgs = px.bar(
        x=top_orgs.values,
        y=top_orgs.index,
        orientation='h',
        labels={'x': 'Number of Leads', 'y': 'Organization'}
    )
    fig_orgs.update_layout(height=600)
    st.plotly_chart(fig_orgs, use_container_width=True)

with tab2:
    st.subheader("Filtered Lead List")

    # Display options
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Showing {len(filtered_df)} results")
    with col2:
        rows_per_page = st.selectbox("Rows per page", [25, 50, 100, 250], index=1)

    # Pagination
    total_pages = (len(filtered_df) - 1) // rows_per_page + 1
    page = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1)
    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    # Display table
    display_df = filtered_df.iloc[start_idx:end_idx].copy()
    display_df['Salary'] = display_df['Salary'].apply(lambda x: f"${x:,.0f}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Priority_Score": st.column_config.NumberColumn("Priority", format="%.2f"),
            "Salary": st.column_config.TextColumn("Salary"),
        }
    )

with tab3:
    st.subheader("Analytics & Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Salary distribution by category
        fig_salary_cat = px.box(
            filtered_df,
            x='Category',
            y='Salary',
            title="Salary Distribution by Category",
            labels={'Salary': 'Salary ($)'}
        )
        st.plotly_chart(fig_salary_cat, use_container_width=True)

    with col2:
        # Priority score distribution
        fig_priority = px.histogram(
            filtered_df,
            x='Priority_Score',
            nbins=30,
            title="Priority Score Distribution",
            labels={'Priority_Score': 'Priority Score'}
        )
        st.plotly_chart(fig_priority, use_container_width=True)

    # Salary vs Priority scatter
    fig_scatter = px.scatter(
        filtered_df,
        x='Salary',
        y='Priority_Score',
        color='Category',
        hover_data=['First Name', 'Last Name', 'Job Title', 'Employer'],
        title="Salary vs Priority Score",
        labels={'Salary': 'Salary ($)', 'Priority_Score': 'Priority Score'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Top titles
    st.subheader("Most Common Job Titles")
    top_titles = filtered_df['Job Title'].value_counts().head(20)
    fig_titles = px.bar(
        x=top_titles.values,
        y=top_titles.index,
        orientation='h',
        labels={'x': 'Count', 'y': 'Job Title'}
    )
    fig_titles.update_layout(height=600)
    st.plotly_chart(fig_titles, use_container_width=True)

with tab4:
    st.subheader("Export Leads")

    st.write(f"**{len(filtered_df)}** leads match your current filters")

    # Export format options
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Full Export")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="ontario_leads_full.csv",
            mime="text/csv"
        )

    with col2:
        st.write("### Contact Info Only")
        contact_only = filtered_df[['First Name', 'Last Name', 'Job Title', 'Employer', 'Sector']].copy()
        csv_contact = contact_only.to_csv(index=False)
        st.download_button(
            label="📥 Download Contact List",
            data=csv_contact,
            file_name="ontario_leads_contacts.csv",
            mime="text/csv"
        )

    # Sample preview
    st.write("### Preview of Export Data")
    st.dataframe(filtered_df.head(10), use_container_width=True, hide_index=True)

    # Export summary stats
    st.write("### Export Summary")
    summary_stats = pd.DataFrame({
        'Metric': ['Total Leads', 'Unique Organizations', 'Average Salary', 'Median Salary',
                   'Salary Range', 'Most Common Category', 'Most Common Sector'],
        'Value': [
            f"{len(filtered_df):,}",
            f"{filtered_df['Employer'].nunique():,}",
            f"${filtered_df['Salary'].mean():,.0f}",
            f"${filtered_df['Salary'].median():,.0f}",
            f"${filtered_df['Salary'].min():,.0f} - ${filtered_df['Salary'].max():,.0f}",
            filtered_df['Category'].mode().iloc[0] if len(filtered_df) > 0 else 'N/A',
            filtered_df['Sector'].mode().iloc[0] if len(filtered_df) > 0 else 'N/A'
        ]
    })
    st.table(summary_stats)

# Footer
st.sidebar.markdown("---")
st.sidebar.info(f"**Data Source:** Ontario Public Service Salary Disclosure 2024\n\n**Total Records:** {len(df):,}")
