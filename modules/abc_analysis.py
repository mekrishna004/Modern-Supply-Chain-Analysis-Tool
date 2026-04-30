import pandas as pd
import plotly.express as px

def perform_abc(inventory_df):
    """
    Perform ABC analysis on inventory data.
    Assumes columns: 'item', 'annual_demand', 'unit_cost'
    """
    if 'annual_demand' not in inventory_df.columns or 'unit_cost' not in inventory_df.columns:
        return "Error: Inventory data must have 'annual_demand' and 'unit_cost' columns."

    df = inventory_df.copy()
    df['annual_value'] = df['annual_demand'] * df['unit_cost']
    df = df.sort_values('annual_value', ascending=False)
    df['cumulative_value'] = df['annual_value'].cumsum()
    total_value = df['annual_value'].sum()
    df['cumulative_percentage'] = (df['cumulative_value'] / total_value) * 100

    def classify(row):
        if row['cumulative_percentage'] <= 80:
            return 'A'
        elif row['cumulative_percentage'] <= 95:
            return 'B'
        else:
            return 'C'

    df['category'] = df.apply(classify, axis=1)

    # Summary
    summary = df.groupby('category').agg({
        'annual_value': 'sum',
        'item': 'count'
    }).rename(columns={'item': 'item_count'})

    # Create Pareto chart with color differentiation by category
    color_map = {
        'A': '#00D084',  # Green for high-value items
        'B': '#FF9F1C',  # Orange for medium-value items
        'C': '#E74C3C'   # Red for low-value items
    }
    
    pareto_chart = px.bar(
        df, 
        x='item', 
        y='annual_value',
        color='category',
        color_discrete_map=color_map,
        title="ABC Inventory Analysis - Pareto Chart",
        labels={'item': 'Item', 'annual_value': 'Annual Value ($)', 'category': 'Category'},
        hover_data={'cumulative_percentage': ':.1f', 'item': True, 'annual_value': ':$.0f'}
    )
    
    pareto_chart.update_layout(
        xaxis_tickangle=-45,
        showlegend=True,
        hovermode='x unified',
        height=500
    )

    return {
        'classified_inventory': df,
        'summary': summary,
        'pareto_chart': pareto_chart
    }