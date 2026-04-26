import pandas as pd
import numpy as np
import math

def optimize_inventory(data_dict):
    """
    Optimize inventory using EOQ model.
    Assumes inventory has 'annual_demand', 'unit_cost', 'holding_cost_rate', 'ordering_cost'
    """
    if 'inventory.csv' not in data_dict:
        return "Error: Inventory data required for optimization."

    inv_df = data_dict['inventory.csv']
    required_cols = ['annual_demand', 'unit_cost', 'holding_cost_rate', 'ordering_cost']
    if not all(col in inv_df.columns for col in required_cols):
        return f"Error: Missing columns: {required_cols}"

    df = inv_df.copy()
    df['EOQ'] = np.sqrt((2 * df['annual_demand'] * df['ordering_cost']) / (df['unit_cost'] * df['holding_cost_rate']))
    df['total_holding_cost'] = (df['EOQ'] / 2) * df['unit_cost'] * df['holding_cost_rate']
    df['total_ordering_cost'] = (df['annual_demand'] / df['EOQ']) * df['ordering_cost']
    df['total_cost'] = df['total_holding_cost'] + df['total_ordering_cost']

    return {
        'optimized_inventory': df[['item', 'EOQ', 'total_cost']],
        'summary': f"Average EOQ: {df['EOQ'].mean():.0f}, Total cost savings potential: {df['total_cost'].sum():.2f}"
    }