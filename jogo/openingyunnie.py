import pygame
from seti.sets import LIGHTBLUE, WHITE, BLUE


class OpeningPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Loading custom font might be needed if specific font style is used
        self.font_large = pygame.font.SysFont('Calibri', 60, bold=True)  # Title font
        self.font_small = pygame.font.SysFont('Calibri', 40, bold=True)  # Button font
        
        # Define the play button
        self.play_button = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
        self.title_surf = self.font_large.render('Match the Tiles', True, WHITE)
        self.title_rect = self.title_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        self.logo_image = pygame.image.load("logo.png")
        self.algoritm = pygame.image.load("algoritm.png")


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    return True
        return False

    def draw(self, screen):
        screen.fill(LIGHTBLUE)
        # Draw the title
        screen.blit(self.title_surf, self.title_rect)
        screen.blit(self.logo_image, (self.screen_width // 2 - self.logo_image.get_width() // 2, 130))
        # Draw the play button
        pygame.draw.rect(screen, BLUE, self.play_button)  # Play button background
        text = self.font_small.render('Play!', True, WHITE)  # Play text
        text_rect = text.get_rect(center=self.play_button.center)
        screen.blit(text, text_rect)
