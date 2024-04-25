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
from .button import Button
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
        # window and backend game grid representation
        self.window = None
        self.grid = None

        # fonts
        self.game_font = None
        self.tooltips_font = None

        # game variables
        self.paused = None

        # menu buttons
        self.menu_resume = None
        self.menu_controls = None
        self.menu_quit = None

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
        self.tooltips_font = pygame.font.SysFont("timesnewroman", OFFSET // 2)

        # initialize window
        self.window = display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        display.set_caption("Sudoku")

        # initialize game variables
        self.paused = False

        # create menu button instances
        self.menu_resume = Button(WINDOW_WIDTH // 2, OFFSET, "RESUME",
                                  self.tooltips_font, BLACK, 1, 25)
        self.menu_controls = Button(WINDOW_WIDTH // 2, OFFSET * 2, "CONTROLS",
                                    self.tooltips_font, BLACK, 1, 25)
        self.menu_quit = Button(WINDOW_WIDTH // 2, OFFSET * 3, "QUIT",
                                self.tooltips_font, BLACK, 1, 25)

    def __draw_game(self) -> None:
        '''
        Handles drawing all of the game elements in a single function.

        Parameters: None

        Returns: None
        '''
        # clear window screen
        self.window.fill(WHITE)

        # draw game grid and cell values
        self.__draw_grid()

        # draw menu tooltip
        self.__draw_text("Press SPACE to open menu", BLACK, OFFSET, OFFSET // 6)

        # apply window changes
        display.flip()

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

    def __draw_text(self, text: str, color: Tuple[int, int, int],
                    x: int, y: int) -> None:
        '''
        Handles drawing the game menu

        Parameters:
            - text: a string containing the text to be drawn
            - color: the color the text should be drawn as
            - x: the x-position of where the text should be rendered
            - y: the y-position of where the text should be rendered

        Returns: None
        '''
        img = self.tooltips_font.render(text, True, color)
        self.window.blit(img, (x, y))
    
    def run(self) -> None:
        '''
        Main game loop function.

        Parameters: None

        Returns: None
        '''
        # run game
        run = True
        while run:
            # draw game if unpaused
            if not self.paused:
                self.__draw_game()
            # otherwise handle paused events
            else:
                self.window.fill(FAINT_GRAY)
                if self.menu_resume.draw(self.window, WHITE, BLACK):
                    self.paused = False
                if self.menu_controls.draw(self.window, WHITE, BLACK):
                    pass
                if self.menu_quit.draw(self.window, WHITE, BLACK):
                    run = False
                display.flip()
            
            for event in pygame.event.get():
                # handle keypresses
                if event.type == pygame.KEYDOWN:
                    # quit game is 'esc' or 'q' is pressed
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        run = False

                    # check for menu option
                    elif event.key == pygame.K_SPACE:
                        if not self.paused:
                            self.paused = True
                        else:
                            self.paused = False

                # handle if user clicks the topright 'X'
                elif event.type == pygame.QUIT:
                    run = False
        
        pygame.quit()

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
