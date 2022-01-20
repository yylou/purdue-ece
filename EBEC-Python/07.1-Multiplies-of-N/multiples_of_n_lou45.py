"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 07.1 - Multiples of N
Date: 10/25/2021

Description:
    Check whether each number in the defined list is the multiples of number '13'

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

def multiples_of(n, int_list) -> list:
    """
    Check whether each number in the input list is the multiples of input n
    """

    """
    Parameters
    ----------
    n : int
        base number

    int_list : list
        list of numbers
    """
    
    return [x for x in int_list if abs(x) % n == 0]

def main():
    # Original List
    ori = [19, 1599, -546, 10, 39, -58, 1, 85, 201, -91, 286, 799, 406]
    print(f'Original list of numbers:\n  {ori}')

    # Get the answer from the output of function 'multiples_of'
    ans = multiples_of(13, ori)
    print(f'Numbers in the list that are multiples of 13:\n  {ans}')

if __name__ == '__main__':
    main()