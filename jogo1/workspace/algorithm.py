import pygame
from seti.sets import *

class AlgorithmPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 45, bold=True)
        
        # Define buttons for menu options
        self.goback = pygame.Rect(580, 70, 160, 100)
        self.BFS = pygame.Rect((screen_width - 400) // 2-100, (screen_height - 50) // 2 - 400, 310, 50)
        self.DFS = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 130) // 2 - 400, 310, 50)
        self.Iterative_D = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 310) // 2 - 400, 310, 50)
        self.Greedy = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 490) // 2 - 400, 310, 50)
        self.A_star = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 670) // 2 - 400, 310, 50)
        self.Weighted_A_star = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 850) // 2 - 400, 310, 50)
        self.algoritmback = pygame.image.load("algoritmback.png")
        
    def draw(self, screen):
        screen.fill(LIGHTBLUE)
        
        pygame.draw.rect(screen, BLUE, self.goback)
        scaled_image = pygame.transform.scale(self.algoritmback, (160,100))
        screen.blit(scaled_image, (580, 70))

        pygame.draw.rect(screen, ORANGE, self.BFS)
        # Draw text on buttons
        start_text = self.font.render("BFS", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.BFS.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, ORANGE, self.DFS)
        # Draw text on buttons
        start_text = self.font.render("DFS", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.DFS.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, ORANGE, self.Iterative_D)
        # Draw text on buttons
        start_text = self.font.render("Iterative D", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.Iterative_D.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.Greedy)
        # Draw text on buttons
        start_text = self.font.render("Greedy", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.Greedy.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.A_star)
        # Draw text on buttons
        start_text = self.font.render("A*", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.A_star.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.Weighted_A_star)
        # Draw text on buttons
        start_text = self.font.render("Weighted A*", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.Weighted_A_star.center)
        screen.blit(start_text, start_text_pos)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.BFS.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked
                if self.DFS.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked    
                if self.Iterative_D.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked
                if self.Greedy.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked
                if self.A_star.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked
                if self.Weighted_A_star.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked
                elif self.goback.collidepoint(mouse_pos):
                    return "goback"
        return False
