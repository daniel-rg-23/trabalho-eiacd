import pygame
from seti.sets import *

class OpeningPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont("Calibri", 108, bold=True)  # Font for the title
        self.font_small = pygame.font.SysFont("Calibri", 50, bold=True)  # Font for the bottom buttons

        self.title_text = self.font_large.render("Match the Tiles", True, WHITE)  # Render the title text
        self.title_text_outline = self.font_large.render("Match the Tiles", True, BLUE)  # Render the title text

        self.start_normal = pygame.Rect(240, 760, 300, 150)  # Define the start button rectangle
        self.algorit = pygame.Rect(705, 10, 80, 80)  # Define the start button rectangle
        self.start_play_text = self.font_small.render("Play!", True, WHITE)
        self.logo_image = pygame.image.load("logo.png")
        self.algoritm = pygame.image.load("algoritm.png")

    def draw(self, screen):
        screen.fill(LIGHTBLUE)  # Fill the screen with black
        # Draw the title text
        screen.blit(self.logo_image, (self.screen_width // 2 - self.logo_image.get_width() // 2, 130))

        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx != 0 or dy != 0:
                    screen.blit(self.title_text_outline, (10 + dx, 325 + dy))

        # Blit the main text
        screen.blit(self.title_text, (10, 325))

        #screen.blit(self.title_text, (self.screen_width // 2 - self.title_text.get_width() // 2, 200))
        # Draw the start button
        pygame.draw.rect(screen, BLUE, self.start_normal)  # Green rectangle as the start button
         # Draw the start button
        pygame.draw.rect(screen, BLUE, self.start_advanced)  # Green rectangle as the start button
        pygame.draw.rect(screen, BLUE, self.algorit)
        scaled_image = pygame.transform.scale(self.algoritm, (80,80))
        screen.blit(scaled_image, (705, 10))

        screen.blit(self.start_normal_text, (self.start_normal.centerx - self.start_normal_text.get_width() // 2,
                                             self.start_normal.centery - self.start_normal_text.get_height() // 2))
        screen.blit(self.start_advanced_text, (self.start_advanced.centerx - self.start_advanced_text.get_width() // 2,
                                                self.start_advanced.centery - self.start_advanced_text.get_height() // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Check if left mouse button is clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_play.collidepoint(mouse_pos):
                        return True  # Return True if the start button is clicked
                    if self.algorit.collidepoint(mouse_pos):
                        return "choose"
        return False
