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
from typing import List, Tuple

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

def mouse_pos_to_grid(pos: Tuple[int, int], grid_size: int,
                      grid_offset: int, cell_size: int) -> Tuple[int, int]:
    '''
    Converts the integer value of the mouse position to grid indices.

    Parameters:
        - pos: a tuple of integers containing the x and y coordinates of the
               mouse position
        - grid_size: an integer representing the size of the sudoku grid
        - grid_offset: an integer representing the offset of the sudoku grid
                       position from 0, 0 in the game window
        - cell_size: an integer representing the size of the individual cells

    Returns:
        - a tuple of two integers representing the row and column indices the
          cursor should be placed in.
    '''
    assert type(pos) == tuple, 'Parameter "pos" must be a tuple!'
    assert type(grid_size) == int
    assert type(grid_offset) == int

    x, y = pos

    assert type(x) == int, 'Parameter "pos" must contain two integers!'
    assert type(y) == int, 'Parameter "pos" must contain two integers!'
    
    grid_pos_x = None
    grid_pos_y = None

    if (
        x < grid_offset
        or y < grid_offset
        or x > grid_size + grid_offset
        or y > grid_size + grid_offset
    ): return None

    if grid_offset <= x < grid_offset + cell_size:
        grid_pos_x = 0
    elif grid_offset + cell_size <= x < grid_offset + cell_size * 2:
        grid_pos_x = 1
    elif grid_offset + cell_size * 2 <= x < grid_offset + cell_size * 3:
        grid_pos_x = 2
    elif grid_offset + cell_size * 3 <= x < grid_offset + cell_size * 4:
        grid_pos_x = 3
    elif grid_offset + cell_size * 4 <= x < grid_offset + cell_size * 5:
        grid_pos_x = 4
    elif grid_offset + cell_size * 5 <= x < grid_offset + cell_size * 6:
        grid_pos_x = 5
    elif grid_offset + cell_size * 6 <= x < grid_offset + cell_size * 7:
        grid_pos_x = 6
    elif grid_offset + cell_size * 7 <= x < grid_offset + cell_size * 8:
        grid_pos_x = 7
    elif grid_offset + cell_size * 8 <= x < grid_offset + cell_size * 9:
        grid_pos_x = 8

    if grid_offset <= y < grid_offset + cell_size:
        grid_pos_y = 0
    elif grid_offset + cell_size <= y < grid_offset + cell_size * 2:
        grid_pos_y = 1
    elif grid_offset + cell_size * 2 <= y < grid_offset + cell_size * 3:
        grid_pos_y = 2
    elif grid_offset + cell_size * 3 <= y < grid_offset + cell_size * 4:
        grid_pos_y = 3
    elif grid_offset + cell_size * 4 <= y < grid_offset + cell_size * 5:
        grid_pos_y = 4
    elif grid_offset + cell_size * 5 <= y < grid_offset + cell_size * 6:
        grid_pos_y = 5
    elif grid_offset + cell_size * 6 <= y < grid_offset + cell_size * 7:
        grid_pos_y = 6
    elif grid_offset + cell_size * 7 <= y < grid_offset + cell_size * 8:
        grid_pos_y = 7
    elif grid_offset + cell_size * 8 <= y < grid_offset + cell_size * 9:
        grid_pos_y = 8

    if grid_pos_x is None or grid_pos_y is None:
        return None
    return grid_pos_x, grid_pos_y

if __name__ == '__main__':
    assert False, 'This is a module. Import its contents into another file.'
