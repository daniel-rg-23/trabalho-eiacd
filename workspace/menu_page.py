import pygame
from seti.sets import *

class MenuPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 45, bold=True)
        

        # Define buttons for menu options
        self.goback = pygame.Rect(580, 70, 120, 80)
        self.puzzle1 = pygame.Rect((screen_width - 400) // 2-100, (screen_height - 50) // 2 - 400, 210, 50)
        self.puzzle2 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 130) // 2 - 400, 210, 50)
        self.puzzle3 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 310) // 2 - 400, 210, 50)
        self.puzzle4 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 490) // 2 - 400, 210, 50)
        self.puzzle5 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 670) // 2 - 400, 210, 50)
        self.puzzle6 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 850) // 2 - 400, 210, 50)
        self.puzzle7 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 1030) // 2 - 400, 210, 50)
        self.puzzle8 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 1210) // 2 - 400, 210, 50)
        self.puzzle9 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 1390) // 2 - 400, 210, 50)
        self.puzzle10 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 1570) // 2 - 400, 210, 50)
    def draw(self, screen):

        screen.fill(LIGHTBLUE)
        
        pygame.draw.rect(screen, BLUE, self.goback)

        pygame.draw.rect(screen, BLUE, self.puzzle1)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 1", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle1.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle2)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 2", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle2.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle3)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 3", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle3.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle4)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 4", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle4.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle5)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 5", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle5.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle6)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 6", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle6.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle7)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 7", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle7.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle8)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 8", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle8.center)
        screen.blit(start_text, start_text_pos)

        pygame.draw.rect(screen, BLUE, self.puzzle9)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 9", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle9.center)
        screen.blit(start_text, start_text_pos)
        
        pygame.draw.rect(screen, BLUE, self.puzzle10)
        # Draw text on buttons
        start_text = self.font.render("Puzzle 10", True, WHITE)
        start_text_pos = start_text.get_rect(center=self.puzzle10.center)
        screen.blit(start_text, start_text_pos)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.puzzle1.collidepoint(mouse_pos):
                    return True  # Return True if the start button is clicked
        return False  
    

    

