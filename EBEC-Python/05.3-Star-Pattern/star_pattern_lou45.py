"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 05.3 - Star Pattern
Date: 09/28/2021

Description:
    Draw the star pattern that has a user specified number of point.

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

def start():
    """
    This function initializes the window and the turtle.
    Do not modify this function.
    """
    setup(564, 564)
    width(7)
    side_length = 60 # Also the radius of a circle enclosed by the star.
    penup()
    goto(0, -side_length) # Start at the bottom of the star.
    pendown()

def main():
    """
    Write your code below this line.
    """

    point = int(input('How many points they want on the star: '))

    inner_angle = 360 / point
    outer_angle = 2 * inner_angle

    # set fill color
    fillcolor("yellow")
    begin_fill()

    right(90 - inner_angle)

    for _ in range(point):
        forward(60)
        left(180 - inner_angle)
        forward(60)
        right(180 - outer_angle)

    # fill color
    end_fill()

# Do not change anything after this line.
if __name__ == '__main__':
    start()
    main()
    done()
