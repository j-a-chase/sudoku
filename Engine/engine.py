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
from .colors import *

import pygame
from pygame import display
from typing import Tuple, List

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

# labels dictionary indices
FUNCTION_INDEX = 0
RECTANGLE_INDEX = 1

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
        self.menu_font = None
        
        self.menu = None
        self.labels = None

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
        self.menu_font = pygame.font.SysFont("timesnewroman", OFFSET // 2)

        # setup menu options
        self.labels = {
            'File': [self.__open_file_menu]
        }

        # initialize window
        self.window = display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.window.fill(WHITE)

        # set window caption
        display.set_caption("Sudoku")

    def __draw_game(self) -> pygame.Rect:
        '''
        Handles drawing all of the game elements in a single function.

        Parameters: None

        Returns:
            - the menu Rect object from the draw_menu function
        '''
        # draw functions
        self.__draw_grid()
        menu = self.__draw_menu()

        # apply window changes
        display.flip()

        return menu

    def __draw_grid(self) -> None:
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

    def __draw_menu(self) -> pygame.Rect:
        '''
        Handles drawing the game menu

        Parameters: None

        Returns:
            - the menu Rect object
        '''
        # create menu dimensions and draw the menu
        menu_bar = pygame.Rect(0, 0, WINDOW_WIDTH, OFFSET)
        pygame.draw.rect(self.window, RED, menu_bar)

        # position menu labels
        label_name = 'File'
        label = self.menu_font.render(label_name, True, BLACK)
        label_rect = label.get_rect(topleft=(OFFSET // 3, OFFSET // 6))
        self.labels[label_name].append(label_rect)
        self.window.blit(label, label_rect)

        return menu_bar
    
    def __open_file_menu(self) -> None:
        '''
        Opens the file menu drop down

        Parameters: None

        Returns: None
        '''
        print("File menu clicked!")
    
    def run(self) -> None:
        '''
        Main game loop function.

        Parameters: None

        Returns: None
        '''
        # draw game, store rectangles for collision detection
        self.menu = self.__draw_game()

        # run game
        run = True
        while run:
            for event in pygame.event.get():
                # grab current mouse position for mousebuttondown events
                mouse = pygame.mouse.get_pos()

                # handle keypresses
                if event.type == pygame.KEYDOWN:
                    # quit game is 'esc' or 'q' is pressed
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        run = False

                # handle if user clicks the topright 'X'
                elif event.type == pygame.QUIT:
                    run = False
                
                # handle mousebuttondown events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if click was in the menu
                    if self.menu.collidepoint(mouse):
                        # iterate through label collisions to determine if and
                        # what label was hit
                        for label in self.labels:
                            if self.labels[label][RECTANGLE_INDEX].collidepoint(mouse):
                                self.labels[label][FUNCTION_INDEX]()
        pygame.quit()

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
