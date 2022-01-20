"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 07.4 - Magic Square
Date: 10/25/2021

Description:
    Check pre-defined two-dimensional square is Lo Shu magic square or not

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

def print_square(l):
    """
    Print the input two-dimensional list
    """

    """
    Parameters
    ----------
    l : list
        Two-dimensional list
    """
    
    for element in l:
        print(f'  {" ".join([str(_) for _ in element])}')

def is_magic(l):
    """
    Check the input two-dimensional list is Lo Shu magic square or not
    """

    """
    Parameters
    ----------
    l : list
        Two-dimensional list
    """
    d = 3
    existence = set()

    for i in range(d):
        # Check Row's Sum
        if sum(l[i]) != 15: return False

        col = 0
        for j in range(3):
            col += l[j][i]

            # Check Element: From 1 to 9 with exact one existence (no duplicate)
            if not (1 <= l[i][j] <= 9): return False
            if l[i][j] not in existence: existence.add(l[i][j])
            else: return False
        
        # Check Col's Sum
        if col != 15: return False

    # Check Diagonal's Sum
    if sum([l[i][i]     for i in range(d)]) != 15: return False
    if sum([l[i][d-i-1] for i in range(d)]) != 15: return False

    return True

def main():
    # Pre-defined 3 two-dimensional squre
    squares = {0: [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1: [[5, 5, 5], [5, 5, 5], [5, 5, 5]], 2: [[4, 9, 2], [3, 5, 7], [8, 1, 6]]}

    # Iterate through each square to print and check whether it is Lo Shu magic square
    for _ in range(3):
        # Print the pre-defined two-dimensional square
        print('Your square is:')
        print_square(squares[_])
        
        # Check current square is Lo Shu magic square or not
        FLAG = is_magic(squares[_])
        if FLAG: print('It is a Lo Shu magic square!', end='')
        else: print('It is not a Lo Shu magic square.', end ='')

        # End of program
        if _ != 2: print('\n')
        else: print('\n')

if __name__ == '__main__':
    main()