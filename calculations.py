"""
calculations.py
"""

import pandas as pd
import numpy as np


def calculate_wc_components(revenue, cogs_pct, ar_days, ap_days, inventory_days):
    """Calculate dollar amounts for AR, Inventory, and AP based on days."""
    cogs = revenue * cogs_pct
    
    # Note: Uses 30-day month convention (360-day year) standard in corporate finance.
    ar = (revenue / 30) * ar_days
    inventory = (cogs / 30) * inventory_days
    ap = (cogs / 30) * ap_days
    
    return {'ar': ar, 'inventory': inventory, 'ap': ap}


def calculate_ebit(revenue, cogs_pct, opex):
    """Calculate EBIT (Earnings Before Interest and Tax)."""
    cogs = revenue * cogs_pct
    ebit = revenue - cogs - opex
    return ebit


def calculate_working_capital(ar, inventory, ap):
    """Calculate Working Capital."""
    return (ar + inventory) - ap


def calculate_delta_wc(wc_current, wc_previous):
    """Calculate change in Working Capital."""
    if wc_previous is None:
        return wc_current
    return wc_current - wc_previous


def calculate_fcf(ebit, tax_rate, depreciation, capex, delta_wc):
    """Calculate Free Cash Flow."""
    nopat = ebit * (1 - tax_rate)
    fcf = nopat + depreciation - capex - delta_wc
    return fcf

# Note: Uses present value (PV) formula to calculate remaining balance independently each month.
# This approach prioritizes code simplicity and readability for educational purposes.
def calculate_debt_service(debt_params, month):
    """
    Calculate monthly debt service (interest + principal).
    
    Returns dict with:
    - interest_expense: Monthly interest payment
    - principal_payment: Monthly principal payment
    - remaining_balance: Remaining loan balance
    """
    if debt_params is None or month > debt_params['term_months']:
        return {'interest_expense': 0, 'principal_payment': 0, 'remaining_balance': 0}
    
    # Calculate remaining balance
    monthly_rate = debt_params['interest_rate'] / 12
    months_remaining = debt_params['term_months'] - month + 1
    
    if months_remaining <= 0:
        return {'interest_expense': 0, 'principal_payment': 0, 'remaining_balance': 0}
    
    # Handle 0% interest case
    if monthly_rate == 0:
        remaining_balance = debt_params['loan_amount'] - (debt_params['monthly_payment'] * (month - 1))
        interest_expense = 0
        principal_payment = debt_params['monthly_payment']
        
        return {
            'interest_expense': interest_expense,
            'principal_payment': principal_payment,
            'remaining_balance': max(0, remaining_balance)
        }
    
    # Standard amortization with interest
    # Remaining balance formula
    remaining_balance = debt_params['monthly_payment'] * ((1 - (1 + monthly_rate)**(-months_remaining)) / monthly_rate)
    
    # Interest for this month
    prev_balance = debt_params['monthly_payment'] * ((1 - (1 + monthly_rate)**(-(months_remaining + 1))) / monthly_rate) if month > 1 else debt_params['loan_amount']
    interest_expense = prev_balance * monthly_rate
    
    # Principal = Total payment - Interest
    principal_payment = debt_params['monthly_payment'] - interest_expense
    
    return {
        'interest_expense': interest_expense,
        'principal_payment': principal_payment,
        'remaining_balance': remaining_balance
    }


def calculate_tier1_metrics(revenue, ebit, ar, inventory, ap, cash_balance, opex):
    """
    Calculate Tier 1 financial metrics.
    
    Returns dict with:
    - current_ratio: Current Assets / Current Liabilities
    - quick_ratio: (Current Assets - Inventory) / Current Liabilities
    - days_cash_on_hand: Cash Balance / (OPEX per day)
    - operating_margin: EBIT / Revenue
    """
    current_assets = ar + inventory + cash_balance
    current_liabilities = ap if ap > 0 else 1  # Avoid division by zero
    
    current_ratio = current_assets / current_liabilities
    quick_ratio = (current_assets - inventory) / current_liabilities
    days_cash_on_hand = (cash_balance / (opex / 30)) if opex > 0 else 0
    operating_margin = (ebit / revenue * 100) if revenue > 0 else 0
    
    return {
        'current_ratio': current_ratio,
        'quick_ratio': quick_ratio,
        'days_cash_on_hand': days_cash_on_hand,
        'operating_margin': operating_margin
    }


def apply_scenario_adjustments(base_inputs, scenario_type):
    """Apply scenario adjustments to base inputs."""
    adjusted = base_inputs.copy()
    
    if scenario_type == 'base':
        return adjusted
    
    elif scenario_type == 'conservative':
        adjusted['ar_days'] = base_inputs['ar_days'] + 10
        adjusted['ap_days'] = max(0, base_inputs['ap_days'] - 5)
        adjusted['inventory_days'] = base_inputs['inventory_days'] * 1.15
        
    elif scenario_type == 'aggressive':
        adjusted['ar_days'] = max(0, base_inputs['ar_days'] - 10)
        adjusted['ap_days'] = base_inputs['ap_days'] + 10
        adjusted['inventory_days'] = base_inputs['inventory_days'] * 0.85
    
    return adjusted


def generate_monthly_projections(inputs, num_months, debt_params=None):
    """Generate monthly financial projections with optional debt modeling."""
    results = []
    
    # Get base values and increase rates
    base_revenue = inputs['revenue']
    price_increase = inputs.get('price_increase', 0)
    
    base_cogs_pct = inputs['cogs_pct']
    cogs_increase = inputs.get('cogs_increase', 0)
    
    base_opex = inputs['opex']
    opex_increase = inputs.get('opex_increase', 0)
    
    # Initialize with steady-state WC (business already operating)
    initial_wc = calculate_wc_components(base_revenue, base_cogs_pct,
                                        inputs['ar_days'], inputs['ap_days'], inputs['inventory_days'])
    wc_previous = calculate_working_capital(initial_wc['ar'], initial_wc['inventory'], initial_wc['ap'])
    ar_previous = initial_wc['ar']
    inventory_previous = initial_wc['inventory']
    ap_previous = initial_wc['ap']
    
    # Track cash balance
    opening_cash = inputs.get('opening_cash', 0)
    cash_balance = opening_cash
    
    # Generate Month 0 (current/baseline) through Month num_months
    for month in range(0, num_months + 1):
        # Apply price increase (compound growth)
        current_revenue = base_revenue * ((1 + price_increase) ** month)
        
        # Apply COGS% increase (compound growth)
        current_cogs_pct = base_cogs_pct * ((1 + cogs_increase) ** month)
        current_cogs_pct = min(current_cogs_pct, 0.95)  # Cap at 95%
        
        # Apply OPEX increase (compound growth)
        current_opex = base_opex * ((1 + opex_increase) ** month)
        
        # Calculate debt service if applicable (starts at month 1)
        debt_service = calculate_debt_service(debt_params, month) if month > 0 else {
            'interest_expense': 0, 'principal_payment': 0, 'remaining_balance': 
            debt_params['loan_amount'] if debt_params else 0
        }
        
        # Calculate EBIT (before interest)
        ebit = calculate_ebit(current_revenue, current_cogs_pct, current_opex)
        
        # EBIT after interest (EBIT - Interest Expense)
        ebit_after_interest = ebit - debt_service['interest_expense']
        ebit_after_tax = ebit_after_interest * (1 - inputs['tax_rate'])
        
        # Calculate COGS for gross margin
        cogs = current_revenue * current_cogs_pct
        gross_margin = ((current_revenue - cogs) / current_revenue * 100) if current_revenue > 0 else 0
        
        # Calculate WC components
        wc_components = calculate_wc_components(
            current_revenue,
            current_cogs_pct,
            inputs['ar_days'],
            inputs['ap_days'],
            inputs['inventory_days']
        )
        
        # Calculate WC
        wc = calculate_working_capital(
            wc_components['ar'],
            wc_components['inventory'],
            wc_components['ap']
        )
        
        # Month 0 represents baseline/current state - business already operating at steady state.
        # No working capital change occurs in Month 0 as it's a snapshot, not a projection period.
        # ΔWC calculations begin in Month 1 when comparing against this baseline.
        # Calculate ΔWC and component changes (zero for month 0)
        if month == 0:
            delta_wc = 0
            delta_ar = 0
            delta_inventory = 0
            delta_ap = 0
        else:
            delta_wc = calculate_delta_wc(wc, wc_previous)
            delta_ar = wc_components['ar'] - ar_previous
            delta_inventory = wc_components['inventory'] - inventory_previous
            delta_ap = wc_components['ap'] - ap_previous
        
        # Calculate FCF (before debt principal)
        fcf = calculate_fcf(
            ebit_after_interest,
            inputs['tax_rate'],
            inputs['depreciation'],
            inputs['capex'],
            delta_wc
        )
        
        # FCF after debt service (subtract principal payment)
        fcf_after_debt = fcf - debt_service['principal_payment']
        
        # Update cash balance (no change in month 0)
        if month > 0:
            cash_balance += fcf_after_debt
        
        # Calculate CCC
        ccc = inputs['ar_days'] + inputs['inventory_days'] - inputs['ap_days']
        
        # Calculate Tier 1 metrics
        tier1 = calculate_tier1_metrics(
            current_revenue,
            ebit,
            wc_components['ar'],
            wc_components['inventory'],
            wc_components['ap'],
            cash_balance,
            current_opex
        )
        
        # Calculate DSCR if debt exists
        dscr = 0
        if debt_params and month > 0 and (debt_service['interest_expense'] + debt_service['principal_payment']) > 0:
            dscr = fcf / (debt_service['interest_expense'] + debt_service['principal_payment'])
        
        # Store results
        results.append({
            'month': month,
            'revenue': current_revenue,
            'cogs': cogs,
            'ebit': ebit,
            'interest_expense': debt_service['interest_expense'],
            'ebit_after_interest': ebit_after_interest,
            'ebit_after_tax': ebit_after_tax,
            'ar': wc_components['ar'],
            'inventory': wc_components['inventory'],
            'ap': wc_components['ap'],
            'wc': wc,
            'delta_wc': delta_wc,
            'delta_ar': delta_ar,
            'delta_inventory': delta_inventory,
            'delta_ap': delta_ap,
            'fcf': fcf,
            'principal_payment': debt_service['principal_payment'],
            'fcf_after_debt': fcf_after_debt,
            'debt_balance': debt_service['remaining_balance'],
            'dscr': dscr,
            'cash_balance': cash_balance,
            'ccc': ccc,
            'gross_margin': gross_margin,
            'current_ratio': tier1['current_ratio'],
            'quick_ratio': tier1['quick_ratio'],
            'days_cash_on_hand': tier1['days_cash_on_hand'],
            'operating_margin': tier1['operating_margin']
        })
        
        # Update previous values
        wc_previous = wc
        ar_previous = wc_components['ar']
        inventory_previous = wc_components['inventory']
        ap_previous = wc_components['ap']
    
    return pd.DataFrame(results)


def generate_scenario_comparison(base_inputs, num_months, debt_params=None):
    """Generate projections for all three scenarios."""
    scenarios = {}
    
    for scenario_type in ['base', 'conservative', 'aggressive']:
        # Apply scenario adjustments
        adjusted_inputs = apply_scenario_adjustments(base_inputs, scenario_type)
        
        # Generate projections (with debt if provided)
        scenarios[scenario_type] = generate_monthly_projections(adjusted_inputs, num_months, debt_params)
    
    return scenarios