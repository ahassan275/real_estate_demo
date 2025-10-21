"""
Analytics and calculations for real estate market insights.
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple


class SalesAnalytics:
    """Analytics for sales market data."""

    @staticmethod
    def calculate_price_comparison(
        target_price: float,
        historical_data: pd.DataFrame,
        subtype_data: Optional[pd.DataFrame] = None,
        subtype: Optional[str] = None
    ) -> Dict:
        """
        Calculate price comparison metrics.

        Args:
            target_price: User's target price
            historical_data: Sales data DataFrame
            subtype_data: Optional subtype breakdown data
            subtype: Optional specific subtype to filter by

        Returns:
            Dictionary with median, average, and percentage differences
        """
        # Filter out NaN values
        median_price = historical_data['Median Sold Price'].median()
        average_price = historical_data['Average Sold Price'].mean()

        # Calculate percentage differences
        median_diff = ((target_price - median_price) / median_price * 100) if median_price else 0
        average_diff = ((target_price - average_price) / average_price * 100) if average_price else 0

        return {
            'median_price': median_price,
            'average_price': average_price,
            'median_diff_percent': median_diff,
            'average_diff_percent': average_diff,
            'target_price': target_price
        }

    @staticmethod
    def get_market_activity_summary(
        data: pd.DataFrame,
        subtype_data: Optional[pd.DataFrame] = None,
        subtype: Optional[str] = None
    ) -> Dict:
        """
        Get market activity summary.

        Args:
            data: Sales data DataFrame
            subtype_data: Optional subtype breakdown data
            subtype: Optional specific subtype

        Returns:
            Dictionary with activity metrics
        """
        # Get most recent data
        recent_data = data.tail(4)  # Last month (4 weeks)

        # Use nanmean and nansum to ignore NaN values
        active_listings = np.nanmean(recent_data['No. Of Active Listings'].values)
        conditional_sales = np.nansum(recent_data['No. Of Conditional Sales'].values)
        sold_properties = np.nansum(recent_data['No. Of Sold Properties'].values)

        # If subtype data is available, add subtype-specific counts
        subtype_count = None
        if subtype_data is not None and subtype and subtype in subtype_data.columns:
            subtype_count = np.nansum(subtype_data[subtype].tail(4).values)

        return {
            'active_listings': int(active_listings) if not pd.isna(active_listings) else 0,
            'conditional_sales': int(conditional_sales) if not pd.isna(conditional_sales) else 0,
            'sold_properties': int(sold_properties) if not pd.isna(sold_properties) else 0,
            'subtype_sold': int(subtype_count) if subtype_count is not None and not pd.isna(subtype_count) else None
        }

    @staticmethod
    def calculate_time_to_sell(data: pd.DataFrame) -> Dict:
        """
        Calculate time to sell metrics.

        Args:
            data: Sales data DataFrame

        Returns:
            Dictionary with DOM and CDOM metrics
        """
        median_dom = data['Median DOM'].median()
        average_dom = data['Average DOM'].mean()
        median_cdom = data['Median CDOM'].median()
        average_cdom = data['Average CDOM'].mean()

        return {
            'median_dom': int(median_dom) if not pd.isna(median_dom) else None,
            'average_dom': int(average_dom) if not pd.isna(average_dom) else None,
            'median_cdom': int(median_cdom) if not pd.isna(median_cdom) else None,
            'average_cdom': int(average_cdom) if not pd.isna(average_cdom) else None
        }

    @staticmethod
    def generate_sales_summary(
        target_price: float,
        price_comparison: Dict,
        time_metrics: Dict,
        activity: Dict,
        subtype: Optional[str] = None
    ) -> str:
        """
        Generate natural language summary for sales.

        Args:
            target_price: User's target price
            price_comparison: Price comparison metrics
            time_metrics: Time to sell metrics
            activity: Market activity metrics
            subtype: Property subtype

        Returns:
            Natural language summary string
        """
        median_diff = price_comparison['median_diff_percent']
        median_price = price_comparison['median_price']
        median_dom = time_metrics.get('median_dom')

        # Price positioning
        if median_diff < -10:
            price_msg = f"Your target price of ${target_price:,.0f} is **{abs(median_diff):.1f}% below** the market median of ${median_price:,.0f}. This is highly competitive for buyers and may attract multiple offers."
        elif median_diff > 10:
            price_msg = f"Your target price of ${target_price:,.0f} is **{median_diff:.1f}% above** the market median of ${median_price:,.0f}. If selling, this may take longer to find a buyer."
        else:
            price_msg = f"Your target price of ${target_price:,.0f} is **well-aligned** with the market median of ${median_price:,.0f} (within {abs(median_diff):.1f}%)."

        # Time to sell
        if median_dom:
            time_msg = f" Properties typically sell in **{median_dom} days** (median DOM)."
        else:
            time_msg = ""

        # Market activity
        subtype_msg = f" for {subtype} properties" if subtype else ""
        activity_msg = f" In the last month, **{activity['sold_properties']} properties** were sold{subtype_msg}."

        return price_msg + time_msg + activity_msg


class RentalAnalytics:
    """Analytics for rental market data."""

    @staticmethod
    def calculate_rent_comparison(
        target_rent: float,
        rental_data: pd.DataFrame
    ) -> Dict:
        """
        Calculate rent comparison metrics.

        Args:
            target_rent: User's target rent
            rental_data: Rental data DataFrame

        Returns:
            Dictionary with median, average, and percentage differences
        """
        median_rent = rental_data['Median Rent Price'].median()
        average_rent = rental_data['Average Rent Price'].mean()

        median_diff = ((target_rent - median_rent) / median_rent * 100) if median_rent else 0
        average_diff = ((target_rent - average_rent) / average_rent * 100) if average_rent else 0

        return {
            'median_rent': median_rent,
            'average_rent': average_rent,
            'median_diff_percent': median_diff,
            'average_diff_percent': average_diff,
            'target_rent': target_rent
        }

    @staticmethod
    def get_rental_activity_summary(
        data: pd.DataFrame,
        subtype_data: Optional[pd.DataFrame] = None,
        subtype: Optional[str] = None
    ) -> Dict:
        """
        Get rental market activity summary.

        Args:
            data: Rental data DataFrame
            subtype_data: Optional rental type breakdown data
            subtype: Optional specific rental type

        Returns:
            Dictionary with activity metrics
        """
        recent_data = data.tail(4)  # Last month

        # Use nanmean and nansum to ignore NaN values
        active_listings = np.nanmean(recent_data['No. Of Active Listings'].values)
        rented_properties = np.nansum(recent_data['No. Of Rented Properties'].values)

        # Subtype-specific counts
        subtype_count = None
        if subtype_data is not None and subtype and subtype in subtype_data.columns:
            subtype_count = np.nansum(subtype_data[subtype].tail(4).values)

        return {
            'active_listings': int(active_listings) if not pd.isna(active_listings) else 0,
            'rented_properties': int(rented_properties) if not pd.isna(rented_properties) else 0,
            'subtype_rented': int(subtype_count) if subtype_count is not None and not pd.isna(subtype_count) else None
        }

    @staticmethod
    def calculate_time_to_rent(data: pd.DataFrame) -> Dict:
        """
        Calculate time to rent metrics.

        Args:
            data: Rental data DataFrame

        Returns:
            Dictionary with DOM and CDOM metrics
        """
        median_dom = data['Median DOM'].median()
        average_dom = data['Average DOM'].mean()
        median_cdom = data['Median CDOM'].median()
        average_cdom = data['Average CDOM'].mean()

        return {
            'median_dom': int(median_dom) if not pd.isna(median_dom) else None,
            'average_dom': int(average_dom) if not pd.isna(average_dom) else None,
            'median_cdom': int(median_cdom) if not pd.isna(median_cdom) else None,
            'average_cdom': int(average_cdom) if not pd.isna(average_cdom) else None
        }

    @staticmethod
    def generate_rental_summary(
        target_rent: float,
        rent_comparison: Dict,
        time_metrics: Dict,
        activity: Dict,
        subtype: Optional[str] = None
    ) -> str:
        """
        Generate natural language summary for rentals.

        Args:
            target_rent: User's target rent
            rent_comparison: Rent comparison metrics
            time_metrics: Time to rent metrics
            activity: Rental market activity metrics
            subtype: Rental property subtype

        Returns:
            Natural language summary string
        """
        median_diff = rent_comparison['median_diff_percent']
        median_rent = rent_comparison['median_rent']
        median_dom = time_metrics.get('median_dom')

        # Rent positioning
        if median_diff < -10:
            rent_msg = f"Your target rent of ${target_rent:,.0f}/month is **{abs(median_diff):.1f}% below** the market median of ${median_rent:,.0f}. This is very competitive for tenants."
        elif median_diff > 10:
            rent_msg = f"Your target rent of ${target_rent:,.0f}/month is **{median_diff:.1f}% above** the market median of ${median_rent:,.0f}. This may take longer to find tenants."
        else:
            rent_msg = f"Your target rent of ${target_rent:,.0f}/month is **well-aligned** with the market median of ${median_rent:,.0f} (within {abs(median_diff):.1f}%)."

        # Time to rent
        if median_dom:
            time_msg = f" Rentals typically get rented in **{median_dom} days** (median DOM)."
        else:
            time_msg = ""

        # Market activity
        subtype_msg = f" for {subtype} rentals" if subtype else ""
        activity_msg = f" In the last month, **{activity['rented_properties']} properties** were rented{subtype_msg}."

        return rent_msg + time_msg + activity_msg
