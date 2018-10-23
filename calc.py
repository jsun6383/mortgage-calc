import math
import time
import csv

# def get_monthly_payments(interest, principal, nperiod):
#     # monthly repayment = (P*r*(1+r)^n)/((1+r)^n-1)
#     top = principal * interest * ( 1 + interest ) ** nperiod
#     bottom = ( 1 + interest ) ** nperiod - 1 

#     return round(top / bottom, 2)
    

# def calc(interest, principal, length):
#     # convert interest rate from % to actual value and to 
#     # monthly interest rate
#     rate = float(interest) / 100 / 12

#     # length is in years need to convert to month
#     nperiod = int(length) * 12
#     principal = int(principal)
#     monthly_payments = get_monthly_payments(rate, principal, nperiod)

#     print("monthly repayments = $", monthly_payments)

def simulate(interest, principal, payment, fee=None, fee_period=None):

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
    total_fee = 0
    period = 1
    while amount_left > 0:
        interest_paid = amount_left * interest / 12
        principal_paid = payment - interest_paid
        total_interest = total_interest + interest_paid
        if period%fee_period == 0:
            total_fee = total_fee + fee

        amount_left = amount_left - principal_paid

        if amount_left < 0:
            amount_left = 0

        period += 1

    duration = to_years_and_month(period)
    return total_interest, duration, total_fee

def to_years_and_month(num_months):
    years = int(num_months / 12)
    months = (num_months / 12 - years) * 12
    return years, months

def print_result(results):
    
    for result in results:
        print("------------------------------------")
        print("Principal amount: ${:,}".format(int(result[2])))
        print("Interest rate: {:.2f}%".format(float(result[3])))
        print("Monthly repayment: ${:,}".format(int(result[4])))
        print("Total interest paid: ${:,.2f}".format(result[0]))
        print("Total fees paid: ${:,}".format(result[5]))
        print("Total cost of loan: ${:,.2f}".format(result[6]))
        print("Total loan lifetime: {} yrs and {} months".format(result[1][0],int(result[1][1])))
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
            total_interest, duration, total_fee = simulate(interest=interest, 
                                                        principal=principal, 
                                                        payment=payment,
                                                        fee=fee,
                                                        fee_period=fee_period)
            results.append((total_interest, duration, principal, interest, payment, 
                        total_fee, total_interest + total_fee))

    print_result(results)




if __name__ == "__main__":
    input_file = "input.csv"
    process_input(input_file=input_file)