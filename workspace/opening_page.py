import pygame
from seti.sets import *

class OpeningPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 80, bold=True)  # You can adjust the font and size
        self.title_text = self.font.render("Match the Tiles", True, BLUE)  # Render the title text
        self.start_normal = pygame.Rect(50, 600, 300, 150)  # Define the start button rectangle
        self.start_advanced = pygame.Rect(430, 600, 300, 150)  # Define the start button rectangle
    def draw(self, screen):
        screen.fill(LIGHTBLUE)  # Fill the screen with black
        # Draw the title text
        screen.blit(self.title_text, (self.screen_width // 2 - self.title_text.get_width() // 2, 200))
        # Draw the start button
        pygame.draw.rect(screen, BLUE, self.start_normal)  # Green rectangle as the start button
         # Draw the start button
        pygame.draw.rect(screen, BLUE, self.start_advanced)  # Green rectangle as the start button
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Check if left mouse button is clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_normal.collidepoint(mouse_pos):
                        return True  # Return True if the start button is clicked
        return False



