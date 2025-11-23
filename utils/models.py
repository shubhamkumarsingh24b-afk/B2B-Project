import random

class B2BPredictiveModels:
    """Mock ML models for B2B lead scoring and CLV prediction"""
    
    def __init__(self):
        self.lead_scoring_model = None
        
    def predict_lead_score(self, lead_data):
        """Predict lead score for new data"""
        # Return mock scores for demo
        return random.randint(20, 95)
    
    def calculate_clv(self, customer_data):
        """Calculate Customer Lifetime Value"""
        # Simplified CLV calculation for demo
        avg_order_value = customer_data.get('avg_order_value', 500000)
        purchase_freq = customer_data.get('purchase_frequency', 2)
        customer_lifespan = customer_data.get('lifespan_years', 3)
        profit_margin = 0.25
        
        clv = avg_order_value * purchase_freq * customer_lifespan * profit_margin
        return clv
    
    def predict_churn_probability(self, customer_data):
        """Predict churn probability"""
        # Mock churn prediction based on recency and frequency
        recency_days = customer_data.get('days_since_last_purchase', 90)
        purchase_freq = customer_data.get('purchase_frequency', 2)
        
        # Simple heuristic: higher recency and lower frequency = higher churn risk
        churn_prob = min(0.9, (recency_days / 365) * (1 / max(1, purchase_freq)))
        return churn_prob
