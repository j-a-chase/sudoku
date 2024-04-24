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
import pygame
from pygame import display
from .colors import *

# constants

# window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

# game size and positioning
GRID_SQAURE_SIZE = 864
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
        self.window = None
        self.__setup()
        
    def __setup(self) -> None:
        '''
        Runs basic setup commands for the pygame application on startup.

        Parameters: None

        Returns: None
        '''
        # initialize pygame resources
        pygame.init()

        # initialize window
        self.window = display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.window.fill(WHITE)

        # draw game grid
        self.draw_grid()

        # set window caption
        display.set_caption("Sudoku")

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
            print((i+1) * (GRID_SQAURE_SIZE // 9) + OFFSET)
            line = THICK_GRID_LINE if (i+1) % 3 == 0 else THIN_GRID_LINE
            pygame.draw.line(self.window, BLACK,
                             ((i+1) * (GRID_SQAURE_SIZE // 9) + OFFSET, OFFSET),
                             ((i+1) * (GRID_SQAURE_SIZE // 9) + OFFSET, WINDOW_HEIGHT - OFFSET),
                             line)
            pygame.draw.line(self.window, BLACK,
                             (OFFSET, (i+1) * (GRID_SQAURE_SIZE // 9) + OFFSET),
                             (WINDOW_WIDTH - OFFSET, (i+1) * (GRID_SQAURE_SIZE // 9) + OFFSET),
                             line)

        # apply window changes
        display.flip()

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
