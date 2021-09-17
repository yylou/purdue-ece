"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 03.4 - Organisms
Date: 09/15/2021

Description:
    Predict the approximate size of a population of organisms.

    Allow the user to enter: 
      - starting number of organisms
      - average dailypopulation increase (as a percentage)
      - the number of days the organisms will be left tomultiply

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


def main():
    numbers = []

    # user input for starting number, daily increase, days
    n = float(input('Starting number, in million: '))
    inc = float(input('Average daily increase, in percent: '))
    days = int(input('Number of days to multiply: '))

    # output table header
    print('{0:>3}{1:>14}'.format('Day', 'Approx. Pop'))

    # output daily population after increasing
    for i in range(days + 1):
        if i != 0: n *= 1 + inc/100
        print('{0:>3}{1:>14.4f}'.format(i, n))

if __name__ == '__main__':
    main()