"""
Real Estate Market Insights Demo - Streamlit Application
"""
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import RealEstateDataLoader
from analytics import SalesAnalytics, RentalAnalytics
from visualizations import (
    plot_price_comparison_chart,
    plot_price_trends,
    plot_market_activity,
    plot_property_type_distribution,
    plot_dom_trends
)

# Page configuration
st.set_page_config(
    page_title="Real Estate Market Insights",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .summary-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4ECDC4;
        margin: 1rem 0;
        color: #1a1a1a;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache real estate data."""
    data_path = Path(__file__).parent / 'data' / 'market_data.xlsx'
    loader = RealEstateDataLoader(str(data_path))
    loader.load_all_sheets()  # Preload all sheets
    return loader


def main():
    # Title
    st.markdown('<div class="main-header">🏠 Real Estate Market Insights Demo</div>', unsafe_allow_html=True)

    # Load data
    loader = load_data()

    # Sidebar - User Inputs
    st.sidebar.header("📊 Market Configuration")

    # Market segment selection
    market_segment = st.sidebar.radio(
        "Select Market Segment",
        ["🏠 Sales - Freehold", "🏢 Sales - Condo", "🔑 Rental - Freehold", "🔑 Rental - Condo"],
        index=0
    )

    # Parse market segment
    is_rental = "Rental" in market_segment
    property_type = "Freehold" if "Freehold" in market_segment else "Condo"

    # Get available subtypes
    segment_type = "Rental" if is_rental else "Sales"
    available_subtypes = loader.get_available_subtypes(property_type, segment_type)

    # Property subtype selection
    subtype = st.sidebar.selectbox(
        "Property Subtype",
        options=['All'] + available_subtypes,
        index=0
    )

    # Target price/rent input
    if is_rental:
        target_value = st.sidebar.number_input(
            "Target Monthly Rent ($)",
            min_value=500,
            max_value=10000,
            value=2500,
            step=100
        )
    else:
        target_value = st.sidebar.number_input(
            "Target Price ($)",
            min_value=100000,
            max_value=5000000,
            value=800000,
            step=10000
        )

    # Timeframe filter
    timeframe = st.sidebar.selectbox(
        "Timeframe",
        options=[
            ("Last 3 Months", "last_3_months"),
            ("Last 6 Months", "last_6_months"),
            ("Since 2023", "since_2023"),
            ("All Data", "all")
        ],
        format_func=lambda x: x[0],
        index=1
    )
    timeframe_value = timeframe[1]

    st.sidebar.markdown("---")
    st.sidebar.info("💡 Adjust the filters above to see how your target compares to the market.")

    # Load appropriate data
    if is_rental:
        main_data = loader.get_rental_data(property_type)
        subtype_data = loader.get_rental_by_subtype(property_type)
    else:
        main_data = loader.get_sales_data(property_type)
        subtype_data = loader.get_sales_by_subtype(property_type)

    # Filter by timeframe
    main_data_filtered = loader.filter_by_timeframe(main_data, timeframe_value)
    subtype_data_filtered = loader.filter_by_timeframe(subtype_data, timeframe_value)

    # Perform analytics
    if is_rental:
        analytics = RentalAnalytics()
        comparison = analytics.calculate_rent_comparison(target_value, main_data_filtered)
        activity = analytics.get_rental_activity_summary(
            main_data_filtered,
            subtype_data_filtered,
            None if subtype == 'All' else subtype
        )
        time_metrics = analytics.calculate_time_to_rent(main_data_filtered)
        summary = analytics.generate_rental_summary(
            target_value,
            comparison,
            time_metrics,
            activity,
            None if subtype == 'All' else subtype
        )
    else:
        analytics = SalesAnalytics()
        comparison = analytics.calculate_price_comparison(
            target_value,
            main_data_filtered,
            subtype_data_filtered,
            None if subtype == 'All' else subtype
        )
        activity = analytics.get_market_activity_summary(
            main_data_filtered,
            subtype_data_filtered,
            None if subtype == 'All' else subtype
        )
        time_metrics = analytics.calculate_time_to_sell(main_data_filtered)
        summary = analytics.generate_sales_summary(
            target_value,
            comparison,
            time_metrics,
            activity,
            None if subtype == 'All' else subtype
        )

    # Display Key Metrics
    st.header("📈 Key Metrics")

    # Add clarification note about subtype filtering
    if subtype != 'All':
        st.info(f"ℹ️ **Note:** Price and Days on Market metrics show overall {property_type} market data. The property subtype filter ('{subtype}') affects market activity counts and the property distribution chart.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        label = "Median Rent" if is_rental else "Median Price"
        value = comparison.get('median_rent' if is_rental else 'median_price')
        st.metric(
            label=label,
            value=f"${value:,.0f}" if value else "N/A"
        )

    with col2:
        label = "Average Rent" if is_rental else "Average Price"
        value = comparison.get('average_rent' if is_rental else 'average_price')
        st.metric(
            label=label,
            value=f"${value:,.0f}" if value else "N/A"
        )

    with col3:
        diff = comparison.get('median_diff_percent', 0)
        st.metric(
            label="% Difference from Median",
            value=f"{diff:+.1f}%",
            delta=f"{diff:+.1f}%",
            delta_color="inverse" if is_rental else "normal"
        )

    with col4:
        dom = time_metrics.get('median_dom')
        st.metric(
            label="Median Days on Market",
            value=f"{dom} days" if dom else "N/A"
        )

    # Natural Language Summary
    st.markdown("### 💬 Market Insights")
    st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

    # Visualizations
    st.header("📊 Visualizations")

    # Price/Rent Comparison Chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Price Comparison")
        price_fig = plot_price_comparison_chart(
            target_value,
            comparison.get('median_rent' if is_rental else 'median_price'),
            comparison.get('average_rent' if is_rental else 'average_price'),
            is_rental
        )
        st.plotly_chart(price_fig, use_container_width=True)

    with col2:
        st.subheader("Market Activity (Last Month)")
        if is_rental:
            activity_col1, activity_col2 = st.columns(2)
            with activity_col1:
                st.metric("Active Listings", activity['active_listings'])
            with activity_col2:
                st.metric("Rented Properties", activity['rented_properties'])
            if activity['subtype_rented'] is not None and subtype != 'All':
                st.metric(f"{subtype} Rented", activity['subtype_rented'])
        else:
            activity_col1, activity_col2, activity_col3 = st.columns(3)
            with activity_col1:
                st.metric("Active Listings", activity['active_listings'])
            with activity_col2:
                st.metric("Conditional Sales", activity['conditional_sales'])
            with activity_col3:
                st.metric("Sold Properties", activity['sold_properties'])
            if activity['subtype_sold'] is not None and subtype != 'All':
                st.metric(f"{subtype} Sold", activity['subtype_sold'])

    # Price/Rent Trends
    st.subheader("Price Trends Over Time" if not is_rental else "Rent Trends Over Time")
    trends_fig = plot_price_trends(
        main_data_filtered,
        None if subtype == 'All' else subtype,
        is_rental
    )
    st.plotly_chart(trends_fig, use_container_width=True)

    # Market Activity Over Time
    st.subheader("Market Activity Over Time")
    activity_fig = plot_market_activity(main_data_filtered, is_rental)
    st.plotly_chart(activity_fig, use_container_width=True)

    # Property Type Distribution
    if len(subtype_data_filtered) > 0:
        st.subheader("Property Type Distribution Over Time")
        distribution_fig = plot_property_type_distribution(
            subtype_data_filtered,
            property_type,
            is_rental
        )
        st.plotly_chart(distribution_fig, use_container_width=True)

    # Days on Market Trends
    st.subheader("Days on Market Trends")
    dom_fig = plot_dom_trends(main_data_filtered, is_rental)
    st.plotly_chart(dom_fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with Streamlit | Data from market_data.xlsx"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
