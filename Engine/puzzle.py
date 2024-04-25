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

from random import randint
from typing import List, Tuple

class Puzzle:
    def __init__(self) -> None:
        '''
        Constructor

        Parameters: None

        Returns: None
        '''
        # initialize our sudoku board
        self.board = None

    def generate_puzzle(self, difficulty: int=65) -> None:
        '''
        Function to generate a sudoku puzzle.

        Parameters:
            - difficulty: an integer indicating how many blank cells to start
                            with, which typically indicates how difficult the
                            puzzle will be

        Returns: None
        '''
        def is_valid(board: List[List[Cell]], row: int, col: int,
                     val: int) -> bool:
            '''
            Helper function to determine if number is valid.

            Parameters:
                - board: a list of list of cells representing a sudoku grid
                - row: an integer representing the row where the move is taking
                        place
                - col: an integer representing the column where the move is
                        taking place
                - val: the value to be tested

            Returns:
                - a boolean if the attempted value is valid or not
            '''
            # check row and column
            for i in range(9):
                if (board[row][i].get_val() == val
                    or board[i][col].get_val() == val): return False
            
            # check subgrid
            subrow, subcol = (row // 3) * 3, (col // 3) * 3
            for i in range(subrow, subrow + 3):
                for j in range(subcol, subcol + 3):
                    if board[i][j].get_val() == val: return False

            return True
        
        def find_empty(board: List[List[Cell]]) -> Tuple[int, int]:
            '''
            Helper function to find the next empty cell.

            Parameters:
                - board: a list of list of cells representing a sudoku grid

            Returns:
                - a tuple containing the coordinates for the next empty cell
            '''
            # iterate by columns, then rows
            for i in range(9):
                for j in range(9):
                    if board[i][j].get_val() == 0: return i, j
            
            return None, None
        
        def solve(board: List[List[Cell]]) -> bool:
            '''
            Helper function to very basically solve a given sudoku grid.

            Parameters:
                - board: a list of list of cells representing a sudoku grid

            Returns:
                - a boolean indicating if the grid has been solved
            '''
            # solve grid using a stack
            stack = []

            # push first Cell onto the stack
            stack.append(find_empty(board))

            while stack:
                # get next empty cell
                row, col = stack[-1]

                # check if grid is solved (no empty cells)
                if row is None: return True

                # start with num = 1
                num = board[row][col].get_val() + 1

                # find a valid value and keep going through the stack
                valid = False
                while num < 10:
                    if is_valid(board, row, col, num):
                        board[row][col].set_val(num)
                        stack.append(find_empty(board))
                        valid = True
                        break
                    num += 1
                if not valid:
                    board[row][col].set_val(0)
                    stack.pop()
            return False

        # generate a new blank board
        new_board = [[Cell() for _ in range(9)] for _ in range(9)]

        # populate the diagonal with random numbers
        for i in range(9):
            num = randint(1, 9)
            while not is_valid(new_board, i, i, num):
                num = randint(1, 9)
            new_board[i][i].set_val(num)

        solve(new_board)

        for i in range(difficulty):
            row, col = randint(0, 8), randint(0, 8)
            while new_board[row][col].get_val() == 0:
                row, col = randint(0, 8), randint(0, 8)
            new_board[row][col].set_val(0)

        self.board = new_board

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
