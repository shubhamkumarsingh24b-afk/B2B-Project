import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import random

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Try to import our utils, but provide fallbacks if they fail
try:
    from utils.data_loader import load_data_from_csv
    from utils.visualizations import (
        create_lead_score_histogram,
        create_lead_source_pie,
        create_clv_segment_box,
        create_churn_histogram,
        create_performance_trend
    )
    UTILS_AVAILABLE = True
except ImportError as e:
    st.warning(f"Utils module not available: {e}. Using fallback functions.")
    UTILS_AVAILABLE = False

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

# Fallback data generation if utils are not available
def generate_sample_data_fallback():
    """Generate realistic sample data for the B2B AI dashboard"""
    random.seed(42)
    
    # Lead data
    industries = ['Hospitality', 'Real Estate', 'Corporate', 'Healthcare', 'Education']
    lead_sources = ['Website', 'Referral', 'LinkedIn', 'Trade Show', 'Email Campaign']
    job_titles = ['Project Manager', 'Procurement Head', 'Architect', 'Facility Manager', 'CEO']
    
    leads = []
    for i in range(200):
        lead = {
            'id': f'LD{i:04d}',
            'company': f'Client {i+1}',
            'industry': random.choice(industries),
            'lead_source': random.choice(lead_sources),
            'contact_title': random.choice(job_titles),
            'lead_score': random.randint(10, 95),
            'engagement_level': random.choice(['High', 'Medium', 'Low']),
            'last_activity': datetime.now() - timedelta(days=random.randint(1, 90)),
            'status': random.choice(['New', 'Contacted', 'Qualified', 'Proposal Sent', 'Closed-Won', 'Closed-Lost'])
        }
        leads.append(lead)
    
    # Customer CLV data
    customers = []
    for i in range(100):
        customer = {
            'id': f'CUST{i:04d}',
            'company': f'Existing Client {i+1}',
            'industry': random.choice(industries),
            'total_spent': random.randint(500000, 5000000),
            'clv_predicted': random.randint(1000000, 10000000),
            'churn_probability': round(random.uniform(0.1, 0.8), 2),
            'segment': random.choice(['Platinum', 'Gold', 'Silver', 'Bronze']),
            'last_purchase': datetime.now() - timedelta(days=random.randint(1, 365))
        }
        customers.append(customer)
    
    return pd.DataFrame(leads), pd.DataFrame(customers)

# Fallback visualization functions
def create_lead_score_histogram_fallback(leads_df):
    """Create lead score distribution histogram"""
    import plotly.express as px
    fig = px.histogram(
        leads_df, 
        x='lead_score',
        title='Lead Score Distribution',
        nbins=20,
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(xaxis_title='Lead Score', yaxis_title='Count')
    return fig

def create_lead_source_pie_fallback(leads_df):
    """Create lead source distribution pie chart"""
    import plotly.express as px
    lead_source_counts = leads_df['lead_source'].value_counts()
    fig = px.pie(
        values=lead_source_counts.values,
        names=lead_source_counts.index,
        title='Lead Source Distribution'
    )
    return fig

def create_clv_segment_box_fallback(customers_df):
    """Create CLV distribution by segment box plot"""
    import plotly.express as px
    fig = px.box(
        customers_df,
        x='segment',
        y='clv_predicted',
        title='CLV Distribution by Customer Segment',
        color='segment'
    )
    fig.update_layout(yaxis_title='Predicted CLV (₹)')
    return fig

def create_churn_histogram_fallback(customers_df):
    """Create churn probability distribution histogram"""
    import plotly.express as px
    fig = px.histogram(
        customers_df,
        x='churn_probability',
        title='Customer Churn Probability Distribution',
        nbins=20,
        color_discrete_sequence=['#ff4444']
    )
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 Crompton B2B AI Command Center</h1>', unsafe_allow_html=True)
    
    try:
        # Load data
        if UTILS_AVAILABLE:
            leads_df, customers_df = load_data_from_csv()
        else:
            leads_df, customers_df = generate_sample_data_fallback()
            st.info("📊 Using generated sample data for demonstration.")
        
        # Display dashboard
        display_dashboard(leads_df, customers_df)
        
    except Exception as e:
        st.error(f"Error loading application: {e}")
        st.info("The app will run with basic generated data.")
        leads_df, customers_df = generate_sample_data_fallback()
        display_dashboard(leads_df, customers_df)

def display_dashboard(leads_df, customers_df):
    """Main dashboard display function"""
    
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
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_leads = len(filtered_leads)
        hot_leads = len(filtered_leads[filtered_leads['lead_score'] >= 80])
        st.metric("Total Leads", total_leads, f"{hot_leads} Hot Leads")
    
    with col2:
        avg_lead_score = filtered_leads['lead_score'].mean()
        st.metric("Avg Lead Score", f"{avg_lead_score:.1f}")
    
    with col3:
        high_value_customers = len(filtered_customers[filtered_customers['segment'].isin(['Platinum', 'Gold'])])
        st.metric("High-Value Customers", high_value_customers)
    
    with col4:
        at_risk_customers = len(filtered_customers[filtered_customers['churn_probability'] > 0.7])
        st.metric("At-Risk Customers", at_risk_customers)
    
    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Lead Intelligence", "💰 Customer Value", "🚨 Alerts & Actions", "📊 Performance"])
    
    with tab1:
        st.subheader("Lead Scoring & Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Lead score distribution
            if UTILS_AVAILABLE:
                fig_score = create_lead_score_histogram(filtered_leads)
            else:
                fig_score = create_lead_score_histogram_fallback(filtered_leads)
            st.plotly_chart(fig_score, use_container_width=True)
        
        with col2:
            # Lead source analysis
            if UTILS_AVAILABLE:
                fig_source = create_lead_source_pie(filtered_leads)
            else:
                fig_source = create_lead_source_pie_fallback(filtered_leads)
            st.plotly_chart(fig_source, use_container_width=True)
        
        # Hot leads table
        st.subheader("🔥 Hot Leads (Score ≥ 80)")
        hot_leads_table = filtered_leads[filtered_leads['lead_score'] >= 80][
            ['id', 'company', 'industry', 'contact_title', 'lead_score', 'status']
        ].sort_values('lead_score', ascending=False)
        
        st.dataframe(
            hot_leads_table,
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.subheader("Customer Lifetime Value & Segmentation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CLV by segment
            if UTILS_AVAILABLE:
                fig_clv = create_clv_segment_box(filtered_customers)
            else:
                fig_clv = create_clv_segment_box_fallback(filtered_customers)
            st.plotly_chart(fig_clv, use_container_width=True)
        
        with col2:
            # Churn probability distribution
            if UTILS_AVAILABLE:
                fig_churn = create_churn_histogram(filtered_customers)
            else:
                fig_churn = create_churn_histogram_fallback(filtered_customers)
            st.plotly_chart(fig_churn, use_container_width=True)
        
        # High-value customers table
        st.subheader("💎 High-Value Customers (Platinum & Gold)")
        high_value_table = filtered_customers[filtered_customers['segment'].isin(['Platinum', 'Gold'])][
            ['id', 'company', 'industry', 'segment', 'clv_predicted', 'churn_probability']
        ].sort_values('clv_predicted', ascending=False)
        
        st.dataframe(
            high_value_table,
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        st.subheader("🚨 Immediate Actions Required")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔥 Priority Hot Leads")
            priority_leads = filtered_leads[
                (filtered_leads['lead_score'] >= 80) & 
                (filtered_leads['status'].isin(['New', 'Contacted']))
            ].head(5)
            
            for _, lead in priority_leads.iterrows():
                st.markdown(f"""
                <div class="alert-high">
                    <strong>{lead['company']}</strong> - {lead['industry']}<br>
                    Score: {lead['lead_score']} | Contact: {lead['contact_title']}<br>
                    <em>Action: Assign to sales rep immediately</em>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
        
        with col2:
            st.markdown("### ⚠️ High Churn Risk Customers")
            risk_customers = filtered_customers[filtered_customers['churn_probability'] > 0.7].head(5)
            
            for _, customer in risk_customers.iterrows():
                st.markdown(f"""
                <div class="alert-medium">
                    <strong>{customer['company']}</strong> - {customer['segment']}<br>
                    Churn Risk: {customer['churn_probability']:.0%}<br>
                    <em>Action: Proactive retention outreach</em>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
    
    with tab4:
        st.subheader("📊 Marketing Performance Analytics")
        
        # Simulate performance metrics over time
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        conversion_rates = [7.5, 8.2, 8.8, 9.1, 9.5, 9.2]
        sales_cycle = [12.0, 11.5, 11.0, 10.8, 10.5, 10.2]
        
        col1, col2 = st.columns(2)
        
        with col1:
            import plotly.graph_objects as go
            fig_conversion = go.Figure()
            fig_conversion.add_trace(go.Scatter(
                x=months, y=conversion_rates,
                mode='lines+markers',
                name='Conversion Rate',
                line=dict(color='#2ecc71', width=3)
            ))
            fig_conversion.update_layout(
                title='Lead Conversion Rate Trend (%)',
                xaxis_title='Month',
                yaxis_title='Conversion Rate %'
            )
            st.plotly_chart(fig_conversion, use_container_width=True)
        
        with col2:
            fig_cycle = go.Figure()
            fig_cycle.add_trace(go.Scatter(
                x=months, y=sales_cycle,
                mode='lines+markers',
                name='Sales Cycle (Months)',
                line=dict(color='#e74c3c', width=3)
            ))
            fig_cycle.update_layout(
                title='Average Sales Cycle Length (Months)',
                xaxis_title='Month',
                yaxis_title='Months'
            )
            st.plotly_chart(fig_cycle, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Crompton B2B AI Platform** | Real-time predictive analytics for smarter marketing decisions")

if __name__ == "__main__":
    main()
