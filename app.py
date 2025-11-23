import streamlit as st
import pandas as pd
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.data_loader import load_data_from_csv
from utils.visualizations import (
    create_lead_score_histogram,
    create_lead_source_pie,
    create_clv_segment_box,
    create_churn_histogram,
    create_performance_trend
)

# Page configuration
st.set_page_config(
    page_title="Crompton B2B AI Command Center",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .alert-high {
        background-color: #ffcccc;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ff4444;
    }
    .alert-medium {
        background-color: #fff4cc;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ffaa00;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 Crompton B2B AI Command Center</h1>', unsafe_allow_html=True)
    
    # Load data
    leads_df, customers_df = load_data_from_csv()
    
    # Sidebar filters
    st.sidebar.header("🔧 Dashboard Filters")
    
    selected_industry = st.sidebar.multiselect(
        "Select Industries:",
        options=leads_df['industry'].unique(),
        default=leads_df['industry'].unique()
    )
    
    min_score, max_score = st.sidebar.slider(
        "Lead Score Range:",
        min_value=0,
        max_value=100,
        value=(50, 100)
    )
    
    # Filter data
    filtered_leads = leads_df[
        (leads_df['industry'].isin(selected_industry)) & 
        (leads_df['lead_score'] >= min_score) & 
        (leads_df['lead_score'] <= max_score)
    ]
    
    filtered_customers = customers_df[
        customers_df['industry'].isin(selected_industry)
    ]
    
    # Display dashboard content (same as previous code)
    display_dashboard(filtered_leads, filtered_customers)

def display_dashboard(leads_df, customers_df):
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_leads = len(leads_df)
        hot_leads = len(leads_df[leads_df['lead_score'] >= 80])
        st.metric("Total Leads", total_leads, f"{hot_leads} Hot Leads")
    
    with col2:
        avg_lead_score = leads_df['lead_score'].mean()
        st.metric("Avg Lead Score", f"{avg_lead_score:.1f}")
    
    with col3:
        high_value_customers = len(customers_df[customers_df['segment'].isin(['Platinum', 'Gold'])])
        st.metric("High-Value Customers", high_value_customers)
    
    with col4:
        at_risk_customers = len(customers_df[customers_df['churn_probability'] > 0.7])
        st.metric("At-Risk Customers", at_risk_customers)
    
    # Rest of your existing dashboard code here...
    # [Include all the tab content from the previous implementation]

if __name__ == "__main__":
    main()
