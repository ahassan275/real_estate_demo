"""
Visualization functions using Plotly for real estate market insights.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


def plot_price_comparison_chart(
    target_price: float,
    median_price: float,
    average_price: float,
    is_rental: bool = False
) -> go.Figure:
    """
    Create a bar chart comparing target price with market prices.

    Args:
        target_price: User's target price/rent
        median_price: Market median price/rent
        average_price: Market average price/rent
        is_rental: Whether this is rental data

    Returns:
        Plotly Figure
    """
    label = "Rent ($/month)" if is_rental else "Price ($)"

    fig = go.Figure(data=[
        go.Bar(
            x=['Your Target', 'Market Median', 'Market Average'],
            y=[target_price, median_price, average_price],
            marker=dict(
                color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                line=dict(color='white', width=2)
            ),
            text=[f'${val:,.0f}' for val in [target_price, median_price, average_price]],
            textposition='outside',
        )
    ])

    fig.update_layout(
        title=f'{label} Comparison',
        yaxis_title=label,
        showlegend=False,
        height=400,
        hovermode='x unified',
        template='plotly_white'
    )

    fig.update_yaxes(tickprefix='$', tickformat=',.0f')

    return fig


def plot_price_trends(
    data: pd.DataFrame,
    subtype: Optional[str] = None,
    is_rental: bool = False
) -> go.Figure:
    """
    Create a line chart showing price/rent trends over time.

    Args:
        data: Sales or rental data DataFrame with Date column
        subtype: Optional property subtype for title
        is_rental: Whether this is rental data

    Returns:
        Plotly Figure
    """
    label = "Rent" if is_rental else "Price"
    median_col = 'Median Rent Price' if is_rental else 'Median Sold Price'
    avg_col = 'Average Rent Price' if is_rental else 'Average Sold Price'

    fig = go.Figure()

    # Median line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data[median_col],
        mode='lines+markers',
        name=f'Median {label}',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=6)
    ))

    # Average line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data[avg_col],
        mode='lines+markers',
        name=f'Average {label}',
        line=dict(color='#45B7D1', width=3, dash='dash'),
        marker=dict(size=6)
    ))

    title = f'{label} Trends Over Time'
    if subtype:
        title += f' - {subtype}'

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=f'{label} ($)',
        hovermode='x unified',
        height=450,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_yaxes(tickprefix='$', tickformat=',.0f')

    return fig


def plot_market_activity(
    data: pd.DataFrame,
    is_rental: bool = False
) -> go.Figure:
    """
    Create a stacked bar chart showing market activity over time.

    Args:
        data: Sales or rental data DataFrame
        is_rental: Whether this is rental data

    Returns:
        Plotly Figure
    """
    fig = go.Figure()

    if is_rental:
        # Rental activity
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['No. Of Active Listings'],
            name='Active Listings',
            marker_color='#FFD93D'
        ))
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['No. Of Rented Properties'],
            name='Rented Properties',
            marker_color='#6BCB77'
        ))
        title = 'Rental Market Activity Over Time'
    else:
        # Sales activity
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['No. Of Active Listings'],
            name='Active Listings',
            marker_color='#FFD93D'
        ))
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['No. Of Conditional Sales'],
            name='Conditional Sales',
            marker_color='#FFA500'
        ))
        fig.add_trace(go.Bar(
            x=data['Date'],
            y=data['No. Of Sold Properties'],
            name='Sold Properties',
            marker_color='#6BCB77'
        ))
        title = 'Sales Market Activity Over Time'

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Number of Properties',
        barmode='group',
        hovermode='x unified',
        height=450,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def plot_property_type_distribution(
    subtype_data: pd.DataFrame,
    property_type: str,
    is_rental: bool = False
) -> go.Figure:
    """
    Create an area chart showing property type distribution over time.

    Args:
        subtype_data: Property subtype breakdown DataFrame
        property_type: 'Freehold' or 'Condo'
        is_rental: Whether this is rental data

    Returns:
        Plotly Figure
    """
    fig = go.Figure()

    # Get all columns except Date and Total columns
    exclude_cols = ['Date', 'Total - Freehold', 'Total Condo', 'Total', 'Condo']
    subtype_cols = [col for col in subtype_data.columns if col not in exclude_cols]

    colors = px.colors.qualitative.Set3

    for idx, col in enumerate(subtype_cols):
        col_name = col.strip()
        fig.add_trace(go.Scatter(
            x=subtype_data['Date'],
            y=subtype_data[col],
            mode='lines',
            name=col_name,
            stackgroup='one',
            line=dict(width=0.5),
            fillcolor=colors[idx % len(colors)]
        ))

    market_label = "Rental" if is_rental else "Sales"
    title = f'{property_type} {market_label} by Property Type Over Time'

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Number of Properties',
        hovermode='x unified',
        height=450,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def plot_dom_trends(data: pd.DataFrame, is_rental: bool = False) -> go.Figure:
    """
    Create a line chart showing Days on Market trends.

    Args:
        data: Sales or rental data DataFrame
        is_rental: Whether this is rental data

    Returns:
        Plotly Figure
    """
    fig = go.Figure()

    # Median DOM
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Median DOM'],
        mode='lines+markers',
        name='Median DOM',
        line=dict(color='#E63946', width=3),
        marker=dict(size=6)
    ))

    # Average DOM
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Average DOM'],
        mode='lines+markers',
        name='Average DOM',
        line=dict(color='#F77F00', width=3, dash='dash'),
        marker=dict(size=6)
    ))

    market_label = "Rental" if is_rental else "Sales"
    title = f'Days on Market Trends - {market_label}'

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Days on Market',
        hovermode='x unified',
        height=400,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig
