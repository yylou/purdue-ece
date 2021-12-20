"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 05.1 - Maze
Date: 09/27/2021

Description:
    Move turtle out of the maze without touching the wall

Contributors:
    Name, login@purdue.edu [repeat for each]

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
    bgpic('maze.png')
    shape('turtle')
    color('green')
    width(5)

def main():
    """
    Write your code below this line.
    """

    right(90)
    forward(11)
    left(90)
    forward(35)
    left(90)
    forward(48)
    right(90)
    forward(48)
    right(90)
    forward(24)
    left(90)
    forward(48)
    right(90)
    forward(24)
    left(90)
    forward(48)
    right(90)
    forward(48)
    left(90)
    forward(48)
    left(90)
    forward(59)
    right(90)
    forward(30)

# Do not change anything after this line.
if __name__ == '__main__':
    start()
    main()
    done()
