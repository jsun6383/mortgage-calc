import math
import time
import csv
import json
import plot

def get_monthly_payments(interest, principal, nperiod):
    # monthly repayment = (P*r*(1+r)^n)/((1+r)^n-1)
    top = principal * interest * ( 1 + interest ) ** nperiod
    bottom = ( 1 + interest ) ** nperiod - 1 

    return round(top / bottom, 2)
    

def calc_monthly_payment(interest, principal, length):
    # convert interest rate from % to actual value and to 
    # monthly interest rate
    rate = float(interest) / 100 / 12

    # length is in years need to convert to month
    nperiod = int(length) * 12
    principal = int(principal)
    return get_monthly_payments(rate, principal, nperiod)

def get_payment_range(total_payment, payment_a):
    payment_range_a = list(range(payment_a - 200, payment_a + 1000, 100))
    payment_range_b = []
    for payment in payment_range_a:
        if payment <= 0:
            raise Exception("Payment too low")
        payment_range_b.append(total_payment - payment)

    return payment_range_a, payment_range_b
    
def generate_graph(total_payment, loan_a, loan_b):
    # loan_a and loan_b follow:
    # {
    #     "principal": 550000,
    #     "interest": 4.37,
    #     "payment": 2000
    # }
    # where payment is monthly payment

    payment_a = loan_a["payment"]
    payment_range_a, payment_range_b = get_payment_range(total_payment, payment_a)
    record_a = {
        "principal": loan_a["principal"],
        "interest": loan_a["interest"],
        "payment_range": payment_range_a
    }
    record_b = {
        "principal": loan_b["principal"],
        "interest": loan_b["interest"],
        "payment_range": payment_range_b
    }

    total_costs = []

    for x in range(0, len(record_a["payment_range"]) - 1):
        total_interest_a, _, total_fees_a = simulate(
            interest=record_a["interest"], 
            principal=record_a["principal"], 
            payment=record_a["payment_range"][x])

        total_interest_b, _, total_fees_b = simulate(
            interest=record_b["interest"], 
            principal=record_b["principal"], 
            payment=record_b["payment_range"][x])

        total_costs.append(total_interest_a + total_interest_b + 
            total_fees_a + total_fees_b)

    plot.plot_result(payment_range_a, payment_range_b, total_costs)
            

def simulate(interest, principal, payment, fee=0, fee_period="yearly"):

    if fee_period == "yearly":
        fee_period = 12
    elif fee_period == "bi-yearly":
        fee_period = 6
    elif fee_period == "monthly":
        fee_period = 1
    else:
        raise Exception("fee_period of {} is not supported".format(fee_period))

    # assume monthly payment
    interest = float(interest) / 100
    principal = int(principal)
    payment = float(payment)
    fee = int(fee)
    amount_left = principal
    total_interest = 0 
    total_fees = 0
    period = 1
    while amount_left > 0:
        interest_paid = amount_left * interest / 12
        principal_paid = payment - interest_paid
        if principal_paid <= 0:
            raise Exception("Payment ${:,.2f} is too low for principal ${:,.0f}."
                .format(payment, principal))
        total_interest = total_interest + interest_paid
        if period%fee_period == 0:
            total_fees = total_fees + fee

        amount_left = amount_left - principal_paid
        # print("amount left = ${:,.2f}".format(amount_left))

        if amount_left < 0:
            amount_left = 0

        period += 1

    duration = to_years_and_month(period)
    return total_interest, duration, total_fees

def to_years_and_month(num_months):
    years = int(num_months / 12)
    months = (num_months / 12 - years) * 12
    return years, months

def print_result(results):
    
    for result in results:
        print("------------------------------------")
        print("Principal amount: ${:,}".format(int(result["principal"])))
        print("Interest rate: {:.2f}%".format(float(result["interest"])))
        print("Monthly repayment: ${:,}".format(int(result["payment"])))
        print("Minimum monthly repayment: ${:,}".format(int(result["min_payment"])))
        print("Total interest paid: ${:,.2f}".format(result["total_interest"]))
        print("Total fees paid: ${:,}".format(result["total_fees"]))
        print("Total cost of loan: ${:,.2f}".format(result["total_cost"]))
        print("Total loan lifetime: {} yrs and {} months".format(result["duration"][0],int(result["duration"][1])))
        print("------------------------------------")
    
    print("Total cost of all loans: ${:,.2f}".format(get_total_cost_of_all_loans(results)))
    print("------------------------------------")


def process_input(input_file):
    results = []
    with open(file=input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for idx, record in enumerate(reader):
            if idx == 0: continue
            if len(record) != 5: 
                raise Exception("Invalid number of elements in input")

            # check each element of the record and make sure they are a number for
            # the first 4 fields and a valid period for the 5th period.
            for element in record: 
                try:
                    if element in ["yearly","monthly","by-yearly"]: continue
                    float(element)
                except ValueError:
                    print("{} on row {} is not in the expected format".format(element, idx))

            principal, interest, payment, fee, fee_period = record
            total_interest, duration, total_fees = simulate(interest=interest, 
                                                        principal=principal, 
                                                        payment=payment,
                                                        fee=fee,
                                                        fee_period=fee_period)
            min_payment = calc_monthly_payment(interest, principal, 30)
            
            results.append(dict(
                total_interest=total_interest, 
                duration=duration, 
                principal=principal, 
                interest=interest, 
                payment=payment,
                min_payment=min_payment,
                total_fees=total_fees, 
                total_cost=total_interest + total_fees))

    print_result(results)
    return results

def get_total_cost_of_all_loans(results):
    total_cost = 0
    for result in results:
        total_cost = total_cost + result["total_cost"]
    return total_cost

if __name__ == "__main__":
    input_file = "input.csv"
    results = process_input(input_file=input_file)

    # loan_a = {
    #     "principal": int(results[0]["principal"]),
    #     "interest": float(results[0]["interest"]),
    #     "payment": int(results[0]["min_payment"])
    # }

    # loan_b = {
    #     "principal": int(results[1]["principal"]),
    #     "interest": float(results[1]["interest"]),
    #     "payment": int(results[1]["min_payment"])
    # }

    # generate_graph(6000, loan_a, loan_b)

