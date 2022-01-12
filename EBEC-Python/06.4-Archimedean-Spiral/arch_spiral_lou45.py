"""
Author: Your Name, login@purdue.edu
Assignment: 06.4 - Arch Spiral
Date: 10/23/2021

Description:
    Draw 'Arch Spiral' by using the module 'math' and 'turtle'

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
from math import pi, sin, cos

# Write new functions below this line (starting with unit 4).


def start():
    """
    This function initializes the window and the turtle.
    Do not modify this function.
    """
    setup(564, 564)
    width('5')


def main():
    """ Write your mainline logic here. """
    tracer(10, 1)

    for theta in range(6 * 360 + 1):
        radians = theta * pi / 180
        dx = theta / (pi * pi) * cos(radians)
        dy = theta / (pi * pi) * sin(radians)

        goto(dx, dy)


if __name__ == '__main__':
    # Do not change this part
    start()
    main()
    done()
