# Modern Supply Chain Analysis Tool

A comprehensive tool for supply chain analysis built with Python and Streamlit.

## Features

- **Data Ingestion**: Upload CSV/Excel files or connect to databases
- **ABC Analysis**: Classify inventory into A/B/C categories
- **Demand Forecasting**: Predict future demand using ARIMA models
- **Risk Analysis**: Identify supply chain risks and vulnerabilities
- **Optimization**: Calculate Economic Order Quantity (EOQ) for inventory
- **Dashboard**: Interactive visualizations of KPIs
- **Reports**: Generate exportable reports
- **Alerts**: Threshold-based notifications

## Installation

1. Clone or download the project
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Usage

1. Upload your data files (inventory.csv, orders.csv, suppliers.csv)
2. Navigate through the analysis modules
3. View results and visualizations
4. Generate reports

## Sample Data

Sample data files are provided in the `data/` folder for testing:

- `inventory.csv`: 20 items with demand, cost, and inventory details
- `orders.csv`: 4 years of monthly demand data
- `suppliers.csv`: 15 suppliers with lead times and reliability scores
- `order_details.csv`: 24 detailed orders with item, supplier, and delivery info

## Technologies

- Streamlit for UI
- Pandas for data manipulation
- DuckDB for SQL queries
- Plotly for visualizations
- Statsmodels for forecasting
