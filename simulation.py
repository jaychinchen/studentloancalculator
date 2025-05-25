import numpy as np

def run_simulation(inputs):
    salary = inputs["initial_salary"]
    loan = inputs["current_loan"]
    investment = inputs["current_loan"]
    total_repayments = 0
    leave_years = 0

    for _ in range(inputs["payback_years"]):
        if np.random.rand() < inputs["child_prob"]:
            leave_years += 1
            loan *= 1 + np.random.normal(
                inputs["loan_rate"],
                inputs["loan_rate_sigma"] / 2
            )
            continue

        salary *= 1 + np.random.normal(
            inputs["salary_growth"],
            inputs["salary_growth_sigma"] / 2
        )
        loan *= 1 + np.random.normal(
            inputs["loan_rate"],
            inputs["loan_rate_sigma"] / 2
        )

        if salary > inputs["threshold"]:
            payment = (salary - inputs["threshold"]) * inputs["repayment_rate"]
            payment = min(payment, loan)
            loan -= payment
            total_repayments += payment

        if loan <= 0:
            break

        investment *= 1 + np.random.normal(
            inputs["investment_rate"],
            inputs["investment_rate_sigma"] / 2
        )

    return total_repayments, investment 