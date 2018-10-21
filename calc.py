import math
import time

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
    period = period / 12 # convert period to years
    return total_interest, period

if __name__ == "__main__":
    # interest = input("What is the interest rate? ")
    # principal = input("What is the principal? ")
    # length = input("How many years is the loan? ")

    # calc(
    #     interest="4.26",
    #     principal="335500",
    #     length="30"
    # )

    total_interest, period = simulate(
                                interest="4.26",
                                principal="335500",
                                payment="2500"
                            )
    
    print("Total interest paid: ${:,.2f}\nTotal loan lifetime: {:.2f} yrs".format(total_interest, period))