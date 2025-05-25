import streamlit as st
import numpy as np
from src.simulation import run_simulation
from src.investment_data import INVESTMENT_OPTIONS, calculate_historical_returns
from src.visualisation import create_gain_plot, create_distribution_plot
from src.ui_components import (
    display_loan_salary_inputs,
    display_growth_rates,
    display_results_summary
)

def main():
    st.title("Student Loan Simulation")
    st.markdown("""
    This simulation helps you decide whether to pay off your student loan early by comparing:
    - Expected total repayments over time
    - Potential returns if you invested the money instead
    """)

    st.header("Loan and Salary Information")
    st.markdown("Enter your current loan details and salary information")
    
    initial_salary, current_loan, payback_years, threshold, repayment_rate = display_loan_salary_inputs()

    st.header("Scenario Parameters")
    st.markdown("Configure the simulation parameters for different economic scenarios")
    
    col3, col4 = st.columns(2)
    
    with col3:
        salary_growth, salary_growth_sigma, loan_rate, loan_rate_sigma, simulations = display_growth_rates()
    
    with col4:
        st.subheader("Investment & Life Events")
        
        investment_type = st.selectbox(
            "Investment Type",
            options=list(INVESTMENT_OPTIONS.keys()),
            index=list(INVESTMENT_OPTIONS.keys()).index("Vanguard FTSE 100 ETF"),
            help="Select an investment type or choose Custom to manually enter returns"
        )
        
        if investment_type == "Custom":
            investment_rate = st.number_input("Investment Return Rate (%)", value=4.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
            investment_rate_sigma = st.number_input("Investment Return Variation (± %)", value=8.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
            child_prob = st.number_input("Probability of Unpaid Career Break per Year (%)", value=10.0, min_value=0.0, max_value=100.0, step=1.0, format="%.1f")
        else:
            with st.spinner(f"Fetching historical data for {investment_type}..."):
                historical_returns = calculate_historical_returns(INVESTMENT_OPTIONS[investment_type], 20)
                
                if historical_returns:
                    investment_rate = historical_returns['mean_return']
                    investment_rate_sigma = historical_returns['variation']
                    
                    st.info(
                        f"Based on the last 20 years:\n\n"
                        f"Average return: {investment_rate:.1f}%\n\n"
                        f"Variation (± %): {investment_rate_sigma:.1f}%\n"
                    )
                    
                    st.write("")
                    
                    child_prob = st.number_input("Probability of Unpaid Career Break per Year (%)", value=10.0, min_value=0.0, max_value=100.0, step=1.0, format="%.0f")
                else:
                    investment_rate = 4.0
                    investment_rate_sigma = 8.0
                    st.warning("Failed to fetch historical data. Using default values.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_button = st.button("Run Simulation", type="primary")

    if run_button:
        inputs = {
            "initial_salary": initial_salary,
            "current_loan": current_loan,
            "payback_years": payback_years,
            "threshold": threshold,
            "repayment_rate": repayment_rate / 100,
            "salary_growth": salary_growth / 100,
            "salary_growth_sigma": salary_growth_sigma / 100,
            "loan_rate": loan_rate / 100,
            "loan_rate_sigma": loan_rate_sigma / 100,
            "investment_rate": investment_rate / 100,
            "investment_rate_sigma": investment_rate_sigma / 100,
            "child_prob": child_prob / 100,
        }
        
        progress_bar = st.progress(0)
        
        results = []
        for i in range(simulations):
            payments, investment = run_simulation(inputs)
            results.append((payments, investment))
            if i % 100 == 0:
                progress_bar.progress(i / simulations)
        
        payments_arr = np.array([p for p, _ in results])
        investments_arr = np.array([i for _, i in results])
        gain_to_pay_early = payments_arr - investments_arr 

        display_results_summary(payments_arr, investments_arr, gain_to_pay_early)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        is_pay_early_better = np.mean(gain_to_pay_early) > 0
        if is_pay_early_better:
            gain_values = gain_to_pay_early
        else:
            gain_values = -gain_to_pay_early
            
        favorable_scenarios = (gain_to_pay_early > 0).mean() if is_pay_early_better else (gain_to_pay_early < 0).mean()
        
        fig1 = create_gain_plot(gain_values, is_pay_early_better, favorable_scenarios)
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = create_distribution_plot(payments_arr, investments_arr, inputs["current_loan"])
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main() 
