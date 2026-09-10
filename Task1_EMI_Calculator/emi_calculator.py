"""
Task 1: Loan EMI Calculator
Internship: Saiket Systems
Description: Calculates monthly EMI, total interest, and total payable amount based on user inputs.
"""

def calculate_emi(principal: float, monthly_rate_percent: float, tenure_months: int) -> tuple[float, float, float]:
    """
    Calculates EMI using the standard formula:
    EMI = [P x r x (1+r)^N] / [(1+r)^N - 1]
    
    Where:
    - P = Principal loan amount
    - r = Monthly interest rate in fraction (rate% / 100)
    - N = Loan tenure in months
    """
    r = monthly_rate_percent / 100.0

    # Special case: 0% interest rate
    if r == 0:
        emi = principal / tenure_months
        total_payment = principal
        total_interest = 0.0
        return emi, total_interest, total_payment

    # Standard EMI Formula
    # (1 + r)^N
    power_term = (1 + r) ** tenure_months
    
    # EMI = P * r * (1+r)^N / ((1+r)^N - 1)
    emi = (principal * r * power_term) / (power_term - 1)
    
    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    return emi, total_interest, total_payment


def main():
    print("=" * 45)
    print("       📊 LOAN EMI CALCULATOR 📊       ")
    print("=" * 45)

    while True:
        try:
            # 1. Input Principal Amount
            principal_input = input("\nEnter loan amount (Principal in ₹): ").strip()
            principal = float(principal_input)
            if principal <= 0:
                print("❌ Loan amount must be greater than 0. Please try again.")
                continue

            # 2. Input Monthly Interest Rate
            rate_input = input("Enter monthly interest rate (in %): ").strip()
            monthly_rate = float(rate_input)
            if monthly_rate < 0:
                print("❌ Interest rate cannot be negative. Please try again.")
                continue

            # 3. Input Loan Tenure in Months
            tenure_input = input("Enter loan tenure (in months): ").strip()
            tenure = int(tenure_input)
            if tenure <= 0:
                print("❌ Loan tenure must be at least 1 month. Please try again.")
                continue

            # Calculate EMI & Summary
            emi, total_interest, total_payment = calculate_emi(principal, monthly_rate, tenure)

            # Display Results
            print("\n" + "-" * 45)
            print("                🧾 LOAN SUMMARY")
            print("-" * 45)
            print(f" Principal Amount     : ₹ {principal:,.2f}")
            print(f" Monthly Interest Rate: {monthly_rate:.2f}%")
            print(f" Loan Tenure          : {tenure} months")
            print("-" * 45)
            print(f" 👉 Your Monthly EMI  : ₹ {emi:.2f}")
            print(f" Total Interest       : ₹ {total_interest:,.2f}")
            print(f" Total Payable Amount : ₹ {total_payment:,.2f}")
            print("=" * 45)

        except ValueError:
            print("❌ Invalid input! Please enter valid numeric values.")
            continue

        # Check if user wants to calculate another
        choice = input("\nDo you want to calculate another EMI? (y/n): ").strip().lower()
        if choice not in ('y', 'yes'):
            print("\nThank you for using Loan EMI Calculator! Goodbye. 👋\n")
            break


if __name__ == "__main__":
    main()
