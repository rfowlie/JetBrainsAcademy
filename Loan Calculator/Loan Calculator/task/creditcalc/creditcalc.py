# import sys
import argparse
import math


def calc_diff(principal, interest, period, month_curr):
    return math.ceil((principal / period) + calc_nominal(interest)
                     * (principal - ((principal * (month_curr - 1)) / period)))


def calc_nominal(interest):
    return interest / 1200


def calc_body(interest, period):
    nominal_interest = calc_nominal(interest)
    return (nominal_interest * math.pow(1 + nominal_interest, period)) / (math.pow(1 + nominal_interest, period) - 1)


def calc_annuity(principal, interest, period):
    return math.ceil(principal * calc_body(interest, period))


def calc_principal(annuity, interest, period):
    return annuity / calc_body(interest, period)


def calc_months(principle, interest, payment):
    nominal_interest = calc_nominal(interest)
    x = payment / (payment - nominal_interest * principle)
    base = 1 + nominal_interest
    return math.ceil(math.log(x, base))


def incorrect():
    print("Incorrect parameters")


def diff():
    sum_ = 0
    for i in range(1, periods_ + 1):
        payment = calc_diff(principal_, interest_, periods_, i)
        sum_ += payment
        print(f"Month {i}: payment is {payment}")
    print()
    print(f"Overpayment = {sum_ - principal_}")


# create parser
parser = argparse.ArgumentParser()
parser.add_argument("--type", choices=["annuity", "diff"], help="Incorrect parameters")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")

# get command line values
args = parser.parse_args()

type_ = args.type
principal_ = int(args.principal) if args.principal is not None else None
periods_ = int(args.periods) if args.periods is not None else None
interest_ = float(args.interest) if args.interest is not None else None
payment_ = int(args.payment) if args.payment is not None else None


def print_months():
    months_total = calc_months(principal_, interest_, payment_)
    years = months_total // 12
    months = months_total % 12
    if years != 0 and months != 0:
        print(f"It will take {years} years and {months} months to repay this loan!")
    elif years == 0:
        print(f"It will take {months} months to repay this loan!")
    elif months == 0:
        print(f"It will take {years} years to repay this loan!")
    print(f"Overpayment = {payment_ * months_total - principal_}")


def print_annuity():
    ann_payment = calc_annuity(principal_, interest_, periods_)
    print(f"Your annuity payment = {ann_payment}!")
    print(f"Overpayment = {ann_payment * periods_ - principal_}")


def print_principal():
    principal_total = calc_principal(payment_, interest_, periods_)
    print(f"Your loan principal = {principal_total}!")
    print(f"Overpayment = {payment_ * periods_ - principal_total}")


# output depending on combination of parameters passed in...this is ugly lol
if interest_ is not None and (type_ == "diff" or type_ == "annuity"):
    if type_ == "diff" and payment_ is None:
        if principal_ is not None and periods_ is not None and interest_ is not None:
            diff()
        else:
            incorrect()
    elif type_ == "annuity":
        if principal_ is not None:
            if payment_ is not None:
                print_months()
            elif periods_ is not None:
                print_annuity()
            else:
                incorrect()
        elif payment_ is not None and periods_ is not None:
            print_principal()
        else:
            incorrect()
else:
    incorrect()
