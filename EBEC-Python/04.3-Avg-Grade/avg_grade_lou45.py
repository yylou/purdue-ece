"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 04.3 - Avg Grade
Date: 09/27/2021

Description:
    Return a letter grade after five input scores are entered

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

def get_valid_score() -> int:
    """
    Get the valid score from user input
    """

    while True:
        score = float(input('Enter a score: '))

        # out of valid range, skip appending to re-enter
        if score < 0 or score > 100: 
            print('  Invalid Input. Please try again.')
            continue
        else:
            return score

def determine_grade(score) -> str:
    """
    Return the letter grade by mapping table
    """

    """
    Parameters
    ----------
    score : int
        Numeric Score
    """

    letter_grade_table = {
        91: 'A',
        82: 'B',
        73: 'C',
        64: 'D',
        0:  'F'
    }

    for _ in sorted(letter_grade_table, reverse=True):
        if score >= _: return letter_grade_table[_]

def calc_average(scores) -> float:
    """
    Return the average grade
    """

    """
    Parameters
    ----------
    scores : list
        List of scores with length 5
    """

    return sum(scores) / float(len(scores))

def main():
    # user input for five valid scores
    scores = []

    while len(scores) != 5:
        # get the valid score from user input
        score = get_valid_score()

        # map the numeric grade to letter grade
        grade = determine_grade(score)
        
        # output for each valid input
        print('  The letter grade for {0:.1f} is {1}.'.format(score, grade))

        scores.append(score)

    # calculate the average score
    avg = calc_average(scores)

    # output for the average score and corresponding letter grade
    print('\nResults:')
    print('  The average score is {0:.2f}.'.format(avg))
    print('  The letter grade for {0:.2f} is {1}.'.format(avg, determine_grade(avg)))

if __name__ == '__main__':
    main()