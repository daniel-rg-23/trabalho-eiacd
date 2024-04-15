import pygame
from seti.sets import *

class AlgorithmPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 45, bold=True)
        
        # Define buttons for menu options
        self.goback = pygame.Rect(580, 70, 160, 100)
        self.puzzle1 = pygame.Rect((screen_width - 400) // 2-100, (screen_height +300) // 2 - 400, 400, 200)
        self.puzzle2 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 950) // 2 - 400, 400, 200)
        self.algoritmback = pygame.image.load("algoritmback.png")
        
    def draw(self, screen):
        screen.fill(LIGHTBLUE)
        
        pygame.draw.rect(screen, BLUE, self.goback)
        scaled_image = pygame.transform.scale(self.algoritmback, (160,100))
        screen.blit(scaled_image, (580, 70))

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.goback.collidepoint(mouse_pos):
                    return "goback"
        return False

    