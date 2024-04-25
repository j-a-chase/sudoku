################################################################################
# Name: James A. Chase
# File: engine.py
# Date: 23 April 2024
# Description:
#
# Class file for game engine.
#
################################################################################

# imports
from .puzzle import Puzzle

import pygame
from pygame import display
from .colors import *

# constants

# window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

# game size and positioning
GRID_SQAURE_SIZE = 864
CELL_SIZE = GRID_SQAURE_SIZE // 9
OFFSET = (WINDOW_WIDTH - GRID_SQAURE_SIZE) // 2

# line sizes
BORDER_LINE = 5
THICK_GRID_LINE = 3
THIN_GRID_LINE = 1

class Engine:

    def __init__(self) -> None:
        '''
        Constructor

        Parameters: None

        Returns: None
        '''
        # initialize
        self.window = None
        self.grid = None
        self.game_font = None

        # run setup
        self.__setup()
        
    def __setup(self) -> None:
        '''
        Runs basic setup commands for the pygame application on startup.

        Parameters: None

        Returns: None
        '''
        # initialize pygame resources
        pygame.init()

        # initialize game board
        self.grid = Puzzle()
        self.grid.generate_puzzle()

        # setup fonts
        self.game_font = pygame.font.SysFont("timesnewroman", 40)

        # initialize window
        self.window = display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.window.fill(WHITE)

        # set window caption
        display.set_caption("Sudoku")

        # draw game grid
        self.draw_grid()

        # debug loop
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                elif event.type == pygame.QUIT:
                    run = False
        pygame.quit()

    def draw_grid(self) -> None:
        '''
        Draws the lines for the sudoku grid

        Parameters: None

        Returns: None
        '''
        # CELL BACKGROUNDS

        for row in range(9):
            for col in range(9):
                if self.grid.board[row][col].get_val() == 0:
                    color = LIGHT_GRAY
                else:
                    color = DARK_GRAY
                pygame.draw.rect(self.window, color, 
                                 ((col * CELL_SIZE) + OFFSET,
                                  (row * CELL_SIZE) + OFFSET,
                                  CELL_SIZE,
                                  CELL_SIZE))

        # GAME BOX LINES

        # top line
        pygame.draw.line(self.window, BLACK,
                         (OFFSET, OFFSET),
                         (WINDOW_WIDTH - OFFSET, OFFSET),
                         BORDER_LINE)
        
        # bottom line
        pygame.draw.line(self.window, BLACK,
                         (OFFSET, WINDOW_HEIGHT - OFFSET),
                         (WINDOW_WIDTH - OFFSET, WINDOW_HEIGHT - OFFSET),
                         BORDER_LINE)
        
        # left line
        pygame.draw.line(self.window, BLACK,
                         (OFFSET, OFFSET),
                         (OFFSET, WINDOW_HEIGHT - OFFSET),
                         BORDER_LINE)
        
        # right line
        pygame.draw.line(self.window, BLACK,
                         (WINDOW_WIDTH - OFFSET, OFFSET),
                         (WINDOW_WIDTH - OFFSET, WINDOW_HEIGHT - OFFSET),
                         BORDER_LINE)
        
        # INDIVIDUAL GRID LINES

        # grid lines
        for i in range(8):
            # we need a thick line every third line in the eight we're drawing
            line = THICK_GRID_LINE if (i+1) % 3 == 0 else THIN_GRID_LINE
            pygame.draw.line(self.window, BLACK,
                             ((i+1) * (CELL_SIZE) + OFFSET, OFFSET),
                             ((i+1) * (CELL_SIZE) + OFFSET, WINDOW_HEIGHT - OFFSET),
                             line)
            pygame.draw.line(self.window, BLACK,
                             (OFFSET, (i+1) * (CELL_SIZE) + OFFSET),
                             (WINDOW_WIDTH - OFFSET, (i+1) * (CELL_SIZE) + OFFSET),
                             line)
            
        # GRID VALUES
        
        for row in range(9):
            for col in range(9):
                if self.grid.board[row][col].get_val() != 0:
                    text = self.game_font.render(
                        str(self.grid.board[row][col].get_val()),
                        True,
                        BLUE
                    )
                    rect = text.get_rect(
                        center=((col * CELL_SIZE) + OFFSET + (CELL_SIZE // 2),
                                (row * CELL_SIZE) + OFFSET + (CELL_SIZE // 2))
                    )
                    self.window.blit(text, rect)

        # apply window changes
        display.flip()

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
