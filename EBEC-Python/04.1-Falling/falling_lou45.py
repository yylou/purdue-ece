"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 04.1 - Falling
Date: 09/27/2021

Description:
    Calculate the falling distance in meters by accepting 
    object's falling time (in seconds) as arguments.

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

def falling_dist(t) -> float:
    """
    Calculate the falling distance
    """

    """
    Parameters
    ----------
    t : int
        Falling time
    """
    
    return (8.87 * (t ** 2)) / 2.

def main():
    # output the table header
    print('Time (s)  Distance (m)')
    print('----------------------')

    # Loop for dif0ferent falling time from 5s to 50s
    for i in range(5, 55, 5):

        # output the answer
        print('{0:>8d}  {1:12.1f}'.format(i, falling_dist(i)))
        falling_dist(i)

if __name__ == '__main__':
    main()