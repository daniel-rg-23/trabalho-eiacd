import pygame
from seti.sets import *
from opening_page import *
from level1 import Game
from level2 import Game2
from level3 import Game3
from level4 import Game4
from level5 import Game5
from menu_page import *
from algorithm import *

# Initialize pygame
pygame.init()


# Create a screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match the Tiles")  # Set your game title here

game = Game()
game2 = Game2()
game3 = Game3()
game4 = Game4()
game5 = Game5()
opening_page = OpeningPage(WIDTH, HEIGHT)
menu_page = MenuPage(WIDTH, HEIGHT)
algorithm_page= AlgorithmPage(WIDTH,HEIGHT)

running = True

while running:
    opening_page.draw(screen)
    event = opening_page.handle_events()  # Store the return value
    if event == "choose":
        algorithm_running = True
        while algorithm_running:
            algorithm_page.draw(screen)
            algorithm_event = algorithm_page.handle_events()
            if algorithm_event == "goback":
                algorithm_running = False
            pygame.display.flip()  # Update the display after handling events
    elif event == True:
        menu_running = True
        while menu_running:
            menu_page.draw(screen)
            menu_event = menu_page.handle_events()  # Store the return value
            if menu_event == 1:  # Check the stored value
                game.new()
                game.run()
            elif menu_event == 2: #go to the second level
                game2.new()
                game2.run()
            elif menu_event == 3: #go to the third level
                game3.new()
                game3.run()
            elif menu_event == 4: #go to the fourth level
                game4.new()
                game4.run()
            elif menu_event == 5: #go to the fifth level
                game5.new()
                game5.run()
               
            elif menu_event == "goback":  # Check the stored value
                menu_running = False
            pygame.display.flip()  # Update the display after handling events
    pygame.display.flip()

# Quit pygame
pygame.quit()


