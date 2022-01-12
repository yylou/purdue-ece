"""
Author: Yuan-Yao Lou, lou45@purdue.edu
Assignment: 06.2 - Rock Paper Scissors
Date: 10/16/2021

Description:
    Lets the user play a game of Rock, Paper, Scissors against the computer.
    - Computer's choice is randomly assigned
    - User's choice is defined by user input

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

CHOICE = {'rock': 0, 'paper': 1, 'scissors': 2}

def get_computer_choice() -> str:
    """
    Get computer's choice by random assignment mechanism
    """

    return random.choice(list(CHOICE.keys()))

def get_player_choice() -> str:
    """
    Get user's choice from user input
    """

    choice = None

    while choice not in CHOICE:
        choice = input('Choose rock, paper, or scissors: ')
        
        # invalid input choice
        if choice not in CHOICE:
            print('You made an invalid choice. Please try again.')

    return choice

def get_winner(computer: str, user: str) -> str:
    """
    Find out the winner by taking computer's and user's choice
    - return 'tie', 'player', 'computer' according to the choices
    """

    """
    Parameters
    ----------
    computer : str
        Computer's random choice
    user : str
        User's specified choice
    """

    _computer = CHOICE[computer]
    _user     = CHOICE[user]
    
    # case: scissors (computer) vs. rock (user)
    if   _computer == 2 and _user == 0: return 'player'

    # case: rock (computer) vs. scissors (user)
    elif _computer == 0 and _user == 2: return 'computer'

    else:
        if   _computer > _user: return 'computer'
        elif _computer < _user: return 'player'
        else: return 'tie'

def main():
    while True:
        # get computer's and user's random choice
        computer = get_computer_choice()
        user     = get_player_choice()

        # print two players' choices
        print(f'  The computer chose {computer}, and you chose {user}.')

        # find out the winner
        result = get_winner(computer, user)
        if result == 'tie':
            print('  Its a tie. Starting over.\n')

        elif result == 'player':
            print(f'  {user} beats {computer}')
            print( '  You won the game!')
            break

        else:
            print(f'  {computer} beats {user}')
            print( '  You lost.  Better luck next time.')
            break

    # end game message
    print('Thanks for playing.')

if __name__ == '__main__':
    main()