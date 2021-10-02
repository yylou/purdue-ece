"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 04.5 - Prime List
Date: 09/27/2021

Description:
    Find the prime list by reusing 04.4 - Prime Number

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

def sqrt(n) -> int:
    """
    Return the positive square root of input integer via Binary Search
    """

    """
    Parameters
    ----------
    n : int
        Input integer
    """

    # searching space: min = 1, max = n
    l, r = 1, n

    while l < r:
        mid = (l + r) // 2

        # find the potential upper bound, assign to right
        if mid * mid >= n: r = mid
        else: l = mid + 1

    return l

def is_prime(n) -> bool:
    """
    Check whether the input integer is prime number
    """

    """
    Parameters
    ----------
    n : int
        Input integer
    """

    # time complexity: log(n)
    upper_bound = sqrt(n)

    if upper_bound == n: return True
    
    # loop from 2 to sqrt(n)
    for i in range(2, upper_bound+1):
        if n % i == 0: return False

    return True

def main():
    # user input
    n = int(input('Enter a positive integer: '))

    # find the prime list
    ans = []
    for i in range(2, n+1): 
        if is_prime(i): ans.append(str(i))

    # output the answer
    print('The primes up to {0} are: {1}'.format(n, ', '.join(ans)))

if __name__ == '__main__':
    main()