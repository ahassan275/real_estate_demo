"""
Data loading and preprocessing for real estate market data.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


class RealEstateDataLoader:
    """Handles loading and preprocessing of real estate market data."""

    def __init__(self, excel_path: str):
        """Initialize data loader with Excel file path."""
        self.excel_path = excel_path
        self._data_cache = {}

    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """Load all sheets from Excel file into a dictionary."""
        if not self._data_cache:
            xls = pd.ExcelFile(self.excel_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                # Parse dates
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                self._data_cache[sheet_name] = df
        return self._data_cache

    def get_sales_data(self, property_type: str) -> pd.DataFrame:
        """
        Get sales data for Freehold or Condo.

        Args:
            property_type: 'Freehold' or 'Condo'

        Returns:
            DataFrame with sales data
        """
        data = self.load_all_sheets()
        if property_type == 'Freehold':
            return data['Freehold'].copy()
        elif property_type == 'Condo':
            df = data['Condos'].copy()
            # Standardize column name (Condos sheet has 'Average Sold Prices' vs 'Average Sold Price')
            if 'Average Sold Prices' in df.columns:
                df.rename(columns={'Average Sold Prices': 'Average Sold Price'}, inplace=True)
            return df
        else:
            raise ValueError(f"Invalid property type: {property_type}")

    def get_sales_by_subtype(self, property_type: str) -> pd.DataFrame:
        """
        Get sales breakdown by property subtype.

        Args:
            property_type: 'Freehold' or 'Condo'

        Returns:
            DataFrame with property type breakdown
        """
        data = self.load_all_sheets()
        if property_type == 'Freehold':
            return data['Freehold Sales By Property Type'].copy()
        elif property_type == 'Condo':
            return data['Condo Sales By Property Type'].copy()
        else:
            raise ValueError(f"Invalid property type: {property_type}")

    def get_rental_data(self, property_type: str) -> pd.DataFrame:
        """
        Get rental market data.

        Args:
            property_type: 'Freehold' or 'Condo'

        Returns:
            DataFrame with rental data
        """
        data = self.load_all_sheets()
        if property_type == 'Freehold':
            df = data['Rental Data (Freehold)'].copy()
        elif property_type == 'Condo':
            df = data['Rental Data (Condo)'].copy()
        else:
            raise ValueError(f"Invalid property type: {property_type}")

        # Standardize column name
        if 'Average Rent Prices' in df.columns:
            df.rename(columns={'Average Rent Prices': 'Average Rent Price'}, inplace=True)
        return df

    def get_rental_by_subtype(self, property_type: str) -> pd.DataFrame:
        """
        Get rental breakdown by property subtype.

        Args:
            property_type: 'Freehold' or 'Condo'

        Returns:
            DataFrame with rental type breakdown
        """
        data = self.load_all_sheets()
        if property_type == 'Freehold':
            return data['Rental Type (Freehold)'].copy()
        elif property_type == 'Condo':
            df = data['Rental Type (Condo)'].copy()
            # Fix: First column 'Condo' contains dates, rename it to 'Date'
            if 'Condo' in df.columns and 'Date' not in df.columns:
                df.rename(columns={'Condo': 'Date'}, inplace=True)
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            return df
        else:
            raise ValueError(f"Invalid property type: {property_type}")

    def filter_by_timeframe(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """
        Filter dataframe by timeframe.

        Args:
            df: DataFrame with 'Date' column
            timeframe: One of 'last_3_months', 'last_6_months', 'since_2023', 'all'

        Returns:
            Filtered DataFrame
        """
        if timeframe == 'all' or 'Date' not in df.columns:
            return df

        # Get the most recent date in the data
        max_date = df['Date'].max()

        if timeframe == 'last_3_months':
            cutoff_date = max_date - timedelta(days=90)
        elif timeframe == 'last_6_months':
            cutoff_date = max_date - timedelta(days=180)
        elif timeframe == 'since_2023':
            cutoff_date = pd.to_datetime('2023-01-01')
        else:
            return df

        return df[df['Date'] >= cutoff_date].copy()

    def get_available_subtypes(self, property_type: str, market_segment: str) -> list:
        """
        Get available property subtypes for a given property type and market segment.

        Args:
            property_type: 'Freehold' or 'Condo'
            market_segment: 'Sales' or 'Rental'

        Returns:
            List of available subtypes
        """
        if market_segment == 'Sales':
            df = self.get_sales_by_subtype(property_type)
        else:  # Rental
            df = self.get_rental_by_subtype(property_type)

        # Get all columns except 'Date' and total columns
        columns = [col for col in df.columns
                  if col not in ['Date', 'Total - Freehold', 'Total Condo', 'Total', 'Condo']]

        # Clean up column names (remove trailing spaces)
        columns = [col.strip() for col in columns]

        return columns
