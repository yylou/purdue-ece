"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 01.3 - Cookie Recipe
Date: 09/01/2021

Description:
    Displays the number of cups of each ingredient needed to make the specified
    number of cookies.

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

import math

def cookie_recipe(n) -> list:
    """
    Calculate the amount of each ingredient based on the following settings:
        48 cookies = 1.75 cups of sugar +
                     1 cup of butter    +
                     2.5 cups of flour
    """

    """
    Parameters
    ----------
    n : int
        Specified number of cookies
    """

    x = n / 48.
    recipe = [1.75 * x, 1 * x, 2.5 * x]

    # Apply the built-in function 'round' on each value in the list 'recipe'
    return [round(_, 2) for _ in recipe]

def main():
    # Input from users
    n = int(input('How many cookies do you want to make? '))

    # Main functions to get cookie recipe
    recipe = cookie_recipe(n)

    # Output final answer
    print('To make {0} cookies, you will need:'.format(n))
    print('{:>7.2f} cups of sugar'.format(recipe[0]))
    print('{:>7.2f} cups of butter'.format(recipe[1]))
    print('{:>7.2f} cups of flour'.format(recipe[2]))

if __name__ == '__main__':
    main()
