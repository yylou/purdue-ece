"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 07.3 - Roll Analysis
Date: 10/25/2021

Description:
    Simulating rolling a pair of dices for 1,000,000 times
    And calculate the percentage of possible results from 2 to 12

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

def roll_d6() -> int:
    """
    For simulating rolling dices, return random integer from 1 to 6
    """

    return random.randint(1, 6)

def get_2d6_rolls(n) -> list:
    """
    Calculate the falling distance
    """

    """
    Parameters
    ----------
    n : int
        Iterations
    """
    
    results = []

    for _ in range(n):
        total = roll_d6() + roll_d6()
        results.append(total)

    return results

def main():
    # Get results of randomly rolling a pair of dices
    n = 1000000
    results = get_2d6_rolls(n)

    # Calculate the percentage of total from 2 to 12
    percentage = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    for element in results: percentage[element] += 1
    for key in percentage: percentage[key] = percentage[key] / n

    # Output the answer
    print('Roll  Frequency')
    for key in sorted(percentage):
        print(f'{key:>3}   {percentage[key] * 100:>6.2f}%')

if __name__ == '__main__':
    main()