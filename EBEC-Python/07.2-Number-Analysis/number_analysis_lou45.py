"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 07.2 - Number Analysis
Date: 10/25/2021

Description:
    Get 10 numbers from user input and use MAX, MIN, SUM for analysis

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

def get_number_list() -> list:
    """
    Get numbers from user inpus
    """

    numbers = []
    for _ in range(10):
        n = float(input(f'  number {_+1:>2} of 10: '))
        numbers.append(n)
    
    return numbers

def main():
    # Get 10 numbers from user input
    print('Enter 10 numbers:')
    numbers = get_number_list()

    # MAX / MIN / Total / AVG
    print(f'Highest number: {max(numbers):.2f}')
    print(f'Lowest number: {min(numbers):.2f}')
    print(f'Total: {sum(numbers):.2f}')
    print(f'Average: {sum(numbers) / 10:.2f}')

if __name__ == '__main__':
    main()