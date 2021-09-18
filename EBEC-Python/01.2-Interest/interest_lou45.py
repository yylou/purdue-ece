"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 01.2 - Interest
Date: 08/31/2021

Description:
    Calculate the balance of the account after a specified number of years
    based on the formula: FV = P(1+r/n)^(nt)

Contributors:
    n/a

My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import math

def round_half_up(n, precision=2) -> float:
    """
    This function aims at rounding half up of the input floating point with
    precision of 2 as default.
    (ex. 3.145 = 3.15, 2.143 = 2.14)
    """

    """
    Parameters
    ----------
    n : float
        Input number
    precision : int
        Precision of floating point
    """
    return math.floor(n * 10**precision + 0.5) / 10**precision

def calculate_interest(p, r, n, t) -> float:
    """
    Main function to calculate the interest based on the following formula:
        FV = P(1+r/n)^(nt)
    """

    """
    Parameters
    ----------
    p : float
        Principal amount that was originally depositedinto the account
    r : float
        Annual interest rate
    n :	float
        Number of times per year that the interestis compounded
    t : float
        Specified number of year
    """
    return round_half_up(p * (1 + r/100/n) ** (n * t))

def main():
    # Input from users
    print('Please enter the following quantities.')
    p = float(input('  How much is the initial deposit? '))
    r = float(input('  What is the annual interest rate in percent? '))
    n = float(input('  How many times per year is the interest compounded? '))
    t = float(input('  How many years will the account earn interest? '))
    print()

    # Main functions for calculating interest
    fv = calculate_interest(p, r, n, t)

    # Output final answer
    print('At the end of {0} years, this account will be worth {1}.'.format(t, '${:,.2f}'.format(fv)))

if __name__ == '__main__':
    main()
