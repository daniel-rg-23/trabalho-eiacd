import pygame
from seti.sets import *
from opening_page import *
from level1 import Game
from menu_page import *
from algorithm import *

# Initialize pygame
pygame.init()


# Create a screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match the Tiles")  # Set your game title here

opening_page = OpeningPage(WIDTH, HEIGHT)
menu_page = MenuPage(WIDTH, HEIGHT)
algorithm_page= AlgorithmPage(WIDTH,HEIGHT)

chosen = [True, False, False, False, False, False, False]

running = True

while running:
    opening_page.draw(screen)
    event = opening_page.handle_events()  # Store the return value
    if event == "choose":
        algorithm_running = True
        while algorithm_running:
            algorithm_page.draw(screen)
            algorithm_event = algorithm_page.handle_events()
            chosen = algorithm_page.get_selected_algorithms()
            if algorithm_event == "goback":
                algorithm_running = False
            pygame.display.flip()  # Update the display after handling events
    elif event == True:
        menu_running = True
        while menu_running:
            menu_page.draw(screen)
            menu_event = menu_page.handle_events()  # Store the return value
            if menu_event == True:  # Check the stored value
                game = Game([(0, 0), (1, 0), (1, 1),(1,2),(3,0),(3,2)],[(3,1),(2,2)],[(3,3),(0,2)],4,2,GREEN,SOFTGREEN)
                game.new()
                game.run(chosen)
            elif menu_event == "goback":  # Check the stored value
                menu_running = False
            pygame.display.flip()  # Update the display after handling events
    pygame.display.flip()

# Quit pygame
pygame.quit()