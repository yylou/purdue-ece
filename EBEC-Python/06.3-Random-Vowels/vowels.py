"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 06.3 - Random Vowels
Date: 10/23/2021

Description:
    Modules imported by 'random_vowels_lou45.py' to randomly draw 'a, e, i, o, u'

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


def draw_a(width, x=-220, y=-30):
    """ Complete this function to draw the character a. """
    penup()
    forward(60)
    setheading(90)
    forward(30)
    pendown()

    circle(30)

    setheading(90)
    forward(30)
    setheading(270)
    forward(60)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_e(width, x=-220, y=-30):
    """ Complete this function to draw the character e. """
    penup()
    setheading(90)
    forward(30)
    pendown()

    setheading(0)
    forward(60)
    setheading(90)
    circle(30, 310, steps=20)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_i(width, x=-220, y=-30):
    """ Complete this function to draw the character i. """
    penup()
    setheading(90)
    forward(100)
    pendown()
    dot(10)

    penup()
    setheading(270)
    forward(30)
    pendown()
    forward(70)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_o(width, x=-220, y=-30):
    """ Complete this function to draw the character o. """
    penup()
    forward(60)
    setheading(90)
    forward(30)
    pendown()

    circle(30)
    
    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_u(width, x=-220, y=-30):
    """ Complete this function to draw the character u. """
    penup()
    setheading(90)
    forward(55)
    
    pendown()
    setheading(270)
    forward(25)
    circle(30, 180)
    penup()
    forward(25)
    pendown()
    setheading(270)
    forward(55)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)


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
    """ You can use this for your own testing. """
    pass


if __name__ == '__main__':
    # Do not change this part
    start()
    main()
    done()
