# Real Estate Market Insights Demo

An interactive Streamlit application that enables users to compare their target house or condo price or rent against detailed historical market sales and rental data.

## Features

### Sales Market Insights
- **Price Comparison**: Compare target price with median and average sold prices
- **Market Activity Summary**: Active listings, conditional sales, and sold properties
- **Time to Sell Estimation**: Median and average Days on Market (DOM) and Cumulative DOM (CDOM)
- **Trend Visualization**: Price trends over time for selected property subtype
- **Natural Language Summary**: Plain-language explanation of price positioning

### Rental Market Insights
- **Rent Comparison**: Compare target rent with market median and average
- **Rental Market Activity**: Active rental listings and rented properties
- **Time to Rent Estimation**: Median and average DOM and CDOM for rentals
- **Rental Property Type Breakdown**: Distribution over time
- **Trend Visualization**: Rent price trends by property type

## Project Structure

```
real_estate_demo/
├── venv/                          # Virtual environment
├── data/
│   └── market_data.xlsx           # Market data source
├── src/
│   ├── data_loader.py            # Data loading and preprocessing
│   ├── analytics.py              # Core analytics calculations
│   └── visualizations.py         # Plotly chart generation
├── app.py                        # Main Streamlit application
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## Installation

1. **Ensure virtual environment is activated:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser and navigate to:**
   - Local URL: http://localhost:8501

3. **Use the sidebar to configure your analysis:**
   - Select market segment (Sales or Rental, Freehold or Condo)
   - Choose property subtype (Detached, Semi, Apartment, etc.)
   - Enter your target price or rent
   - Select timeframe filter

4. **View insights:**
   - Key metrics dashboard
   - Natural language market summary
   - Interactive Plotly charts showing trends and comparisons

## Market Segments

### Sales - Freehold
- **Subtypes**: Detached, Row, Semi
- **Metrics**: Sold prices, DOM, CDOM, market activity

### Sales - Condo
- **Subtypes**: Apartment, Apartment (old), Townhome, Stacked, Other
- **Metrics**: Sold prices, DOM, CDOM, market activity

### Rental - Freehold
- **Subtypes**: Detached, Row, Semi
- **Metrics**: Rent prices, DOM, CDOM, rental activity

### Rental - Condo
- **Subtypes**: Apartment, Detached, Row
- **Metrics**: Rent prices, DOM, CDOM, rental activity

## Data Source

The application uses `data/market_data.xlsx` with the following sheets:
- Freehold (sales data)
- Condos (sales data)
- Freehold Sales By Property Type
- Condo Sales By Property Type
- Rental Data (Freehold)
- Rental Type (Freehold)
- Rental Data (Condo)
- Rental Type (Condo)

## Key Technologies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **OpenPyXL**: Excel file reading

## Developer Notes

### Data Loading
- Data is cached using `@st.cache_data` for optimal performance
- All sheets are preloaded on app startup
- Date parsing is handled automatically

### Analytics
- Sales and rental analytics are separated into distinct classes
- Natural language summaries are generated based on price/rent positioning
- Percentage differences are calculated relative to market median

### Visualizations
- All charts are interactive Plotly figures
- Responsive sizing for different screen sizes
- Consistent color scheme across visualizations

## License

This is a demo application for real estate market insights.
