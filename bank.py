MIN_DURATION = 2592000  # One month in seconds
MAX_DURATION = 15552000  # Six months in seconds


class BankLoan:
    def __init__(self, init_corpus):
        self.init_corpus = init_corpus
        self.loan_applications = []

    def apply_for_loan(self, customer, loan_amount, duration):
        interest_rate = self.calculate_interest_rate(duration)
        self.loan_applications.append({"customer": customer, "loan_amount": loan_amount, "duration": duration, "interest_rate": interest_rate})

    def calculate_interest_rate(self, duration):
        # Assumption: Interest rate is inversely proportional to the time duration between MIN_DURATION and MAX_DURATION
        # Assumption: Higher the duration, the lower the interest rate
        # Assumption: Linear inverse relationship between duration and interest rate for simplicity
        normalized_duration = (duration - MIN_DURATION) / (MAX_DURATION - MIN_DURATION)
        max_interest_rate = 0.1  # Maximum interest rate (10%)
        min_interest_rate = 0.01  # Minimum interest rate (1%)
        interest_rate = max_interest_rate - normalized_duration * (max_interest_rate - min_interest_rate)
        return interest_rate

    def make_installment_payment(self, customer, installment_amount, installment_time, penalty_rate):
        for loan in self.loan_applications:
            if loan["customer"] == customer:
                remaining_principal = loan["loan_amount"]
                interest_rate = loan["interest_rate"]
                duration = loan["duration"]

                # Calculate interest for the installment period
                interest = remaining_principal * interest_rate * installment_time / duration

                # Apply penalty if the installment is late
                if installment_time > duration:
                    penalty = remaining_principal * penalty_rate
                    remaining_principal += penalty

                # Reduce debt from principal and interest component
                remaining_principal -= (installment_amount - interest)

                # Handle surplus payments
                if installment_amount > (remaining_principal + interest):
                    surplus_payment = installment_amount - (remaining_principal + interest)
                    remaining_principal -= surplus_payment

                # Update the loan details
                loan["loan_amount"] = remaining_principal

                # Print payment details
                print(f"Customer: {customer}")
                print(f"Installment Amount: {installment_amount}")
                print(f"Remaining Principal: {remaining_principal}")
                print(f"Interest: {interest}")
                if installment_time > duration:
                    print(f"Penalty: {penalty}")
                if installment_amount > (remaining_principal + interest):
                    print(f"Surplus Payment: {surplus_payment}")


bank = BankLoan(init_corpus=1000000)  # Initialize the bank with a fixed supply of money (INIT_CORPUS)

bank.apply_for_loan("Customer1", 50000, 7776000)  # Customer1 applies for a loan of 50000 with a duration of 90 days (7776000 seconds)
bank.apply_for_loan("Customer2", 100000, 2592000)  # Customer2 applies for a loan of 100000 with a duration of 30 days (2592000 seconds)

# Simulate installment payments, penalties, and surplus payments
bank.make_installment_payment("Customer1", 20000, 7782000, penalty_rate=0.05)
bank.make_installment_payment("Customer2", 30000, 2630000, penalty_rate=0.05)
