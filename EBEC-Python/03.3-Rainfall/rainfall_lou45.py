"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 03.3 - Rainfall
Date: 09/15/2021

Description:
    Use nested loops to collect data and calculate the average rainfall overa period of years.

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


def main():
    numbers = []

    # user input for number of years
    n = int(input('Enter the number of years: '))
    if n < 1: print('Invalid input.'); return

    month_table = {
        0: 'Jan.',
        1: 'Feb.',
        2: 'Mar.',
        3: 'Apr.',
        4: 'May.',
        5: 'Jun.',
        6: 'Jul.',
        7: 'Aug.',
        8: 'Sep.',
        9: 'Oct.',
       10: 'Nov.',
       11: 'Dec.',
    }

    record = []

    # outer loop for each year
    for i in range(n):
        print('  For year No. {0}'.format(i+1))

        # inner loop for each month
        for j in range(12):
            while True:
                rainfall = float(input('    Enter the rainfall for {0}: '.format(month_table[j])))
                
                if rainfall < 0: print('    Invalid input, please try again.'); continue
                else: record.append(rainfall); break

    # output total rainfall and monthly average rainfall
    print('There are {0} months.'.format(n * 12))
    print('The total rainfall is {0:.2f} inches.'.format(sum(record)))
    print('The monthly average rainfall is {0:.2f} inches.'.format(sum(record) / len(record)))

if __name__ == '__main__':
    main()