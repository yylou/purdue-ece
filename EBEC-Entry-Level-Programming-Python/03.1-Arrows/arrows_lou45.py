"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 03.1 - Arrows
Date: 09/15/2021

Description:
    Uses nested loops to draw the pattern of arrow

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
    # user input for number of arrows
    n = int(input('How many arrows should I draw? '))

    # output arrows: outer loop for printing '<' and '>'
    for i in range(n):
        print('<', end='')

        # nested loop for printing '-'
        for j in range(i): print('-', end='')

        print('>')

if __name__ == '__main__':
    main()