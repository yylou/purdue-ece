"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 03.2 - Sum Average
Date: 09/15/2021

Description:
     A loop that asks the user to enter a series of non-negative num-bers (positive numbers or zero). 
     The user should enter a negative number to signal the end ofthe series. 
     
     After all the non-negative numbers have been entered, the program should displaytheir sum and average.

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

    # user input for non-negative number 
    while True:
        n = float(input('Enter a non-negative number (negative to quit): '))
        if n < 0: break
        else: numbers.append(n)

    # number of input is ZERO
    if len(numbers) == 0: print('  You didn\'t enter any numbers.'); return

    # output number of inputs and the sum and averasge
    print('  You entered {0} numbers.'.format(len(numbers)))
    print('  Their sum is {0:.3f} and their average is {1:.3f}.'.format(sum(numbers), sum(numbers) / len(numbers)))

if __name__ == '__main__':
    main()