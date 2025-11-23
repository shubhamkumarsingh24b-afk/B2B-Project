import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

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

def generate_sample_data():
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

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 Crompton B2B AI Command Center</h1>', unsafe_allow_html=True)
    
    # Load data
    leads_df, customers_df = generate_sample_data()
    
    # Display dashboard
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
            # Lead score distribution using Streamlit's native chart
            st.write("**Lead Score Distribution**")
            st.bar_chart(filtered_leads['lead_score'].value_counts().sort_index())
        
        with col2:
            # Lead source analysis using Streamlit's native chart
            st.write("**Lead Source Distribution**")
            lead_source_counts = filtered_leads['lead_source'].value_counts()
            st.dataframe(lead_source_counts)
        
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
            # CLV by segment using Streamlit's native chart
            st.write("**CLV by Customer Segment**")
            segment_clv = filtered_customers.groupby('segment')['clv_predicted'].mean()
            st.bar_chart(segment_clv)
        
        with col2:
            # Churn probability distribution
            st.write("**Churn Risk Distribution**")
            st.bar_chart(filtered_customers['churn_probability'].value_counts().sort_index())
            
            # High risk indicator
            high_risk_count = len(filtered_customers[filtered_customers['churn_probability'] > 0.7])
            if high_risk_count > 0:
                st.error(f"🚨 {high_risk_count} customers at high churn risk!")
        
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
            
            if len(priority_leads) > 0:
                for _, lead in priority_leads.iterrows():
                    st.markdown(f"""
                    <div class="alert-high">
                        <strong>{lead['company']}</strong> - {lead['industry']}<br>
                        Score: {lead['lead_score']} | Contact: {lead['contact_title']}<br>
                        <em>Action: Assign to sales rep immediately</em>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("")
            else:
                st.info("No priority hot leads at the moment.")
        
        with col2:
            st.markdown("### ⚠️ High Churn Risk Customers")
            risk_customers = filtered_customers[filtered_customers['churn_probability'] > 0.7].head(5)
            
            if len(risk_customers) > 0:
                for _, customer in risk_customers.iterrows():
                    st.markdown(f"""
                    <div class="alert-medium">
                        <strong>{customer['company']}</strong> - {customer['segment']}<br>
                        Churn Risk: {customer['churn_probability']:.0%}<br>
                        <em>Action: Proactive retention outreach</em>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("")
            else:
                st.info("No high churn risk customers at the moment.")
    
    with tab4:
        st.subheader("📊 Marketing Performance Analytics")
        
        # Simulate performance metrics over time
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        conversion_rates = [7.5, 8.2, 8.8, 9.1, 9.5, 9.2]
        sales_cycle = [12.0, 11.5, 11.0, 10.8, 10.5, 10.2]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Lead Conversion Rate Trend (%)**")
            conversion_data = pd.DataFrame({
                'Month': months,
                'Conversion Rate': conversion_rates
            })
            st.line_chart(conversion_data.set_index('Month'))
        
        with col2:
            st.write("**Average Sales Cycle Length (Months)**")
            cycle_data = pd.DataFrame({
                'Month': months,
                'Sales Cycle': sales_cycle
            })
            st.line_chart(cycle_data.set_index('Month'))
        
        # Performance summary
        st.subheader("📈 Performance Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Conversion Rate", "9.2%", "+1.7%")
        
        with col2:
            st.metric("Current Sales Cycle", "10.2 months", "-1.8 months")
        
        with col3:
            st.metric("ROI Improvement", "22%", "+22%")
    
    # Footer
    st.markdown("---")
    st.markdown("**Crompton B2B AI Platform** | Real-time predictive analytics for smarter marketing decisions")

if __name__ == "__main__":
    main()
