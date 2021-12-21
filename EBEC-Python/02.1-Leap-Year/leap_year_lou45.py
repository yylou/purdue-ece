"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 02.1 - Leap Year
Date: 09/06/2021

Description:
    Check whether the input year is the leap year by following constraints:
        (1) If the year could be divisible by 100 and 400, it is leap year.
            Otherwise, it is not. (ex. 2000 is but 2100 is not)
        (2) If the year could not be divisible by 100, then it is a leap year
            if and only if it is divisible by 4. (ex. 2004 is but 2006 is not)

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

def check_leap_year(year) -> int:
    """
    Check whether the input year is the leap year by following constraints:
        (1) If the year could be divisible by 100 and 400, it is leap year.
            Otherwise, it is not. (ex. 2000 is but 2100 is not)
        (2) If the year could not be divisible by 100, then it is a leap year
            if and only if it is divisible by 4. (ex. 2004 is but 2006 is not)
    """

    """
    Parameters
    ----------
    year : int
        Specified the year for leap year check
    """

    # condition 1: could be divisble by 100
    if year % 100 == 0:
        if year % 400 == 0: return 29
        else: return 28

    # condition 2: cannot be divisble by 100
    else:
        if year % 4 == 0: return 29
        else: return 28

def main():
    # user input for specific year
    year = int(input('Please input a year: '))

    # output final answer
    print('In the year {0}, February has {1} days.'.format(year, check_leap_year(year)))

if __name__ == '__main__':
    main()
