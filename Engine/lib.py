################################################################################
# Name: James A. Chase
# File: lib.py
# Date: 23 April 2024
# Description:
#
# A collection of helpful functions for the project that can be separately
# tested.
#
################################################################################

# imports
from .cell import Cell
from typing import List

def is_valid(board: List[List[Cell]], row: int, col: int, val: int) -> bool:
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

if __name__ == '__main__':
    assert False, 'This is a module. Import its contents into another file.'
