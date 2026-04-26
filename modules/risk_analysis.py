import pandas as pd
import numpy as np

def analyze_risks(data_dict):
    """
    Analyze supply chain risks.
    """
    risks = []

    if 'inventory.csv' in data_dict:
        inv_df = data_dict['inventory.csv']
        if 'current_stock' in inv_df.columns and 'safety_stock' in inv_df.columns:
            low_stock = inv_df[inv_df['current_stock'] < inv_df['safety_stock']]
            risks.append(f"Low stock items: {len(low_stock)}")

    if 'suppliers.csv' in data_dict:
        sup_df = data_dict['suppliers.csv']
        if 'lead_time' in sup_df.columns:
            avg_lead = sup_df['lead_time'].mean()
            var_lead = sup_df['lead_time'].std()
            risks.append(f"Average lead time: {avg_lead:.1f} days, Variability: {var_lead:.1f}")

    if 'order_details.csv' in data_dict:
        ord_df = data_dict['order_details.csv']
        if 'on_time' in ord_df.columns:
            on_time_rate = ord_df['on_time'].mean() * 100
            risks.append(f"On-time delivery rate: {on_time_rate:.1f}%")

    return {
        'identified_risks': risks,
        'recommendations': ["Increase safety stock for low items", "Diversify suppliers with high variability", "Monitor delivery performance"]
    }