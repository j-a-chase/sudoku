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
from colors import *

# engine class global constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

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
        self.window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.window.fill(WHITE)

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
