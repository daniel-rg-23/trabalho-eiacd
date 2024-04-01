import pygame
from seti.sets import *
from opening_page import *
from level1 import *
from menu_page import *


# Initialize pygame
pygame.init()


# Create a screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match the Tiles")  # Set your game title here

game = Game()
opening_page = OpeningPage(WIDTH, HEIGHT)
menu_page = MenuPage(WIDTH, HEIGHT)


running = True


while running:
    opening_page.draw(screen)
    if opening_page.handle_events():
        menu_running = True
        while menu_running:
            menu_page.draw(screen)
            if menu_page.handle_events():
                game.new()
                game.run()
            pygame.display.flip()  # Update the display after handling events
    pygame.display.flip()

# Quit pygame
pygame.quit()

