"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 06.1 - Math Quiz
Date: 10/16/2021

Description:
    Pick up two random integers for user to verify the sum value
    - The first random integer has 2 digits
    - The second random integer has 3 digits

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

import random

def random_number(n) -> int:
    """
    Return random integer by specified digits
    """

    """
    Parameters
    ----------
    n : int
        Number of digits
    """
    
    # Given start and end value for random integer range
    range_start = 10 ** (n - 1)
    range_end   = (10 ** n) - 1

    return random.randint(range_start, range_end)
    

def main():
    # output two random integers
    n1 = random_number(2)
    n2 = random_number(3)
    result = n1 + n2
    print(  '{0:>5}'.format(n1))
    print('+ {0:>3}'.format(n2))
    print('-----')

    # user input for potential answer
    user_input = int(input('= '))

    # verify user answer with golden answer
    if result == user_input:
        print('Correct -- Good Work!')

    else:
        print(f'Incorrect. The correct answer is {result}.')

if __name__ == '__main__':
    main()