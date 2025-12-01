"""
app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from calculations import generate_monthly_projections, apply_scenario_adjustments
from templates import get_example_templates

st.set_page_config(page_title="Cash Flow Lab", page_icon="💰", layout="wide")

# Debug mode flag (set False for deployment)
DEBUG_DEFAULT = False


def main():
    render_header()
    render_financial_concepts()
    render_sidebar()
    
    if st.session_state.get('inputs_ready', False):
        # Generate base scenario
        base = generate_monthly_projections(
            st.session_state['user_inputs'],
            st.session_state['num_months'],
            st.session_state.get('debt_params')
        )
        
        # Show base business summary 
        render_base_summary()
        
        # Scenario Lab - one type at a time
        scenarios = {'base': base}
        scenarios = render_scenario_lab(scenarios)
        
        # Show results
        render_scenario_comparison(scenarios)
        render_visualizations(scenarios)
        render_wc_breakdown(scenarios)
        render_explore_more()
        render_export(scenarios)
        
        # Feedback and support sections
        render_feedback_and_support()
        
        # Legal disclaimer
        render_legal_disclaimer()
    else:
        st.info("👈 Select a template in sidebar to start")


def render_feedback_and_support():
    """Feedback form and Buy Me a Coffee."""
    st.markdown("---")
    
    # Feedback form
    st.markdown("""
<div style="background: #e3f2fd; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center;">
    <p style="color: #1565c0; font-size: 16px; font-weight: 600; margin: 0 0 12px 0;">✨ Share Feedback or Request Assistance</p>
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSd7E0Vg3lD5SzrCbcJ7INpaMVX-Ad3WdSlgmiY-G8wXyBNymw/viewform?usp=header" rel="noopener" style="display: inline-block; background: #1565c0; color: white; padding: 10px 25px; border-radius: 5px; text-decoration: none; font-weight: 600; font-size: 13px;">
        Contact Us
    </a>
</div>
""", unsafe_allow_html=True)
    
    # Buy Me a Coffee
    st.markdown("""
<div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 5px; margin: 20px 0;">
    <p style="margin: 0 0 10px 0; font-size: 16px;">☕ <strong> Support this project and future work </strong></p>
    <a href="https://www.buymeacoffee.com/flourishingperspectivehub" target="_blank" rel="noopener">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px;">
    </a>
</div>
""", unsafe_allow_html=True)


def render_legal_disclaimer():
    """Legal and privacy information."""
    st.markdown("---")
    
    with st.expander("⚖️ Legal & Privacy Information"):
        st.markdown("""
**Educational Simulator**

Best practice: **Assume all results may be inaccurate.** This tool demonstrates financial concepts through simplified models, not real-world predictions.

**Your Responsibility:**
- Verify all calculations independently.
- Consult qualified professionals before decisions.
- Use for learning and exploration only.

---

### Financial Disclaimer

This tool is provided for informational and educational purposes only and does not constitute financial, investment, tax, or legal advice.

⚠️ **IMPORTANT**: This tool provides estimates only. Results may contain errors. Always verify calculations independently before making financial decisions.

- **Not Professional Advice**: The calculations, projections, and scenarios are based on user-provided data and simplified models. They should not be relied upon as the sole basis for financial decisions.
- **No Warranty**: This tool is provided "as is" without warranties of any kind, express or implied.
- **Consult Professionals**: Always consult with qualified financial advisors, accountants, or legal professionals before making important financial decisions.
- **Your Responsibility**: You are solely responsible for verifying the accuracy of inputs and interpreting results appropriately.

---

### Privacy & Data Handling

**Important:** This tool is hosted on Streamlit Cloud. Your inputs are processed on their servers but are not stored by us after your session ends. For information on Streamlit's data handling, see their Privacy Policy.

**Recommendations:**
- Do not enter sensitive personal information.
- Use representative numbers for planning purposes.

**Forms & Feedback:** Submissions via Google Forms are stored by Google and are subject to Google's privacy policy.

---

### External Links, Affiliates & Advertising

This site may contain:
- Affiliate links to third-party services (we may earn commission on purchases).
- Advertising or sponsored content.
- Links to resources we recommend.

**Disclosure**: We only recommend products or services we believe are valuable. Our recommendations are independent of any compensation received.

**Third-Party Links**: Our site contains links to external resources. We are not responsible for the accuracy, availability, or practices of those sites.

---

### Terms of Use

By using this tool, you agree to these terms:

**Acceptable Use**:
- Use this tool for lawful purposes only.
- Do not attempt to reverse engineer, hack, or exploit the application.
- Do not use automated tools to scrape or abuse the service.

**Limitation of Liability**: To the maximum extent permitted by law, we are not liable for any damages arising from your use of this tool, including but not limited to financial losses, business interruptions, or data loss.

**Modifications**: We reserve the right to modify, suspend, or discontinue the tool, or any portion of these terms, at any time without notice.

**Governing Law**: These terms are governed by the laws of the jurisdiction in which the service operator is based.
""")
    
    st.markdown("---")
    st.caption("💰 Cash Flow Lab | Free educational tool — explore, plan, and learn. Always verify all calculations.")

def render_header():
    st.title("💰 Cash Flow Lab")
    st.caption("Learn how business and operational decisions impact cash flow and working capital")
    

    
    # top warning   
    st.info("💡 **Educational tool** — Learn financial concepts through interactive scenarios. Results are simplified estimates. Always verify calculations and consult professionals before making financial decisions.")    
    # Intro

    st.success("""
**Interactive Financial Modeling Lab**

See how AR/AP/Inventory, growth, and strategy affect cash and why liquidity differs from profit. 
               
Explore concepts like the growth paradox and working capital cycles through interactive scenarios.

👈 **Start by selecting a template in the sidebar, then select a scenario type below** ⬇️
""")




def render_financial_concepts():
    """Educational foundation."""
    with st.expander("📚 Financial Concepts Reference", expanded=False):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Core Metrics", "Growth Paradox", "Operational Risks", "Advanced", "Definitions"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Gross Margin**  
                `(Revenue - COGS) / Revenue × 100%`
                
                Profitability before operating expenses.
                - Measures pricing power vs. production costs
                - Higher = more room for OPEX
                
                **COGS (Cost of Goods Sold)**  
                Direct costs to produce/deliver products.
                - Raw materials, manufacturing labor
                - Directly scales with revenue
                
                **Inventory**  
                Goods on hand awaiting sale.
                - Ties up cash until sold
                - Higher inventory = more capital needed
                
                **Accounts Receivable (AR)**  
                Money customers owe you.
                - Higher AR = cash locked until paid
                - Measured in days outstanding
                
                **Accounts Payable (AP)**  
                Money you owe suppliers.
                - Higher AP = using supplier credit
                - Measured in days payable
                
                **EBIT (Earnings Before Interest & Tax)**  
                `Revenue - COGS - OPEX`
                
                Operating profit before financing costs.
                - Shows business performance
                - Ignores debt structure
                """)
            
            with col2:
                st.markdown("""
                **Working Capital (WC)**  
                `(AR + Inventory) - AP`
                
                Cash tied up in operations.
                - Positive: Assets exceed liabilities
                - Higher WC = more cash needed
                
                ---
                
                **ΔWC (Change in WC)**  
                `WC_current - WC_previous`
                
                Cash consumed/released.
                - Positive: Cash tied up
                - Negative: Cash freed
                
                ---
                
                **Cash Conversion Cycle (CCC)**  
                `AR days + Inventory days - AP days`
                
                Days cash tied up in operations.
                - <30 days: Excellent
                - 30-60 days: Normal
                - >60 days: High - needs attention
                
                ---
                
                **Free Cash Flow (FCF)**  
                `NOPAT + Depreciation - CapEx - ΔWC`
                
                Cash available after operations & investments.
                - FCF > 0: Generates cash
                - FCF < 0: Consumes cash
                - The ultimate measure of financial health
                
                💡 **Key**: Profit ≠ Cash. ΔWC bridges the gap.
                """)
        
        with tab2:
            st.markdown("""
            ### Growth Paradox
            
            **You can be profitable but run out of cash!**
            
            **Why?** Revenue growth forces you to tie up more cash in AR and Inventory.
            
            **Example: 10% Revenue Growth**
            
            | Metric | Month 1 | Month 2 | Change |
            |--------|---------|---------|--------|
            | Revenue | \\$100K | \\$110K | +\\$10K (10%) |
            | **Profit (EBIT)** | \\$15.0K | \\$16.5K | +\\$1.5K ✅ |
            | **--- WC COMPONENTS ---** | | | |
            | AR (Assets) | \\$150.0K | \\$165.0K | +\\$15.0K 🔴 |
            | Inventory (Assets) | \\$120.0K | \\$132.0K | +\\$12.0K 🔴 |
            | AP (Liabilities) | \\$60.0K | \\$66.0K | +\\$6.0K 🟢 |
            | Total WC (\\$) | \\$210.0K | \\$231.0K | +\\$21.0K |
            | **--- CASH FLOW ---** | | | |
            | ΔWC (Cash Consumed) | - | \\$21.0K | +\\$21.0K |
            | **FCF (Profit - ΔWC)** | - | **-\\$4.5K** 🚨 | - |
            | **Cash Balance** | **\\$100K** | **\\$95.5K** | **-\\$4.5K** |
            
            📌 **The Paradox:** Profit increased by \\$1.5K, but cash decreased by \\$4.5K!  
            Growth consumed \\$21K in working capital (AR + Inventory grew faster than AP), turning positive profit into negative cash flow.
            
            💡 **Test**: Growth scenario
            
            ---
            
            ### Sustainable Growth Limit
            
            Max growth your cash supports. Beyond = need funding.
            
            💡 **See**: Max Sustainable Growth chart
            """)
        
        with tab3:
            st.markdown("""
            **Working Capital Trap**: Revenue flat, AR/Inventory rises → cash drain  
            💡 Test: Stagnant Revenue
            
            **Terms Shock**: Suppliers shorten AP → immediate cash hit  
            💡 Test: Conservative WC
            
            **Collections Slowdown**: Customers pay late → AR balloons  
            💡 Test: Payment Delays (+15d AR)
            
            **Inventory Build-Up**: Over-order inventory → cash locked in unsold stock  
            - COGS rises proportionally with inventory
            - More goods sitting = more cash tied up
            💡 Test: Inventory Buildup (+20%)
            
            **Inflation Squeeze**: COGS% rises → margins shrink + WC grows  
            - Higher COGS = lower Gross Margin
            - Same revenue, less profit, more cash needed
            💡 Test: Cost Inflation (+2%/mo)
            """)
        
        with tab4:
            st.markdown("""
            **CapEx Cliff**: Large equipment purchase → FCF drops  
            💡 See: EBIT to FCF waterfall
            
            **Positive Cash, Negative FCF**: Balance healthy but FCF negative  
            💡 Look for: Cash vs FCF chart divergence
            
            ---
            
            ### Debt & Leverage Concepts
            
            **Debt Service Coverage Ratio (DSCR)**  
            `FCF / (Interest + Principal)`
            
            Uses FCF (not EBITDA) to account for:
            - Capital expenditures
            - Working capital needs
            - Actual cash available for debt service
            
            - &gt;1.25: Healthy cushion
            - 1.0-1.25: Tight coverage
            - &lt;1.0: Cannot service debt
            
            **Note**: Our DSCR uses Free Cash Flow (accounts for CapEx & ΔWC) rather than EBITDA for more conservative debt coverage assessment.
            
            💡 Test: Higher Debt scenario  
            💡 See: DSCR chart
    
            """)
        
        with tab5:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **AR Days**: Customer payment time  
                **AP Days**: Supplier payment time  
                **Inventory Days**: Stock holding time  
                **CCC**: Cash tied up duration
                """)
            with col2:
                st.markdown("""
                **COGS**: Cost of Goods Sold  
                **OPEX**: Operating Expenses  
                **CapEx**: Capital Expenditures  
                **FCF**: Free Cash Flow
                """)


def render_sidebar():
    st.sidebar.title("🎛️ Initial Business Setup")
    st.sidebar.caption("Set your baseline - test variations in main page")
    
    # Templates
    with st.sidebar.expander("🚀 Quick Start Templates", expanded=True):
        templates = get_example_templates()
        st.caption("Click to load a starting point")
        
        cols = st.columns(2)
        with cols[0]:
            if st.button("Typical Business", width="stretch", 
                        help="Standard business - customize as needed"):
                load_template(templates["Typical Business"])
            if st.button("🏪 Retail", width="stretch",
                        help="High inventory, fast AR collection"):
                load_template(templates["Retail Store"])
        with cols[1]:
            if st.button("💻 SaaS", width="stretch",
                        help="Low COGS, high growth potential"):
                load_template(templates["SaaS Startup"])
            if st.button("🏭 Mfg", width="stretch",
                        help="Extended payment terms, high inventory"):
                load_template(templates["Manufacturing"])
    


    st.sidebar.markdown("---")
    
    # Business Fundamentals
    st.sidebar.subheader("💼 Business Fundamentals")
    
    num_months = st.sidebar.number_input(
        "Projection period (months)", 3, 36,
        st.session_state.get('months', 12), 1
    )
    
    opening_cash = st.sidebar.number_input(
        "Opening Cash ($)", 0, 10000000,
        st.session_state.get('cash', 100000), 10000
    )
    
    revenue = st.sidebar.number_input(
        "Monthly Revenue ($)", 0, 10000000,
        st.session_state.get('rev', 100000), 10000
    )
    
    cogs_pct = st.sidebar.slider(
        "COGS (% of revenue)", 0, 100,
        st.session_state.get('cogs', 60), 5
    ) / 100
    st.sidebar.caption(f"Gross Margin: {(1-cogs_pct)*100:.0f}%")
    
    opex = st.sidebar.number_input(
        "Monthly OPEX ($)", 0, 1000000,
        st.session_state.get('opex', 20000), 5000
    )
    
    # Working Capital Terms (from template)
    st.sidebar.subheader("🔄 Working Capital Terms")
    st.sidebar.caption("From template - adjust in scenarios")
    
    ar_days = st.session_state.get('ar', 45)
    ap_days = st.session_state.get('ap', 30)
    inv_days = st.session_state.get('inv', 60)
    
    ccc = ar_days + inv_days - ap_days
    st.sidebar.metric("Cash Conversion Cycle", f"{ccc} days")
    st.sidebar.caption(f"AR: {ar_days}d | AP: {ap_days}d | Inv: {inv_days}d")
    
    # Advanced Settings
    with st.sidebar.expander("⚙️ Advanced Settings"):
        tax_rate = st.slider("Tax Rate (%)", 0, 50, 
                            st.session_state.get('tax', 25), 5) / 100
        
        capex = st.number_input("Monthly CapEx ($)", 0, 500000,
                               st.session_state.get('capex_val', 5000), 1000)
        
        depreciation = st.number_input("Monthly Depreciation ($)", 0, 500000,
                                      st.session_state.get('depr_val', 4000), 1000)
        
        # Base growth rate
        base_growth = st.slider("Base Growth Rate (%/mo)", 0.0, 5.0,
                               st.session_state.get('growth_val', 2.0), 0.5) / 100
        st.caption("Revenue growth in Base scenario")
    
    # Debt (from template)
    with st.sidebar.expander("💳 Debt Settings"):
        st.caption("From template - adjust in scenarios")
        
        has_term = st.checkbox("Term Loan",
                              value=st.session_state.get('has_term', False))
        if has_term:
            term_amount = st.number_input("Loan Amount ($)", 0, 10000000,
                                         st.session_state.get('term_amount', 100000), 10000)
            term_rate = st.slider("Interest Rate (%)", 0.0, 15.0, 
                                 st.session_state.get('term_rate', 6.0), 0.5) / 100
            term_months = st.number_input("Term (months)", 12, 360, 
                                         st.session_state.get('term_months', 60), 12)
            
            # Calculate monthly payment (handle 0% interest)
            monthly_rate = term_rate / 12
            if monthly_rate > 0:
                monthly_payment = term_amount * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
            else:
                monthly_payment = term_amount / term_months
            
            debt_params = {
                'loan_amount': term_amount,
                'interest_rate': term_rate,
                'term_months': term_months,
                'monthly_payment': monthly_payment
            }
            st.caption(f"Monthly Payment: ${monthly_payment:,.0f}")
        else:
            debt_params = None
    
    # Debug Mode
    # Only show debug toggle if DEBUG_DEFAULT is True (for development)
    if DEBUG_DEFAULT:
        st.sidebar.markdown("---")
        debug_mode = st.sidebar.checkbox("🔧 Debug Mode", value=DEBUG_DEFAULT)
        st.session_state['debug_mode'] = debug_mode
    else:
        st.session_state['debug_mode'] = False
    
    # Store state
    st.session_state['user_inputs'] = {
        'revenue': revenue,
        'cogs_pct': cogs_pct,
        'cogs_increase': 0,
        'opex': opex,
        'opex_increase': 0,
        'tax_rate': tax_rate,
        'ar_days': ar_days,
        'ap_days': ap_days,
        'inventory_days': inv_days,
        'capex': capex,
        'depreciation': depreciation,
        'price_increase': base_growth,
        'opening_cash': opening_cash
    }
    st.session_state['num_months'] = num_months
    st.session_state['debt_params'] = debt_params
    st.session_state['inputs_ready'] = True


def load_template(template):
    """Load template into session state."""
    mapping = {
        'ar_days': 'ar', 'ap_days': 'ap', 'inventory_days': 'inv',
        'num_months': 'months', 'opening_cash': 'cash', 'revenue': 'rev',
        'opex': 'opex', 'capex': 'capex_val', 'depreciation': 'depr_val'
    }
    
    for key, val in template.items():
        if key == 'cogs_pct':
            st.session_state['cogs'] = int(val * 100)
        elif key == 'tax_rate':
            st.session_state['tax'] = int(val * 100)  # Store as INT percentage
        elif key == 'price_increase':
            st.session_state['growth_val'] = val * 100  # Store as percentage
        elif key == 'has_term':
            st.session_state['has_term'] = val
        elif key == 'term_amount':
            st.session_state['term_amount'] = val
        elif key == 'term_rate':
            st.session_state['term_rate'] = val * 100  # Store as percentage
        elif key == 'term_months':
            st.session_state['term_months'] = val
        elif key in mapping:
            st.session_state[mapping[key]] = val
    
    st.rerun()


def render_base_summary():
    """Show base business with key metrics."""
    st.markdown("---")
    st.subheader("📊 Your Base Business")
    
    inputs = st.session_state['user_inputs']
    debt_params = st.session_state.get('debt_params')
    
    # Generate base scenario to get metrics
    base = generate_monthly_projections(
        inputs,
        st.session_state['num_months'],
        debt_params
    )
    
    ar = inputs['ar_days']
    ap = inputs['ap_days']
    inv = inputs['inventory_days']
    ccc = ar + inv - ap
    final_cash = base['cash_balance'].iloc[-1]
    total_fcf = base['fcf'].sum()
    
    # 5 metrics in one row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Monthly Revenue", f"${inputs['revenue']:,.0f}")
        st.caption(f"COGS: {inputs['cogs_pct']*100:.0f}% | OPEX: ${inputs['opex']:,.0f}")
        st.caption(f"Growth: {inputs['price_increase']*100:.1f}%/mo")
    
    with col2:
        st.metric("CCC", f"{ccc:.0f}d")
        st.caption(f"AR: {ar}d | AP: {ap}d | Inv: {inv}d")
        if ccc > 60:
            st.caption("⚠️ High - cash tied 2+ months")
        elif ccc < 30:
            st.caption("✅ Excellent")
        else:
            st.caption("✓ Normal")
    
    with col3:
        st.metric("Opening Cash", f"${inputs['opening_cash']:,.0f}")
        debt_str = f"Debt: ${debt_params['loan_amount']:,.0f}" if debt_params else "No Debt"
        st.caption(debt_str)
    
    with col4:
            st.metric("Final Cash", f"${final_cash:,.0f}")
            if final_cash < 0:
                st.caption("🚨 Deficit - need funding")
            else:
                st.caption("✅ Positive")
            st.caption("Opening + FCF (Month 0 excluded)")
            st.caption("📊 See: Cash Balance chart")

    
    with col5:
        st.metric("Total FCF", f"${total_fcf:,.0f}")
        if total_fcf < 0:
            st.caption("Cash consumed")
        else:
            st.caption("Cash generated")
        st.caption("📊 See: FCF chart")
    



def render_scenario_lab(scenarios):
    """One scenario type at a time."""
    st.markdown("---")
    st.markdown("### Scenarios: 🎯 What Do You Want to Learn?")
    st.caption("Pick a scenario type and adjust its parameters below")

# Scenario overview table
    st.markdown("""
    | Working Capital Terms | Growth Rates | Operational Risks | Debt & Leverage |
    |---|---|---|---|
    | How AR/AP/Inventory timing impact cash | Growth impact on liquidity and sustainability | How operations impact cash | How debt affects cash pressure |
    """)

    
    
    base_inputs = st.session_state['user_inputs']
    num_months = st.session_state['num_months']
    debt_params = st.session_state.get('debt_params')
    
    # One scenario type at a time
    scenario_type = st.radio(
        "Select scenario type",
        ["Working Capital Terms", "Growth Rates", "Operational Risks", "Debt & Leverage"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Store scenario type for later use
    st.session_state['active_scenario_type'] = scenario_type
    
    if scenario_type == "Working Capital Terms":
        scenarios = render_wc_scenarios(scenarios, base_inputs, num_months, debt_params)
    
    elif scenario_type == "Growth Rates":
        scenarios = render_growth_scenarios(scenarios, base_inputs, num_months, debt_params)
    
    elif scenario_type == "Operational Risks":
        scenarios = render_risk_scenarios(scenarios, base_inputs, num_months, debt_params)
    
    elif scenario_type == "Debt & Leverage":
        scenarios = render_debt_scenarios(scenarios, base_inputs, num_months, debt_params)
    
    return scenarios


def render_wc_scenarios(scenarios, base_inputs, num_months, debt_params):
    """Working capital scenarios with table format."""

    
    ar = base_inputs['ar_days']
    ap = base_inputs['ap_days']
    inv = base_inputs['inventory_days']
    
    # Calculate scenario values
    agg_ar, agg_ap, agg_inv = max(0, ar-10), ap+10, int(inv*0.85)
    cons_ar, cons_ap, cons_inv = ar+10, max(0, ap-5), int(inv*1.15)
    
    st.markdown("**Select scenarios to test:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_agg = st.checkbox("✅ Aggressive", value=True)
    
    with col2:
        show_cons = st.checkbox("⚠️ Conservative", value=True)
    
    with col3:
        show_custom = st.checkbox("⚙️ Custom", value=False)
    
    if show_custom:
        st.markdown("**Custom terms:**")
        c1, c2, c3 = st.columns(3)
        with c1:
            custom_ar = st.number_input("AR days", 0, 180, ar, 5)
        with c2:
            custom_ap = st.number_input("AP days", 0, 180, ap, 5)
        with c3:
            custom_inv = st.number_input("Inv days", 0, 365, inv, 5)
        
        st.caption(f"Custom CCC: {custom_ar+custom_inv-custom_ap}d")
    
    # Show scenarios in table
    st.markdown("---")
    st.markdown("**Scenario Comparison:**")
    
    scenario_data = []
    scenario_data.append({
        'Scenario': 'Base',
        'AR Days': ar,
        'AP Days': ap,
        'Inv Days': inv,
        'CCC': ar + inv - ap
    })
    
    scenario_data.append({
        'Scenario': '✅ Aggressive',
        'AR Days': agg_ar,
        'AP Days': agg_ap,
        'Inv Days': agg_inv,
        'CCC': agg_ar + agg_inv - agg_ap
    })
    
    scenario_data.append({
        'Scenario': '⚠️ Conservative',
        'AR Days': cons_ar,
        'AP Days': cons_ap,
        'Inv Days': cons_inv,
        'CCC': cons_ar + cons_inv - cons_ap
    })
    
    st.dataframe(pd.DataFrame(scenario_data), hide_index=True, width="stretch")
    
    # Generate scenarios
    if show_agg:
        agg_inputs = base_inputs.copy()
        agg_inputs.update({'ar_days': agg_ar, 'ap_days': agg_ap, 'inventory_days': agg_inv})
        scenarios['aggressive'] = generate_monthly_projections(agg_inputs, num_months, debt_params)
    
    if show_cons:
        cons_inputs = base_inputs.copy()
        cons_inputs.update({'ar_days': cons_ar, 'ap_days': cons_ap, 'inventory_days': cons_inv})
        scenarios['conservative'] = generate_monthly_projections(cons_inputs, num_months, debt_params)
    
    if show_custom:
        custom_inputs = base_inputs.copy()
        custom_inputs.update({'ar_days': custom_ar, 'ap_days': custom_ap, 'inventory_days': custom_inv})
        scenarios['custom'] = generate_monthly_projections(custom_inputs, num_months, debt_params)
    
    return scenarios


def render_growth_scenarios(scenarios, base_inputs, num_months, debt_params):
    """Growth scenarios with learning moments."""

    
    growth_rate = st.radio(
        "Test growth rate:",
        ["3%/mo", "5%/mo", "8%/mo", "10%/mo", "12%/mo"],
        horizontal=True
    )
    
    growth_map = {"3%/mo": 0.03, "5%/mo": 0.05, "8%/mo": 0.08, "10%/mo": 0.10, "12%/mo": 0.12}
    growth_val = growth_map[growth_rate]
    
    # Store selected growth rate
    st.session_state['selected_growth_rate'] = growth_rate
    
    growth_inputs = base_inputs.copy()
    growth_inputs['price_increase'] = growth_val
    scenarios['growth'] = generate_monthly_projections(growth_inputs, num_months, debt_params)
    
    # Learning moment
    growth_cash = scenarios['growth']['cash_balance'].min()
    if growth_cash < 0:
        deficit_month = scenarios['growth'][scenarios['growth']['cash_balance'] < 0].iloc[0]['month']
        st.error(f"🚨 **Learning Moment**: At {growth_val*100:.0f}% growth, cash goes negative by Month {deficit_month:.0f}!")
        st.caption(f"Need ${abs(growth_cash):,.0f} funding. Growth ties up cash in AR/Inventory.")
    else:
        st.success(f"✅ At {growth_val*100:.0f}% growth, cash stays positive!")
    
    # Max Sustainable Growth
    st.markdown("---")
    st.markdown("### 📈 Max Sustainable Growth & Cash Runway")
    
    test_rates = [0.00, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12, 0.15]
    max_sustainable = 0
    runway_data = []
    
    for rate in test_rates:
        test_inputs = base_inputs.copy()
        test_inputs['price_increase'] = rate
        test_df = generate_monthly_projections(test_inputs, num_months, debt_params)
        min_cash = test_df['cash_balance'].min()
        
        if min_cash >= 0:
            max_sustainable = rate
            runway_months = num_months
        else:
            deficit_month = test_df[test_df['cash_balance'] < 0].iloc[0]['month']
            runway_months = int(deficit_month) - 1
        
        runway_data.append({'rate': rate, 'runway_months': runway_months})
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Max Sustainable Growth", f"{max_sustainable*100:.0f}%/mo")
        st.caption(f"Can sustain {num_months} months")
    
    with col2:
        fig_runway = go.Figure()
        
        fig_runway.add_trace(go.Scatter(
            x=[d['rate']*100 for d in runway_data],
            y=[d['runway_months'] for d in runway_data],
            mode='lines+markers',
            line=dict(color='#3498DB', width=3),
            marker=dict(size=8)
        ))
        
        fig_runway.add_vline(x=max_sustainable*100, line_dash="dash", line_color="green",
                            annotation_text=f"Max: {max_sustainable*100:.0f}%")
        
        fig_runway.update_layout(
            title="Cash Runway vs Growth Rate",
            xaxis_title="Growth Rate (%/month)",
            yaxis_title="Months of Runway",
            height=350
        )
        
        st.plotly_chart(fig_runway, width="stretch", key='runway_chart')
    
    return scenarios


def render_risk_scenarios(scenarios, base_inputs, num_months, debt_params):
    """Operational risk scenarios."""

    
    col1, col2 = st.columns(2)
    
    with col1:
        test_delay = st.checkbox("📅 Payment Delays (+15d AR)")
        if test_delay:
            delay_inputs = base_inputs.copy()
            delay_inputs['ar_days'] = base_inputs['ar_days'] + 15
            scenarios['delay'] = generate_monthly_projections(delay_inputs, num_months, debt_params)
            
            cash_impact = scenarios['delay']['cash_balance'].iloc[-1] - scenarios['base']['cash_balance'].iloc[-1]
            st.caption(f"Impact: ${cash_impact:,.0f}")
        
        test_inflation = st.checkbox("📈 Cost Inflation (+2%/mo COGS)")
        if test_inflation:
            inflation_inputs = base_inputs.copy()
            inflation_inputs['cogs_increase'] = 0.02
            scenarios['inflation'] = generate_monthly_projections(inflation_inputs, num_months, debt_params)
            
            margin_end = scenarios['inflation']['gross_margin'].iloc[-1]
            margin_start = (1 - base_inputs['cogs_pct']) * 100
            st.caption(f"Margin: {margin_start:.0f}% → {margin_end:.0f}%")
            
            # Check if COGS cap was hit
            final_cogs_pct = scenarios['inflation']['cogs'].iloc[-1] / scenarios['inflation']['revenue'].iloc[-1]
            if final_cogs_pct >= 0.94:
                st.warning("⚠️ COGS capped at 95%")
    
    with col2:
        test_inv = st.checkbox("📦 Inventory Buildup (+20%)")
        if test_inv:
            inv_inputs = base_inputs.copy()
            inv_inputs['inventory_days'] = int(base_inputs['inventory_days'] * 1.2)
            scenarios['excess_inv'] = generate_monthly_projections(inv_inputs, num_months, debt_params)
            
            cash_impact = scenarios['excess_inv']['cash_balance'].iloc[-1] - scenarios['base']['cash_balance'].iloc[-1]
            base_inv_days = base_inputs['inventory_days']
            new_inv_days = inv_inputs['inventory_days']
            st.caption(f"Inventory: {base_inv_days}d → {new_inv_days}d")
            st.caption(f"Cash tied: ${abs(cash_impact):,.0f}")
        
        test_stagnant = st.checkbox("📉 Stagnant Revenue (0% growth)")
        if test_stagnant:
            stagnant_inputs = base_inputs.copy()
            stagnant_inputs['price_increase'] = 0.0
            stagnant_inputs['opex_increase'] = 0.01
            scenarios['stagnant'] = generate_monthly_projections(stagnant_inputs, num_months, debt_params)
            
            if scenarios['stagnant']['fcf'].sum() < scenarios['base']['fcf'].sum():
                st.caption("⚠️ FCF declines")
    
    return scenarios


def render_debt_scenarios(scenarios, base_inputs, num_months, debt_params):
    """Debt & leverage scenarios."""

    if debt_params is None:
        st.info("👈 Enable Term Loan in sidebar to test debt scenarios")
        return scenarios
    
    # Show base debt info
    st.markdown(f"**Base Debt:** ${debt_params['loan_amount']:,.0f} @ {debt_params['interest_rate']*100:.1f}% for {debt_params['term_months']} months")
    st.caption(f"Monthly Payment: ${debt_params['monthly_payment']:,.0f}")
    
    st.markdown("---")
    st.markdown("**Test debt variations:**")
    
    test_higher = st.checkbox("📈 Higher Debt (+50%)")
    if test_higher:
        higher_debt = debt_params.copy()
        higher_debt['loan_amount'] = debt_params['loan_amount'] * 1.5
        monthly_rate = higher_debt['interest_rate'] / 12
        if monthly_rate > 0:
            higher_debt['monthly_payment'] = higher_debt['loan_amount'] * (monthly_rate * (1 + monthly_rate)**higher_debt['term_months']) / ((1 + monthly_rate)**higher_debt['term_months'] - 1)
        else:
            higher_debt['monthly_payment'] = higher_debt['loan_amount'] / higher_debt['term_months']
        
        scenarios['higher_debt'] = generate_monthly_projections(base_inputs, num_months, higher_debt)
        st.caption(f"Amount: ${higher_debt['loan_amount']:,.0f}")
        st.caption(f"Payment: ${higher_debt['monthly_payment']:,.0f}/mo")
    
    return scenarios



def render_scenario_comparison(scenarios):
    """Compare scenarios."""
    st.markdown("---")
    st.subheader("📋 Scenario Comparison")
    
    base_cash = scenarios['base']['cash_balance'].iloc[-1]
    base_ccc = scenarios['base']['ccc'].iloc[0]
    base_fcf = scenarios['base']['fcf'].sum()
    
    data = []
    
    labels = {
        'base': 'Base', 'aggressive': 'Aggressive WC', 'conservative': 'Conservative WC',
        'custom': 'Custom WC', 'growth': f"Growth ({st.session_state.get('selected_growth_rate', 'N/A')})", 
        'delay': 'Payment Delays',
        'inflation': 'Cost Inflation', 'excess_inv': 'Excess Inventory',
        'stagnant': 'Stagnant Revenue', 'higher_debt': 'Higher Debt (+50%)',
        'growth_debt': 'Growth + Debt (5%/mo)'
    }
    
    for name, df in scenarios.items():
        final = df.iloc[-1]
        cash_vs = final['cash_balance'] - base_cash
        ccc_vs = df['ccc'].iloc[0] - base_ccc
        fcf_vs = df['fcf'].sum() - base_fcf
        
        data.append({
            'Scenario': labels.get(name, name),
            'CCC': f"{df['ccc'].iloc[0]:.0f}d",
            'vs Base': f"{ccc_vs:+.0f}d" if name != 'base' else '-',
            'Final Cash': f"${final['cash_balance']:,.0f}",
            'vs Base ': f"${cash_vs:+,.0f}" if name != 'base' else '-',
            'Total FCF': f"${df['fcf'].sum():,.0f}",
            'vs Base  ': f"${fcf_vs:+,.0f}" if name != 'base' else '-'
        })
    
    st.dataframe(pd.DataFrame(data), width="stretch", hide_index=True)
    
    # Debug Mode
    if st.session_state.get('debug_mode', False):
        st.markdown("---")
        st.subheader("🔧 Debug: Detailed Tables")
        
        for name, df in scenarios.items():
            with st.expander(f"📊 {labels.get(name, name)} Data"):
                st.dataframe(df, width="stretch", hide_index=True)


def render_visualizations(scenarios):
    """Core charts."""
    st.markdown("---")
    st.subheader("📊 Visual Evidence")
    
    # Check if debt exists in any scenario
    has_debt = any(df['dscr'].sum() > 0 for df in scenarios.values())
    
    if has_debt:
        # Show 3 charts in row 1
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(create_line_chart(scenarios, 'fcf', 'Free Cash Flow'), 
                           width="stretch", key='fcf_chart')
            st.caption("💡 Negative = burning | Positive = generating")
        
        with col2:
            st.plotly_chart(create_line_chart(scenarios, 'cash_balance', 'Cash Balance'), 
                           width="stretch", key='cash_chart')
            st.caption("💡 Goes negative = need funding")
        
        with col3:
            st.plotly_chart(create_dscr_chart(scenarios), 
                           width="stretch", key='dscr_chart')
            st.caption("💡 DSCR = FCF / Debt Payments | >1.25 = Healthy | 1.0-1.25 = Tight | <1.0 = Stressed")
    else:
        # Original 2-column layout when no debt
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_line_chart(scenarios, 'fcf', 'Free Cash Flow'), 
                           width="stretch", key='fcf_chart')
            st.caption("💡 Negative = burning | Positive = generating")
        
        with col2:
            st.plotly_chart(create_line_chart(scenarios, 'cash_balance', 'Cash Balance'), 
                           width="stretch", key='cash_chart')
            st.caption("💡 Goes negative = need funding")
    
    # Row 2: WC and CCC
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(create_line_chart(scenarios, 'wc', 'Working Capital'), 
                       width="stretch", key='wc_chart')
        st.caption("💡 Capital tied in operations")
    
    with col4:
        st.plotly_chart(create_line_chart(scenarios, 'ccc', 'CCC (days)', False), 
                       width="stretch", key='ccc_chart')
        st.caption("💡 Lower = faster conversion")
    
    # Waterfall
    st.markdown("### 💧 EBIT to FCF Bridge (How Profit Becomes Cash)")
    
    if len(scenarios) > 1:
        compare_scenario = list(scenarios.keys())[1]
        
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("**Base**")
            st.plotly_chart(create_waterfall(scenarios['base']), 
                          width="stretch", key='waterfall_base')
        with col6:
            st.markdown(f"**{compare_scenario.capitalize()}**")
            st.plotly_chart(create_waterfall(scenarios[compare_scenario]), 
                          width="stretch", key='waterfall_compare')
    else:
        st.plotly_chart(create_waterfall(scenarios['base']), 
                       width="stretch", key='waterfall_single')


def render_wc_breakdown(scenarios):
    """Show WC breakdown for Base and selected scenario."""
    base = scenarios['base']
    
    # Check if there's variation
    if base['delta_wc'].std() < 100:
        st.markdown("---")
        st.info("💡 Enable Growth scenario to see Working Capital changes over time")
        return
    
    st.markdown("---")
    st.subheader("🔍 Working Capital Breakdown")
    st.caption("Where cash gets tied up")
    
    # Show base + selected scenario (if not base)
    if len(scenarios) > 1:
        selected_key = [k for k in scenarios.keys() if k != 'base'][0]
        selected = scenarios[selected_key]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Base Scenario**")
            fig_base = create_wc_breakdown_chart(base)
            st.plotly_chart(fig_base, width="stretch", key='wc_breakdown_base')
        
        with col2:
            st.markdown(f"**{selected_key.replace('_', ' ').title()} Scenario**")
            fig_selected = create_wc_breakdown_chart(selected)
            st.plotly_chart(fig_selected, width="stretch", key='wc_breakdown_selected')
        
        st.caption("💡 Red = consumed | Green = released | Growth drives consumption")
    else:
        # Just base
        fig = create_wc_breakdown_chart(base)
        st.plotly_chart(fig, width="stretch", key='wc_breakdown')
        st.caption("💡 Red = consumed | Green = released | Growth drives consumption")


def render_explore_more():
    """Suggest additional exploration with external resources."""
    st.markdown("---")
    st.markdown('<p style="font-size: 24px; font-weight: bold;">🧭 EXPLORE MORE</p>', unsafe_allow_html=True)
    
    st.markdown("""
    - [Free cash flow (FCF) vs. net income: Differences and how to calculate](https://quickbooks.intuit.com/r/cash-flow/critical-difference-profit-cash-flow/) (QuickBooks)
    - [How to calculate and interpret your cash conversion cycle](https://ramp.com/blog/how-to-calculate-cash-conversion-cycle) (Blog from Ramp)
    - [Financial and Managerial Accounting — MIT OpenCourseWare](https://ocw.mit.edu/courses/15-514-financial-and-managerial-accounting-summer-2003/)
    - [How Finance Works: The HBR Guide](https://a.co/d/hQDOIl3) - Practical guide to finance, valuation, and risk by Mihir Desai
    """)


def render_export(scenarios):
    """CSV export."""
    st.markdown("---")
    st.subheader("💾 Export")
    
    #warning at Export
    st.warning("⚠️ **Reminder**: Educational estimates only. Best practice is to assume results may be inaccurate. Verify all calculations independently and consult qualified professionals before making financial decisions.")

    export_df = pd.DataFrame()
    for name, df in scenarios.items():
        df_copy = df.copy()
        df_copy['scenario'] = name
        export_df = pd.concat([export_df, df_copy], ignore_index=True)
    
    csv = export_df.to_csv(index=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    st.download_button(
        "📥 Download CSV",
        csv,
        f"wc_analysis_{timestamp}.csv",
        "text/csv",
        width="stretch"
    )


def create_line_chart(scenarios, metric, title, is_currency=True):
    """Line chart."""
    fig = go.Figure()
    
    colors = {
        'base': '#1f77b4', 'aggressive': '#2ca02c', 'conservative': '#ff7f0e',
        'custom': '#9467bd', 'growth': '#d62728', 'delay': '#8c564b',
        'inflation': '#e377c2', 'excess_inv': '#7f7f7f', 'stagnant': '#bcbd22',
        'higher_debt': '#e377c2', 'growth_debt': '#d62728'
    }
    
    for name, df in scenarios.items():
        if name in colors:
            # Filter out Month 0, start at Month 1
            df_plot = df[df['month'] > 0].copy()
            
            # Highlight growth scenario if it's the active one
            is_growth_selected = (name == 'growth' and 
                                st.session_state.get('active_scenario_type') == 'Growth Rates')
            
            fig.add_trace(go.Scatter(
                x=df_plot['month'], y=df_plot[metric],
                mode='lines+markers',
                name=name.replace('_', ' ').title(),
                line=dict(
                    color=colors[name], 
                    width=4 if is_growth_selected else 2.5,
                    dash='solid' if not is_growth_selected else 'solid'
                ),
                marker=dict(size=10 if is_growth_selected else 6)
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Amount ($)" if is_currency else "Days",
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    if is_currency:
        fig.update_yaxes(tickformat="$,.0f")
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig


def create_waterfall(df):
    """EBIT to FCF waterfall."""
    final = df.iloc[-1]
    inputs = st.session_state['user_inputs']
    
    ebit_tax = final['ebit_after_tax']
    depr = inputs['depreciation']
    capex = inputs['capex']
    dwc = final['delta_wc']
    fcf = final['fcf']
    
    fig = go.Figure(go.Waterfall(
        x=['EBIT<br>(After Tax)', '+Depr', '-CapEx', '-ΔWC', 'FCF'],
        y=[ebit_tax, depr, -capex, -dwc, fcf],
        measure=['relative', 'relative', 'relative', 'relative', 'total'],
        text=[f"${v:,.0f}" for v in [ebit_tax, depr, -capex, -dwc, fcf]],
        textposition='outside',
        decreasing={"marker": {"color": "#E74C3C"}},
        increasing={"marker": {"color": "#27AE60"}},
        totals={"marker": {"color": "#3498DB"}}
    ))
    
    fig.update_layout(showlegend=False, height=350)
    fig.update_yaxes(tickformat="$,.0f")
    
    return fig


def create_dscr_chart(scenarios):
    """DSCR line chart."""
    fig = go.Figure()
    
    colors = {
        'base': '#1f77b4', 
        'aggressive': '#2ca02c', 
        'conservative': '#ff7f0e',
        'custom': '#9467bd', 
        'growth': '#d62728', 
        'delay': '#8c564b',
        'inflation': '#e377c2', 
        'excess_inv': '#7f7f7f', 
        'stagnant': '#bcbd22',
        'higher_debt': '#e377c2', 
        'growth_debt': '#d62728'
    }
    
    for name, df in scenarios.items():
        if df['dscr'].sum() > 0:  # Only show scenarios with debt
            # Filter out Month 0, start at Month 1
            df_plot = df[df['month'] > 0].copy()
            
            fig.add_trace(go.Scatter(
                x=df_plot['month'], y=df_plot['dscr'],
                mode='lines+markers',
                name=name.replace('_', ' ').title(),
                line=dict(color=colors.get(name, '#999999'), width=2.5),
                marker=dict(size=6)
            ))
    
    # Add threshold lines
    fig.add_hline(y=1.25, line_dash="dash", line_color="green", line_width=3,
                  annotation_text="✅ Healthy (1.25x)", annotation_position="right",
                  annotation=dict(font_size=12, font_color="green"))
    fig.add_hline(y=1.0, line_dash="dash", line_color="red", line_width=3,
                  annotation_text="⚠️ Minimum (1.0x)", annotation_position="right",
                  annotation=dict(font_size=12, font_color="red"))
    
    fig.update_layout(
        title="Debt Service Coverage Ratio",
        xaxis_title="Month",
        yaxis_title="DSCR (x)",
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    return fig


def create_wc_breakdown_chart(df):
    """Working capital breakdown chart."""
    # Filter out Month 0, start at Month 1
    df_plot = df[df['month'] > 0].copy()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_plot['month'], y=df_plot['delta_ar'],
        name='ΔAR (Tied in Receivables)',
        marker_color='#E74C3C'
    ))
    
    fig.add_trace(go.Bar(
        x=df_plot['month'], y=df_plot['delta_inventory'],
        name='ΔInventory (Tied in Stock)',
        marker_color='#E67E22'
    ))
    
    fig.add_trace(go.Bar(
        x=df_plot['month'], y=-df_plot['delta_ap'],
        name='ΔAP (Released from Delays)',
        marker_color='#27AE60'
    ))
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cash Impact ($)",
        barmode='relative',
        height=350,
        showlegend=True
    )
    fig.update_yaxes(tickformat="$,.0f")
    
    return fig


if __name__ == "__main__":
    main()