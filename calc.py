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

def simulate(interest, principal, payment):
    # assume monthly payment
    interest = float(interest) / 100
    principal = int(principal)
    payment = float(payment)
    amount_left = principal
    total_interest = 0 
    period = 1
    while amount_left > 0:
        interest_paid = amount_left * interest / 12
        principal_paid = payment - interest_paid
        total_interest = total_interest + interest_paid
        amount_left = amount_left - principal_paid

        if amount_left < 0:
            amount_left = 0

        # print("At the end of period ", period, 
        #       ", total interest paid is $", "%.2f" % round(total_interest, 2), 
        #       ", principal paid this period is $", "%.2f" % round(principal_paid, 2),
        #       ", principal left is $", "%.2f" % round(amount_left, 2), 
        #       sep="")
        period += 1
        # time.sleep(1)
    duration = to_years_and_month(period)
    return total_interest, duration

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
        print("Total loan lifetime: {} yrs and {} months".format(result[1][0],int(result[1][1])))
        print("------------------------------------")


def process_input(input_file):
    results = []
    with open(file=input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for idx, record in enumerate(reader):
            if idx == 0: continue
            if len(record) != 3: 
                raise Exception("Invalid number of elements in input")
            for element in record: 
                try:
                    float(element)
                except ValueError:
                    print("{} on row {} is not a number".format(element, idx))

            principal, interest, payment = record
            total_interest, duration = simulate(interest=interest, 
                                              principal=principal, 
                                              payment=payment)
            results.append((total_interest, duration, principal, interest, payment))

    print_result(results)




if __name__ == "__main__":

    input_file = "input.csv"
    process_input(input_file=input_file)

    # interest = "4.26"
    # principal = "335500"
    # payment = "2500"

    # total_interest, period = simulate(
    #                             interest=interest,
    #                             principal=principal,
    #                             payment=payment
    #                         )

    # print("Principal amount: ${:,}".format(int(principal)))
    # print("Interest rate: {:.2f}%".format(float(interest)))
    # print("Monthly repayment: ${:,}".format(int(payment)))
    # print("Total interest paid: ${:,.2f}".format(total_interest))
    # print("Total loan lifetime: {:.2f} yrs".format(period))