"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 02.2 - Software Sales
Date: 09/06/2021

Description:
    Given a table that shows discounts rate given by a specific quantity and
    a package that retails for $79, calculate the final price.

        Quantity        Discount
        ------------------------
         5 - 24         10%
        25 - 49         20%
        50 - 99         30%
        100+            45%

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


import sys


def price(n, discount) -> float:
    """
    Given a table that shows discounts rate given by a specific quantity and
    a package that retails for $79, calculate the final price.
    """

    """
    Parameters
    ----------
    n : int
        The number of purchased packages
    discount : int
        The discount rate
    """

    return n * 79 * (1 - discount / 100.)

def main():
    # user input for specific year
    n = int(input('How many packages will be purchased: '))
    if n < 0: print('  Invalid Input!'); return

    discount_table = {
          5: 0,
         25: 10,
         50: 20,
        100: 30,
        float('inf'): 45
    }

    # calculate the discount rate
    discount = 0
    for key in sorted(discount_table):
        if n < key: discount = discount_table[key]; break

    if discount == 0: print('  No discount applied.')
    else: print('  {0}% discount applied.'.format(discount))

    # output final answer
    print('  The total price for purchasing {0} packages is ${1:,.2f}.'.format(n, price(n, discount)))

if __name__ == '__main__':
    main()
