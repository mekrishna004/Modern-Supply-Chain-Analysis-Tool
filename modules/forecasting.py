import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go

def forecast_demand(orders_df):
    """
    Forecast demand using ARIMA.
    Assumes columns: 'date', 'demand'
    """
    if 'date' not in orders_df.columns or 'demand' not in orders_df.columns:
        return "Error: Orders data must have 'date' and 'demand' columns."

    df = orders_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    df = df.resample('ME')['demand'].sum()  # Monthly aggregation

    # Fit ARIMA model
    model = ARIMA(df, order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast next 12 months
    forecast = model_fit.forecast(steps=12)
    forecast_index = pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), periods=12, freq='ME')

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.values, mode='lines', name='Historical'))
    fig.add_trace(go.Scatter(x=forecast_index, y=forecast, mode='lines', name='Forecast', line=dict(dash='dash')))
    fig.update_layout(title="Demand Forecast", xaxis_title="Date", yaxis_title="Demand")

    return {
        'model_summary': model_fit.summary(),
        'forecast': pd.DataFrame({'date': forecast_index, 'forecasted_demand': forecast}),
        'chart': fig
    }