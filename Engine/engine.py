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

# engine class global constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
OFFSET = (WINDOW_WIDTH - 800) // 2
THICK_LINE = 5
THIN_LINE = 1

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

        # GAME BOX LINES

        # top line
        pygame.draw.line(self.window, BLACK,
                         (OFFSET, OFFSET),
                         (WINDOW_WIDTH - OFFSET, OFFSET), THICK_LINE)
        
        # bottom line
        pygame.draw.line(self.window, BLACK,
                         (OFFSET, WINDOW_HEIGHT - OFFSET),
                         (WINDOW_WIDTH - OFFSET, WINDOW_HEIGHT - OFFSET), THICK_LINE)
        
        # left line
        pygame.draw.line(self.window, BLACK,
                         (OFFSET, OFFSET),
                         (OFFSET, WINDOW_HEIGHT - OFFSET), THICK_LINE)
        
        # right line
        pygame.draw.line(self.window, BLACK,
                         (WINDOW_WIDTH - OFFSET, OFFSET),
                         (WINDOW_WIDTH - OFFSET, WINDOW_HEIGHT - OFFSET), THICK_LINE)

        # set window caption
        display.set_caption("Sudoku")

        # apply window changes
        display.flip()

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

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
