import pygame
from seti.sets import *

class MenuPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 45, bold=True)
        

        # Define buttons for menu options
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2 -200
        button_spacing = 20
        button_y = (screen_height - button_height - button_spacing * 2) // 2 - 400
        self.start_button = pygame.Rect(button_x, button_y, button_width, button_height)

    def draw(self, screen):

        screen.fill(LIGHTBLUE)
        pygame.draw.rect(screen, BLUE, self.start_button)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 1", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_text_pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button.collidepoint(mouse_pos):
                    return True  # Return True if the start button is clicked
        return False  
    

    

