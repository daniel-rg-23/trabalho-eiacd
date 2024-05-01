import pygame
from seti.sets import *

class MenuPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 45, bold=True)
        

        # Define buttons for menu options
        self.goback = pygame.Rect(580, 74, 144, 87)
        self.gobackmenu = pygame.image.load("gobackmenupage.png")
        self.puzzle1 = pygame.Rect((screen_width - 400) // 2-100, (screen_height - 50) // 2 - 400, 265, 90)
        self.puzzle2 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 250) // 2 - 400, 265, 90)
        self.puzzle3 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 550) // 2 - 400, 265, 90)
        self.puzzle4 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 850) // 2 - 400, 265, 90)
        self.puzzle5 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 1150) // 2 - 400, 265, 90)
        self.puzzle6 = pygame.Rect((screen_width - 400) // 2-100, (screen_height + 1450) // 2 - 400, 265, 90)

    def draw(self, screen):

        screen.fill(LIGHTBLUE)
        
        pygame.draw.rect(screen, BLUE, self.goback)

        scaled_image = pygame.transform.scale(self.gobackmenu, (144,87))
        screen.blit(scaled_image, (580, 74))


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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.puzzle1.collidepoint(mouse_pos):
                    return True  # Return True if a puzzle button is clicked
                elif self.goback.collidepoint(mouse_pos):
                    return "goback"  # Return "goback" if the Go Back button is clicked
        return False
    

    

