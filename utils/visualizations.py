import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_lead_score_histogram(leads_df):
    """Create lead score distribution histogram"""
    fig = px.histogram(
        leads_df, 
        x='lead_score',
        title='Lead Score Distribution',
        nbins=20,
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(xaxis_title='Lead Score', yaxis_title='Count')
    return fig

def create_lead_source_pie(leads_df):
    """Create lead source distribution pie chart"""
    lead_source_counts = leads_df['lead_source'].value_counts()
    fig = px.pie(
        values=lead_source_counts.values,
        names=lead_source_counts.index,
        title='Lead Source Distribution'
    )
    return fig

def create_clv_segment_box(customers_df):
    """Create CLV distribution by segment box plot"""
    fig = px.box(
        customers_df,
        x='segment',
        y='clv_predicted',
        title='CLV Distribution by Customer Segment',
        color='segment'
    )
    fig.update_layout(yaxis_title='Predicted CLV (₹)')
    return fig

def create_churn_histogram(customers_df):
    """Create churn probability distribution histogram"""
    fig = px.histogram(
        customers_df,
        x='churn_probability',
        title='Customer Churn Probability Distribution',
        nbins=20,
        color_discrete_sequence=['#ff4444']
    )
    fig.add_vline(x=0.7, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
    return fig

def create_performance_trend(months, values, title, y_axis_title, color):
    """Create performance trend line chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=values,
        mode='lines+markers',
        name=title,
        line=dict(color=color, width=3)
    ))
    fig.update_layout(
        title=title,
        xaxis_title='Month',
        yaxis_title=y_axis_title
    )
    return fig
