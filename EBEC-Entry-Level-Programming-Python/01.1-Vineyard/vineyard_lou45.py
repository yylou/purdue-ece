"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 01.1 - Vineyard
Date: 09/02/2021

Description:
    Calculate the number of vines that will fit in the row based on the several
    parameters and the forumula: V = (R - 2E) / S
        V is the number of grapevines that will fit in the row
        R is the length of the row
        E is the amount of space
        S is the space between vines

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

def calculate_vineyard(s, e, r) -> int:
    """
    Main function to calculate the number of vines based on following forumula:
        V = (R - 2E) / S
    """

    """
    Parameters
    ----------
    s : float
        Amount of space between the vines, in meters
    e : float
        Amount of space used by an end-post assembly, in meters
    r : float
        Length of the row, in meters
    """
    return int((r - 2 * e) / s)

def main():
    # Input from users
    print('Enter each of the following quantities in meters.')
    s = float(input('  How much space should be between the vines? '))
    e = float(input('  How wide is the end-post assembly? '))
    r = float(input('  How long is this row? '))
    print()

    # Main functions for calculating the number of vines
    n = calculate_vineyard(s, e, r)

    # Output final answer
    print('This row has enough space for {0} vine(s).'.format(n))

if __name__ == '__main__':
    main()
