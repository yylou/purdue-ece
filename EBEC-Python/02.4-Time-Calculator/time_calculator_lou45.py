"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 02.4 - Time Calculator
Date: 09/15/2021

Description:
    A program that asks the user to enter a number of seconds and then 
    displays the total time entered in days, hours, minutes and second.

    Only non-zero units should be displayed and 
    all units should be separated by proper punctuation.

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


def time_calculator(n) -> str:
    """
    Calculate the total time in days, hours, minutes and second format.
    """

    """
    Parameters
    ----------
    n : int
        Number of seconds
    """

    DAY  = 86400
    HOUR = 3600
    MIN  = 60

    # time calculation for days, hours, mins and seconds
    days = n // DAY
    n %= DAY
    hours = n // HOUR
    n %= HOUR
    mins = n // MIN
    n %= MIN

    fields = []

    if days:  fields.append('{0} day(s)'.format(days))
    if hours: fields.append('{0} hour(s)'.format(hours))
    if mins:  fields.append('{0} minute(s)'.format(mins))
    if n: fields.append('{0} second(s)'.format(n))

    # return if there is only one field
    if len(fields) == 1: return fields[0]

    # concate each field by ',' and 'and'
    return ', '.join(fields[:-1]) + ' and ' + fields[-1]

def main():
    # user input for specific year
    n = int(input('Please enter a time in seconds: '))
    if n < 60: print('  {0} seconds is less than one minute.'.format(n)); return

    # check for pocket number
    time = time_calculator(n)

    # output final answer
    print('  {0:,} seconds is: {1}.'.format(n, time))

if __name__ == '__main__':
    main()