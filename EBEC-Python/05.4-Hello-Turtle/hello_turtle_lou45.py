"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 05.4 - Hello Turtle
Date: 09/28/2021

Description:
    Draw the word pattern "hello turtle" on the screen

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
    setup(600, 400)
    width(9)


def draw_e(width, x=-175, y=50):
    """Write this function."""

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


def draw_h(width, x=-175, y=50):
    """Write this function."""

    penup()
    forward(60)
    pendown()

    setheading(90)
    forward(30)
    circle(30, 180)
    setheading(90)
    forward(90)
    setheading(270)
    forward(120)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_l(width, x=-175, y=50):
    """Write this function."""

    pendown()
    setheading(90)
    forward(120)
    
    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_o(width, x=-175, y=50):
    """Write this function."""

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


def draw_r(width, x=-250, y=-125):
    """Write this function."""

    setheading(90)
    pendown()
    forward(55)
    setheading(270)
    forward(30)
    circle(30, -90)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)


def draw_t(width, x=-250, y=-125):
    """Write this function."""

    penup()
    forward(60)

    pendown()
    setheading(90)
    forward(120)
    penup()
    setheading(270)
    forward(30)
    setheading(180)
    forward(30)
    setheading(0)
    pendown()
    forward(60)

    penup()
    goto(x, y)
    setheading(0)
    forward(width)

def draw_u(width, x=-250, y=-125):
    """Write this function."""

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

def main():
    """
    After these lines, use your letter drawing functions
    to write code that will draw the words "hello turtle".
    """

    speed(0)

    penup()
    goto(-175, 50)

    draw_h(100)
    draw_e(200)
    draw_l(250)
    draw_l(300)
    draw_o(400)

    goto(-250, -125)

    draw_t(120)
    draw_u(220)
    draw_r(240)
    draw_t(360)
    draw_l(400, x=-250, y=-125)
    draw_e(0)
    

# Do not change anything after this line.
if __name__ == '__main__':
    start()
    main()
    done()
