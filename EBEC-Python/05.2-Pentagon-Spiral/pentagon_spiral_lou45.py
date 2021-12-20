"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 05.2 - Pentagon Spiral
Date: 09/28/2021

Description:
    Draw the pentagonal spiral
    - The length of the spiral’s sides start at 8 pixels
      and increase by 8 pixels after every 72 degree

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
    width(5)

def main():
    """
    Write your code below this line.
    """

    # iterate through each edge of the spiral pentagon
    for i in range(1, 34):        
        forward(i * 8)
        left(72)

# Do not change anything after this line.
if __name__ == '__main__':
    start()
    main()
    done()
