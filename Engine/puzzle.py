################################################################################
# Name: James A. Chase
# File: puzzle.py
# Date: 23 April 2024
# Description:
#
# Class file for Puzzle class.
#
################################################################################

# imports
from .cell import Cell
from .lib import is_valid, solve

from random import randint
from copy import deepcopy

class Puzzle:
    def __init__(self) -> None:
        '''
        Constructor

        Parameters: None

        Returns: None
        '''
        # initialize our sudoku board
        self.board = None
        self.solved_board = None

    def generate_puzzle(self, difficulty: int=65) -> None:
        '''
        Function to generate a sudoku puzzle.

        Parameters:
            - difficulty: an integer indicating how many blank cells to start
                            with, which typically indicates how difficult the
                            puzzle will be

        Returns: None
        '''
        # generate a new blank board
        new_board = [[Cell() for _ in range(9)] for _ in range(9)]

        # populate the diagonal with random numbers
        for i in range(9):
            num = randint(1, 9)
            while not is_valid(new_board, i, i, num):
                num = randint(1, 9)
            new_board[i][i].set_val(num)

        # solve board
        solve(new_board)

        self.solved_board = deepcopy(new_board)

        # remove squares to create puzzle (more usually means more difficult)
        for i in range(difficulty):
            row, col = randint(0, 8), randint(0, 8)
            while new_board[row][col].get_val() == 0:
                row, col = randint(0, 8), randint(0, 8)
            new_board[row][col].set_val(0)

        # lock cells with a starting value
        for row in range(9):
            for col in range(9):
                if new_board[row][col].get_val() != 0:
                    new_board[row][col].set_locked(True)

        self.board = new_board

    def is_win(self) -> bool:
        '''
        Function to check for a win between boards

        Parameters: None

        Returns:
            - a boolean indicating if a win has been achieved
        '''
        for row in range(9):
            for col in range(9):
                if self.board[row][col].get_val() != self.solved_board[row][col].get_val():
                    return False
        return True

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
