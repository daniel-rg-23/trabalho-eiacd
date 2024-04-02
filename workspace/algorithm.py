import pygame
from seti.sets import *

class MenuPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 45, bold=True)
        
        # Define buttons for menu options
        self.goback = pygame.Rect(580, 70, 160, 100)
        self.puzzle1 = pygame.Rect((screen_width - 400) // 2-100, (screen_height +300) // 2 - 400, 400, 200)
        self.puzzle2 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 950) // 2 - 400, 400, 200)
        
        
    def draw(self, screen):
        screen.fill(LIGHTBLUE)
        
        pygame.draw.rect(screen, BLUE, self.goback)

        pygame.draw.rect(screen, ORANGE, self.puzzle1)
        # Draw text on buttons
        start_text = self.font.render("greedy", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle1.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle2)
        # Draw text on buttons
        start_text = self.font.render("A*", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle2.center)
        screen.blit(start_text, start_text_pos)


# Create a pygame window and initialize it
pygame.init()
screen_width = WIDTH
screen_height = HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu Page")

# Create an instance of the MenuPage class
menu_page = MenuPage(screen_width, screen_height)

# Call the draw method to draw the menu page
menu_page.draw(screen)

# Update the display
pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()
