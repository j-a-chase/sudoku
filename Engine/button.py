################################################################################
# Name: James A. Chase
# File: button.py
# Date: 23 April 2024
# Description:
#
# Class file for Button class to create buttons in a pygame application.
#
################################################################################

# imports
import pygame
from typing import Tuple

class Button:
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font,
                 color: Tuple[int, int, int], scale: float=1.0,
                 padding: int=0) -> None:
        '''
        Constructor

        Parameters:
            - x: an integer indicating the x-position where the button should be
                    rendered
            - y: an integer indicating the y-position where the button should be
                    rendered
            - text: a string indicating the text to be rendered on the button
            - font: a pygame.Font object that indicates what font to render the
                    button text in
            - color: a tuple containing integer RGB values for a color
            - scale: a float indicating a scale for the button, default 1.0
            - padding: an integer indicating the number of pixels to pad the
                       button in each direction

        Returns: None
        '''
        # render provided text as an image
        image = font.render(text, True, color)

        # scale the image appropriately
        self.img = pygame.transform.scale(image,
                                          (int(image.get_width() * scale),
                                           int(image.get_height() * scale)))
        
        # render image in a rectangle in a given position
        self.rect = self.img.get_rect(topleft=(x, y))

        # hold clicked state for the button
        self.clicked = False

        # holds the designated amount of padding to add to the button background
        # and border
        self.padding = padding

    def draw(self, screen: pygame.Surface, bg_color: Tuple[int, int, int],
             border_color: Tuple[int, int, int]) -> bool:
        '''
        Draws the button on the screen

        Parameters:
            - screen: a pygame.Surface object to draw the button on
            - bg_color: a tuple containing integer RGB values for a color for the
                        background of the button
            - border_color: a tuple containing integer RGB values for a color
                            for the border of the button

        Returns:
            - a boolean value indicating the button was pressed
        '''
        # indicates if the button was pressed
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicks
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # inflate a new rectangle for the background and border of the button
        bg_rect = self.rect.inflate(self.padding, self.padding)

        # button background
        pygame.draw.rect(screen, bg_color, bg_rect)

        # button border
        pygame.draw.rect(screen, border_color, bg_rect, width=5)

        # button text
        screen.blit(self.img, (self.rect.x, self.rect.y))

        return action

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
