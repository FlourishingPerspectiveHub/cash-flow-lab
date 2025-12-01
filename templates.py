"""
Templates for Working Capital Navigator
Example business templates for quick start
"""

def get_example_templates():
    """Pre-filled example templates for different business types."""
    return {
        "Typical Business": {
            "description": "Standard business - customize as needed",
            "num_months": 12,
            "opening_cash": 100000,
            "revenue": 100000,
            "cogs_pct": 0.60,
            "opex": 20000,
            "ar_days": 45,
            "ap_days": 30,
            "inventory_days": 60,
            "capex": 3000,
            "depreciation": 3000,
            "price_increase": 0.02,
            "tax_rate": 0.25,
            "has_term": True,
            "term_amount": 50000,
            "term_rate": 0.06,
            "term_months": 60
        },
        
        "Retail Store": {
            "description": "High inventory, fast AR collection",
            "num_months": 12,
            "opening_cash": 75000,
            "revenue": 150000,
            "cogs_pct": 0.65,
            "opex": 30000,
            "ar_days": 15,
            "ap_days": 30,
            "inventory_days": 90,
            "capex": 3000,
            "depreciation": 3000,
            "price_increase": 0.02,
            "tax_rate": 0.25,
            "has_term": True,
            "term_amount": 50000,
            "term_rate": 0.065,
            "term_months": 84
        },
        
        "SaaS Startup": {
            "description": "Low COGS, high growth potential",
            "num_months": 12,
            "opening_cash": 200000,
            "revenue": 80000,
            "cogs_pct": 0.20,
            "opex": 50000,
            "ar_days": 60,
            "ap_days": 30,
            "inventory_days": 0,
            "capex": 5000,
            "depreciation": 5000,
            "price_increase": 0.03,
            "tax_rate": 0.25,
            "has_term": True,
            "term_amount": 100000,
            "term_rate": 0.08,
            "term_months": 48
        },
        
        "Manufacturing": {
            "description": "Extended payment terms, high inventory",
            "num_months": 12,
            "opening_cash": 150000,
            "revenue": 250000,
            "cogs_pct": 0.70,
            "opex": 35000,
            "ar_days": 60,
            "ap_days": 45,
            "inventory_days": 75,
            "capex": 10000,
            "depreciation": 10000,
            "price_increase": 0.02,
            "tax_rate": 0.25,
            "has_term": True,
            "term_amount": 200000,
            "term_rate": 0.055,
            "term_months": 120
        }
    }