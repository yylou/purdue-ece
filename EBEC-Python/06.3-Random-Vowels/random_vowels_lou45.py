"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 06.3 - Random Vowels
Date: 10/23/2021

Description:
    Randomly draw 'a, e, i, o, u' by imported module 'vowels'

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

from turtle import *

# Import additional modules below this line.
import vowels
import random

# Write new functions below this line (starting with unit 4).


def start():
    """
    This function initializes the window and the turtle.
    Do not modify this function.
    """
    setup(600, 400)
    width(9)
    speed(0)
    penup()
    goto(-220, -30)


def main():
    """ Write your mainline logic here. """

    # Lambda function (from vowels) table
    table = {
                1: lambda x: vowels.draw_a(x),
                2: lambda x: vowels.draw_e(x),
                3: lambda x: vowels.draw_i(x-30),
                4: lambda x: vowels.draw_o(x),
                5: lambda x: vowels.draw_u(x),
            }

    # Shuffle the choice
    choice = list(table.keys())
    random.shuffle(choice)

    # Draw according to the shuffled choice
    for i in range(1, 6):
        table[choice[i-1]](i*90)


if __name__ == '__main__':
    # Do not change this part
    start()
    main()
    done()
