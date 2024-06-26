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
from .lib import mouse_pos_to_grid, solve

import pygame
from pygame import display
from typing import Tuple

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
        self.menu_state = None
        self.cursor_pos = None
        self.error_flag = None

        # MENU BUTTONS

        # menu main
        self.menu_resume = None
        self.menu_controls = None
        self.menu_quit = None

        # control menu
        self.controls_back = None

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
        self.menu_state = 'main'
        self.cursor_pos = (4, 4)
        self.error_flag = False

        # create menu button instances
        self.menu_resume = Button(WINDOW_WIDTH // 2, OFFSET, "RESUME",
                                  self.tooltips_font, BLACK, 1, 25)
        self.menu_controls = Button(WINDOW_WIDTH // 2, OFFSET * 2, "CONTROLS",
                                    self.tooltips_font, BLACK, 1, 25)
        self.menu_quit = Button(WINDOW_WIDTH // 2, OFFSET * 3, "QUIT",
                                self.tooltips_font, BLACK, 1, 25)
        
        self.controls_back = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT - (OFFSET * 4), "Back",
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

        # error text if error flag is triggered
        if self.error_flag:
            self.__draw_text("WRONG!!!", RED, OFFSET, WINDOW_HEIGHT - OFFSET)

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
                elif self.grid.board[row][col].get_locked():
                    color = DARKER_GRAY
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
                             ((i+1) * CELL_SIZE + OFFSET, OFFSET),
                             ((i+1) * CELL_SIZE + OFFSET, WINDOW_HEIGHT - OFFSET),
                             line)
            pygame.draw.line(self.window, BLACK,
                             (OFFSET, (i+1) * CELL_SIZE + OFFSET),
                             (WINDOW_WIDTH - OFFSET, (i+1) * CELL_SIZE + OFFSET),
                             line)
            
        # GRID VALUES

        for row in range(9):
            for col in range(9):
                if self.grid.board[row][col].get_val() != 0:
                    color = AQUA if self.grid.board[row][col].get_locked() else BLUE
                    text = self.game_font.render(
                        str(self.grid.board[row][col].get_val()),
                        True,
                        color
                    )
                    rect = text.get_rect(
                        center=((col * CELL_SIZE) + OFFSET + (CELL_SIZE // 2),
                                (row * CELL_SIZE) + OFFSET + (CELL_SIZE // 2))
                    )
                    self.window.blit(text, rect)

        # CURSOR POSITION
        x, y = self.cursor_pos

        pygame.draw.line(self.window, GREEN,
                         ((x) * CELL_SIZE + OFFSET, (y) * CELL_SIZE + OFFSET),
                         ((x) * CELL_SIZE + OFFSET, (y + 1) * CELL_SIZE + OFFSET),
                         THICK_GRID_LINE)
        pygame.draw.line(self.window, GREEN,
                         ((x + 1) * CELL_SIZE + OFFSET, (y) * CELL_SIZE + OFFSET),
                         ((x + 1) * CELL_SIZE + OFFSET, (y + 1) * CELL_SIZE + OFFSET),
                         THICK_GRID_LINE)
        pygame.draw.line(self.window, GREEN,
                         ((x) * CELL_SIZE + OFFSET, (y) * CELL_SIZE + OFFSET),
                         ((x + 1) * CELL_SIZE + OFFSET, (y) * CELL_SIZE + OFFSET),
                         THICK_GRID_LINE)
        pygame.draw.line(self.window, GREEN,
                         ((x) * CELL_SIZE + OFFSET, (y + 1) * CELL_SIZE + OFFSET),
                         ((x + 1) * CELL_SIZE + OFFSET, (y + 1) * CELL_SIZE + OFFSET),
                         THICK_GRID_LINE)

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
                if self.menu_state == 'main':
                    if self.menu_resume.draw(self.window, WHITE, BLACK):
                        self.paused = False
                    if self.menu_controls.draw(self.window, WHITE, BLACK):
                        self.menu_state = 'controls'
                    if self.menu_quit.draw(self.window, WHITE, BLACK):
                        run = False
                else:
                    # draw controls text
                    self.__draw_text("Q - Quit", BLACK, GRID_SQAURE_SIZE // 2 - OFFSET, OFFSET)
                    self.__draw_text("N - New Board", BLACK, GRID_SQAURE_SIZE // 2 - OFFSET, OFFSET * 2)
                    self.__draw_text("R - Reset", BLACK, GRID_SQAURE_SIZE // 2 - OFFSET, OFFSET * 3)
                    self.__draw_text("B - Blank Board", BLACK, GRID_SQAURE_SIZE // 2 - OFFSET, OFFSET * 4)

                    if self.controls_back.draw(self.window, WHITE, BLACK):
                        self.menu_state = 'main'
                display.flip()
            
            for event in pygame.event.get():
                # handle keypresses
                if event.type == pygame.KEYDOWN:
                    self.error_flag = False
                    if not self.paused:
                        x, y = self.cursor_pos

                        # handle arrow key movement
                        if event.key == pygame.K_UP and y > 0:
                            self.cursor_pos = (x, y-1)
                            continue
                        if event.key == pygame.K_DOWN and y < 8:
                            self.cursor_pos = (x, y+1)
                            continue
                        if event.key == pygame.K_LEFT and x > 0:
                            self.cursor_pos = (x-1, y)
                            continue
                        if event.key == pygame.K_RIGHT and x < 8:
                            self.cursor_pos = (x+1, y)
                            continue

                        # handle numeric input
                        elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            self.grid.board[y][x].set_val(1)
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            self.grid.board[y][x].set_val(2)
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            self.grid.board[y][x].set_val(3)
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            self.grid.board[y][x].set_val(4)
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            self.grid.board[y][x].set_val(5)
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            self.grid.board[y][x].set_val(6)
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            self.grid.board[y][x].set_val(7)
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                            self.grid.board[y][x].set_val(8)
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                            self.grid.board[y][x].set_val(9)

                        if self.grid.board[y][x].get_val() != self.grid.solved_board[y][x].get_val():
                            self.error_flag = True
                            self.grid.board[y][x].set_val(0)
                        
                    # quit game is 'esc' or 'q' is pressed
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        run = False

                    # check for menu option
                    elif event.key == pygame.K_SPACE:
                        if not self.paused:
                            self.paused = True
                        else:
                            self.paused = False

                # handle if user clicks on the grid
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = mouse_pos_to_grid(
                        pygame.mouse.get_pos(),
                        GRID_SQAURE_SIZE,
                        OFFSET,
                        CELL_SIZE
                    )
                    if click_pos:
                        self.cursor_pos = click_pos
                
                # handle if user clicks the topright 'X'
                elif event.type == pygame.QUIT:
                    run = False
            
            # check for win
            if self.grid.is_win():
                print("You Win!")
        
        pygame.quit()

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
