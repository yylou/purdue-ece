"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 02.5 - Fluid Mechanics
Date: 09/15/2021

Description:
    Calculate the Reynold snumber based on the input values:
        - Velocity of the water flowing through a pipe (V)
        - Pipe’s diameter (d)
        - Water’s temperature (T) from 5C, 10C, and 15C

    Formula: Re = (Vd)

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


def reynolds_number(t, v, d) -> float:
    """
    Calculate the Reynold snumber
    """

    """
    Parameters
    ----------
    t : float
        Water’s temperature
    v: float
        Velocity of the water
    d: float
        Pipe’s diameter
    """

    kinematic_viscosity = {
         5: 1.49 * (10 ** -6),
        10: 1.31 * (10 ** -6),
        15: 1.15 * (10 ** -6),
    }

    return v*d / kinematic_viscosity[t]

def main():
    # user input for specific year
    t = float(input('Enter the temperature in \u00B0C as 5, 10, or 15: '))
    v = float(input('Enter the velocity of water in the pipe: '))
    d = float(input('Enter the pipe\'s diameter: '))

    # check for pocket number
    re = reynolds_number(t, v, d)

    # output final answer
    print('At {0}\u00B0C, the Reynolds number for flow at {1} m/s in a {2} m diameter pipe is {3:.2e}.'.format(t, v, d, re))

if __name__ == '__main__':
    main()