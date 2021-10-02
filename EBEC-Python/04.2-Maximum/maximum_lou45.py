"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 04.2 - Maximum
Date: 09/27/2021

Description:
    Find the maximum from user input of two integers

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

def max_of_two(n1, n2) -> int:
    """
    Find the greater number
    """

    """
    Parameters
    ----------
    n1 : int
        Number 1
    n2 : int
        Number 2
    """
    
    # return n1 if n1 is greater than n2, else return n2
    return n1 if n1 > n2 else n2

def main():
    # user input for two integers
    n1 = int(input('Enter the first integer: '))
    n2 = int(input('Enter the second integer: '))

    # output the answer
    print ('The number {0} is greater.'.format(max_of_two(n1, n2)))

if __name__ == '__main__':
    main()