import pandas as pd
from datetime import datetime, timedelta
import random

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

def load_data_from_csv():
    """Load data from CSV files"""
    try:
        leads_df = pd.read_csv('data/sample_leads.csv')
        customers_df = pd.read_csv('data/sample_customers.csv')
        
        # Convert date columns
        if 'last_activity' in leads_df.columns:
            leads_df['last_activity'] = pd.to_datetime(leads_df['last_activity'])
        if 'last_purchase' in customers_df.columns:
            customers_df['last_purchase'] = pd.to_datetime(customers_df['last_purchase'])
        
        return leads_df, customers_df
    except FileNotFoundError:
        # Generate and save sample data if files don't exist
        leads_df, customers_df = generate_sample_data()
        leads_df.to_csv('data/sample_leads.csv', index=False)
        customers_df.to_csv('data/sample_customers.csv', index=False)
        return leads_df, customers_df
