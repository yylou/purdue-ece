"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 02.3 - Roulette Colors
Date: 09/15/2021

Description:
    Given a specific pocket number, return the color of that pocket.

    The rules are as follows:
        n = 0, color = green
        n in [ 1, 10], color = black if n % 2 == 0 else red
        n in [11, 18], color = red   if n % 2 == 0 else black
        n in [19, 28], color = black if n % 2 == 0 else red
        n in [29, 36], color = red   if n % 2 == 0 else black

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


def check_color(n) -> str:
    """
    Given a specific pocket number, return the color of that pocket.
    """

    """
    Parameters
    ----------
    n : int
        The pocket number
    """

    if n == 0: return 'green'
    if  1 <= n <= 10: return 'red'   if n % 2 else 'black'
    if 11 <= n <= 18: return 'black' if n % 2 else 'red'
    if 19 <= n <= 28: return 'red'   if n % 2 else 'black'
    if 29 <= n <= 36: return 'black' if n % 2 else 'red'

def main():
    # user input for specific year
    n = int(input('Please choose a pocket number: '))
    if not (0 <= n <= 36): print('  Invalid Input!'); return

    # check for pocket number
    color = check_color(n)

    # output final answer
    print('  Pocket number {0} is {1}.'.format(n, color))

if __name__ == '__main__':
    main()