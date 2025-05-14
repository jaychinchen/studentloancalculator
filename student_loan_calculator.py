import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_simulation(inputs):
    """Run a single Monte Carlo simulation with given inputs"""
    salary = inputs["initial_salary"]
    loan = inputs["current_loan"]
    investment = inputs["current_loan"]
    total_repayments = 0
    leave_years = 0

    for _ in range(inputs["payback_years"]):  # Changed from years to payback_years
        # Check for child leave
        if np.random.rand() < inputs["child_prob"]:
            leave_years += 1
            loan *= 1 + np.random.normal(
                inputs["loan_rate"],
                inputs["loan_rate_sigma"]
            )
            continue

        # Update salary and loan with growth/interest
        salary *= 1 + np.random.normal(
            inputs["salary_growth"],
            inputs["salary_growth_sigma"]
        )
        loan *= 1 + np.random.normal(
            inputs["loan_rate"],
            inputs["loan_rate_sigma"]
        )

        # Calculate loan repayment
        if salary > inputs["threshold"]:
            payment = (salary - inputs["threshold"]) * inputs["repayment_rate"]
            payment = min(payment, loan)
            loan -= payment
            total_repayments += payment

        if loan <= 0:
            break

        # Calculate investment returns
        investment *= 1 + np.random.normal(
            inputs["investment_rate"],
            inputs["investment_rate_sigma"]
        )

    return total_repayments, investment

def main():
    # Set the style for all plots with larger font size
    sns.set_theme(style="whitegrid", font_scale=1.4)
    
    st.title("Student Loan Calculator")
    st.markdown("""
    This calculator helps you decide whether to pay off your student loan early by comparing:
    - Expected total repayments over time
    - Potential returns if you invested the money instead
    """)

    # Loan and Salary Information
    st.header("Loan and Salary Information")
    st.markdown("Enter your current loan details and salary information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        initial_salary = st.number_input("Current Annual Salary (£)", value=50000, min_value=0)
        current_loan = st.number_input("Outstanding Loan Amount (£)", value=50000, min_value=0)
        payback_years = st.number_input("Years Remaining for Repayment", value=15, min_value=1, max_value=50, step=1)
    
    with col2:
        threshold = st.number_input("Repayment Threshold (£)", value=27000, min_value=0)
        repayment_rate = st.number_input("Repayment Rate", value=0.09, min_value=0.0, max_value=1.0, step=0.01)

    # Scenario Parameters
    st.header("Scenario Parameters")
    st.markdown("Configure the simulation parameters for different economic scenarios")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Growth Rates")
        salary_growth = st.number_input("Expected Salary Growth per Year", value=0.05, min_value=0.0, max_value=1.0, step=0.01)
        salary_growth_sigma = st.number_input("Salary Growth Variation", value=0.03, min_value=0.0, max_value=1.0, step=0.01)
        loan_rate = st.number_input("Loan Interest Rate", value=0.06, min_value=0.0, max_value=1.0, step=0.01)
        loan_rate_sigma = st.number_input("Loan Interest Rate Variation", value=0.03, min_value=0.0, max_value=1.0, step=0.01)
    
    with col4:
        st.subheader("Investment & Life Events")
        investment_rate = st.number_input("Investment Return Rate", value=0.025, min_value=0.0, max_value=1.0, step=0.01)
        investment_rate_sigma = st.number_input("Investment Return Variation", value=0.01, min_value=0.0, max_value=1.0, step=0.01)
        child_prob = st.number_input("Probability of Career Break per Year", value=0.1, min_value=0.0, max_value=1.0, step=0.01)
        simulations = st.number_input("Number of Simulations", value=10000, min_value=100, max_value=100000, step=100)

    # Create inputs dictionary
    inputs = {
        "initial_salary": initial_salary,
        "current_loan": current_loan,
        "payback_years": payback_years,  # Changed from years to payback_years
        "threshold": threshold,
        "repayment_rate": repayment_rate,
        "salary_growth": salary_growth,
        "salary_growth_sigma": salary_growth_sigma,
        "loan_rate": loan_rate,
        "loan_rate_sigma": loan_rate_sigma,
        "investment_rate": investment_rate,
        "investment_rate_sigma": investment_rate_sigma,
        "child_prob": child_prob
    }

    if st.button("Run Simulation", type="primary"):
        # Show progress bar
        progress_bar = st.progress(0)
        
        # Run simulations
        results = []
        for i in range(simulations):
            payments, investment = run_simulation(inputs)
            results.append((payments, investment))
            if i % 100 == 0:  # Update progress every 100 simulations
                progress_bar.progress(i / simulations)
        
        # Convert results to arrays
        payments_arr = np.array([p for p, _ in results])
        investments_arr = np.array([i for _, i in results])
        gain_to_pay_early = payments_arr - investments_arr 

        # Display summary statistics
        st.subheader("Results Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Expected Total Loan Repayment", f"£{np.mean(payments_arr):,.2f}")
            st.metric("Expected Investment Returns", f"£{np.mean(investments_arr):,.2f}")
            st.metric("Expected Gain from Investing Early", f"£{np.mean(gain_to_pay_early):,.2f}")
        
        with col2:
            st.metric("Median Loan Repayment", f"£{np.median(payments_arr):,.2f}")
            st.metric("Median Investment Returns", f"£{np.median(investments_arr):,.2f}")
            st.metric("Probability of Better Returns", f"{(gain_to_pay_early > 0).mean():.1%}")

        # Create and display plots
        st.subheader("Visualisation")
        
        # Plot 1: Gain/Loss Distribution
        fig1, ax1 = plt.subplots(figsize=(12, 7))
        # Main distribution
        sns.histplot(
            data=gain_to_pay_early,
            bins=40,
            stat="density",
            alpha=0.6,
            color="#0068C9",  # Streamlit blue
            edgecolor="white",
            linewidth=0.5
        )
        # Add vertical line at break-even point
        ax1.axvline(
            0,
            color="#FF2B2B",  # Streamlit red
            linestyle="--",
            linewidth=2,
            label="Break-even point"
        )
        # Add mean line
        mean_gain = np.mean(gain_to_pay_early)
        ax1.axvline(
            mean_gain,
            color="#00CC96",  # Streamlit green
            linestyle="--",
            linewidth=2,
            label=f"Mean: £{mean_gain:,.0f}"
        )
        # Customize the plot
        ax1.set_title(
            "Expected Returns if Paying Loan Early",
            pad=20,
            fontsize=16,
            fontweight="bold"
        )
        ax1.set_xlabel("Investment Gain/Loss vs Loan Repayment (£)", fontsize=14)
        ax1.set_ylabel("Frequency", fontsize=14)
        ax1.legend(fontsize=12, framealpha=0.8)
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

        # Plot 2: Comparison Distribution
        fig2, ax2 = plt.subplots(figsize=(12, 7))
        # Plot the distributions
        sns.histplot(
            data=payments_arr,
            bins=40,
            stat="density",
            alpha=0.6,
            color="#FF2B2B",  # Streamlit red
            label="Loan Repayments",
            edgecolor="white",
            linewidth=0.5
        )
        sns.histplot(
            data=investments_arr,
            bins=40,
            stat="density",
            alpha=0.6,
            color="#00CC96",  # Streamlit green
            label="Investment Growth",
            edgecolor="white",
            linewidth=0.5
        )
        # Add original loan amount line
        ax2.axvline(
            inputs["current_loan"],
            color="#0068C9",  # Streamlit blue
            linestyle="--",
            linewidth=2,
            label=f"Original Loan: £{inputs['current_loan']:,}"
        )
        # Customize the plot
        ax2.set_title(
            "Loan Repayments vs Investment Returns",
            pad=20,
            fontsize=16,
            fontweight="bold"
        )
        ax2.set_xlabel("Total Value (£)", fontsize=14)
        ax2.set_ylabel("Frequency", fontsize=14)
        ax2.legend(fontsize=12, framealpha=0.8)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

if __name__ == "__main__":
    main()
