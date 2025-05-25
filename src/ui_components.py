import streamlit as st
import numpy as np

TOOLTIPS = {
    'variation': "This represents the variation covering approx. 95% of cases. For example, if growth is 5% and variation is 6%, actual growth will be between -1% and 11% per year in 95% of cases.",
    'years_remaining': """Number of years remaining for repayment of the loan. Different plans have different write-off periods:

Plan 1
  - Before Sept 2006: written off at age 65
  - After Sept 2006: written off 25 years after first repayment

Plan 2: written off 30 years after first repayment

Plan 4: written off at earlier of:
  - 30 years after first repayment
  - Age 65

Plan 5: written off 40 years after first repayment""",
    'loan_interest': """Typical Student Loan Interest Rates and Variations (Past 20 Years)

Plan 1: 2.0% ± 2.1%

Plan 2: 6.0% ± 2.0%

Plan 3 (Postgrad): 6.3% ± 1.5%

Plan 5: 3.5% ± 1.0%"""
}

def display_loan_salary_inputs():
    col1, col2 = st.columns(2)
    
    with col1:
        initial_salary = st.number_input("Current Annual Salary (£)", value=50000, min_value=0, step=5000)
        current_loan = st.number_input("Outstanding Loan Amount (£)", value=50000, min_value=0, step=5000)
        payback_years = st.number_input("Years Remaining for Repayment", value=15, min_value=1, max_value=50, step=1, help=TOOLTIPS['years_remaining'])
    
    with col2:
        threshold = st.number_input("Loan Repayment Threshold (£)", value=27000, min_value=0, step=1000)
        repayment_rate = st.number_input("Loan Repayment Rate (%)", value=9.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    
    return initial_salary, current_loan, payback_years, threshold, repayment_rate

def display_growth_rates():
    st.subheader("Growth Rates")
    salary_growth = st.number_input("Expected Salary Growth (%/year)", value=5.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    salary_growth_sigma = st.number_input("Salary Growth Variation (± %)", value=3.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f", help=TOOLTIPS['variation'])
    loan_rate = st.number_input("Loan Interest Rate (%)", value=6.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f", help=TOOLTIPS['loan_interest'])
    loan_rate_sigma = st.number_input("Loan Interest Rate Variation (± %)", value=2.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f", help=TOOLTIPS['loan_interest'])
    simulations = st.number_input("Number of Simulations", value=10000, min_value=100, max_value=100000, step=100)
    
    return salary_growth, salary_growth_sigma, loan_rate, loan_rate_sigma, simulations

def display_results_summary(payments_arr, investments_arr, gain_to_pay_early):
    st.subheader("Results Summary")
    
    recommendation = "Recommendation: pay off your loan early" if np.mean(gain_to_pay_early) > 0 else "Recommendation: keep your loan and invest the money"
    st.markdown(f"<h4 style='color: #00CC96'>💡 {recommendation}</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div style='text-align: center;'>"
                    "Predicted Total Loan<br>Repayment<br>"
                    f"<div style='font-size: 1.8em; font-weight: normal;'>£{np.mean(payments_arr):,.0f}</div>"
                    "</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center;'>"
                    "Predicted Investment<br>Returns<br>"
                    f"<div style='font-size: 1.8em; font-weight: normal;'>£{np.mean(investments_arr):,.0f}</div>"
                    "</div>", unsafe_allow_html=True)

    with col3:
        if np.mean(gain_to_pay_early) > 0:
            label = "Predicted Gain from Paying Early"
            value = f"£{np.mean(gain_to_pay_early):,.0f}"
        else:
            label = "Predicted Gain from Keeping Loan"
            value = f"£{-np.mean(gain_to_pay_early):,.0f}"
            
        st.markdown(f"<div style='text-align: center;'>"
                    f"{label}<br><br>"
                    f"<div style='font-size: 1.8em; font-weight: normal;'>{value}</div>"
                    "</div>", unsafe_allow_html=True) 
