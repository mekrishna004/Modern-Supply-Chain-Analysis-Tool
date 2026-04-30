import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from modules import abc_analysis, forecasting, risk_analysis, optimization
import os

# Page Configuration
st.set_page_config(page_title="Supply Chain Analysis Tool", layout="wide", page_icon="📦")
st.title("📦 Modern Supply Chain Analysis Tool")
st.markdown("Analyze inventory, forecast demand, assess risks, and optimize operations.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data Ingestion", "ABC Analysis", "Demand Forecasting", "Risk Analysis", "Optimization", "Dashboard", "Reports", "Alerts"])

# Global data storage
if 'data' not in st.session_state:
    st.session_state.data = {}

# Helper functions
def load_data(file_obj):
    """Load CSV or Excel into a DataFrame."""
    if file_obj.name.endswith(".csv"):
        return pd.read_csv(file_obj)
    if file_obj.name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_obj)
    raise ValueError("Unsupported file type. Please upload CSV or Excel.")

def convert_potential_dates(dataframe):
    """Try converting object columns to datetime."""
    df_copy = dataframe.copy()
    for column in df_copy.columns:
        if df_copy[column].dtype == "object":
            converted = pd.to_datetime(df_copy[column], errors="coerce")
            if converted.notna().mean() > 0.7:
                df_copy[column] = converted
    return df_copy

# Data Ingestion Page
if page == "Data Ingestion":
    st.header("📁 Data Ingestion")
    st.markdown("Upload your supply chain data files (inventory, orders, suppliers).")

    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, type=["csv", "xlsx", "xls"])

    if uploaded_files:
        for file in uploaded_files:
            try:
                df = load_data(file)
                df = convert_potential_dates(df)
                st.session_state.data[file.name] = df
                st.success(f"Loaded {file.name}: {df.shape[0]} rows, {df.shape[1]} columns")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Error loading {file.name}: {e}")

    # Load sample data if not uploaded
    sample_files = ['inventory.csv', 'orders.csv', 'suppliers.csv', 'order_details.csv']
    for file in sample_files:
        if file not in st.session_state.data:
            try:
                df = pd.read_csv(f'data/{file}')
                df = convert_potential_dates(df)
                st.session_state.data[file] = df
                st.info(f"Loaded sample {file}: {df.shape[0]} rows, {df.shape[1]} columns")
            except FileNotFoundError:
                pass

# ABC Analysis Page
elif page == "ABC Analysis":
    st.header("🔤 ABC Analysis")
    if 'inventory.csv' in st.session_state.data:
        df = st.session_state.data['inventory.csv']
        abc_results = abc_analysis.perform_abc(df)
        st.subheader("ABC Classification Summary")
        st.dataframe(abc_results['summary'])
        st.subheader("Pareto Chart")
        st.plotly_chart(abc_results['pareto_chart'])
        st.subheader("Classified Inventory")
        st.dataframe(abc_results['classified_inventory'])
    else:
        st.warning("Please upload inventory.csv first.")

# Demand Forecasting Page
elif page == "Demand Forecasting":
    st.header("📈 Demand Forecasting")
    if 'orders.csv' in st.session_state.data:
        df = st.session_state.data['orders.csv']
        forecast_results = forecasting.forecast_demand(df)
        st.subheader("Forecast Chart")
        st.plotly_chart(forecast_results['chart'])
        st.subheader("Forecasted Values")
        st.dataframe(forecast_results['forecast'])
    else:
        st.warning("Please upload orders.csv first.")

# Risk Analysis Page
elif page == "Risk Analysis":
    st.header("⚠️ Risk Analysis")
    risk_results = risk_analysis.analyze_risks(st.session_state.data)
    st.subheader("Identified Risks")
    for risk in risk_results['identified_risks']:
        st.write(f"- {risk}")
    st.subheader("Recommendations")
    for rec in risk_results['recommendations']:
        st.write(f"- {rec}")

# Optimization Page
elif page == "Optimization":
    st.header("🎯 Optimization")
    if 'inventory.csv' in st.session_state.data:
        opt_results = optimization.optimize_inventory(st.session_state.data)
        if isinstance(opt_results, dict):
            st.subheader("Optimization Results")
            st.dataframe(opt_results['optimized_inventory'])
            st.write(opt_results['summary'])
        else:
            st.error(opt_results)
    else:
        st.warning("Please upload inventory.csv first.")

# Dashboard Page
elif page == "Dashboard":
    st.header("📊 Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    if 'inventory.csv' in st.session_state.data:
        inv_df = st.session_state.data['inventory.csv']
        total_items = len(inv_df)
        total_value = (inv_df['annual_demand'] * inv_df['unit_cost']).sum()
        avg_stock = inv_df['current_stock'].mean()
        col1.metric("Total Items", total_items)
        col2.metric("Total Inventory Value", f"${total_value:,.0f}")
        col3.metric("Avg Stock Level", f"{avg_stock:.0f}")

    if 'order_details.csv' in st.session_state.data:
        ord_df = st.session_state.data['order_details.csv']
        total_orders = len(ord_df)
        on_time_rate = ord_df['on_time'].mean() * 100
        total_order_value = ord_df['total_cost'].sum()
        col4.metric("On-Time Delivery", f"{on_time_rate:.1f}%")

    # Charts
    if 'orders.csv' in st.session_state.data:
        ord_df = st.session_state.data['orders.csv']
        ord_df['date'] = pd.to_datetime(ord_df['date'])
        monthly_demand = ord_df.set_index('date').resample('ME')['demand'].sum()
        st.subheader("Monthly Demand Trend")
        st.line_chart(monthly_demand)

    if 'suppliers.csv' in st.session_state.data:
        sup_df = st.session_state.data['suppliers.csv']
        st.subheader("Supplier Reliability")
        st.bar_chart(sup_df.set_index('supplier')['reliability_score'])

# Reports Page
elif page == "Reports":
    st.header("📄 Reports")
    report_type = st.selectbox("Select Report", ["ABC Analysis", "Forecast", "Risks", "Optimization"])
    if st.button("Generate Report"):
        if report_type == "ABC Analysis" and 'inventory.csv' in st.session_state.data:
            abc_results = abc_analysis.perform_abc(st.session_state.data['inventory.csv'])
            csv = abc_results['classified_inventory'].to_csv(index=False)
            st.download_button("Download ABC Report", csv, "abc_report.csv", "text/csv")
        elif report_type == "Forecast" and 'orders.csv' in st.session_state.data:
            forecast_results = forecasting.forecast_demand(st.session_state.data['orders.csv'])
            csv = forecast_results['forecast'].to_csv(index=False)
            st.download_button("Download Forecast Report", csv, "forecast_report.csv", "text/csv")
        else:
            st.warning("Required data not uploaded.")

# Alerts Page
elif page == "Alerts":
    st.header("🚨 Alerts")
    if 'inventory.csv' in st.session_state.data:
        inv_df = st.session_state.data['inventory.csv']
        low_stock_threshold = st.slider("Low Stock Threshold", 0, 100, 20)
        low_stock_items = inv_df[inv_df['current_stock'] < low_stock_threshold]
        if not low_stock_items.empty:
            st.error(f"Low stock alert: {len(low_stock_items)} items below {low_stock_threshold}")
            st.dataframe(low_stock_items[['item', 'current_stock']])
        else:
            st.success("All items above stock threshold.")
    else:
        st.warning("Upload inventory data for alerts.")