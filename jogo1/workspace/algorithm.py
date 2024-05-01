import pygame
from seti.sets import *
from level1 import *


class AlgorithmPage:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Calibri", 40, bold=True)
        self.selected_algorithms = []
        # Define buttons for menu options
        self.goback = pygame.Rect(580, 70, 160, 100)
        self.algoritmback = pygame.image.load("algoritmback.png")
        
        # Define rectangles for algorithms
        self.algorithm_rects = [
            pygame.Rect((screen_width - 400) // 2-130, (screen_height -50) // 2 - 400 + i * 130, 440, 100) 
            for i in range(7)
        ]
        
        # Algorithm names
        self.algorithm_names = [ "Breadth First Search", "Depth First Search", "Depth Limited Search", "Iterative Deepening", "Greedy", "A*", "Weighted A*"]
        
        # Initialize boolean variables for each algorithm
        
        self.bfs_selected = True
        self.dfs_selected = False
        self.dls_selected = False
        self.id_selected = False
        self.greedy_selected = False
        self.a_star_selected = False
        self.weighted_a_star_selected = False

    def draw(self, screen):
        screen.fill(LIGHTBLUE)
        
        pygame.draw.rect(screen, BLUE, self.goback)
        scaled_image = pygame.transform.scale(self.algoritmback, (160,100))
        screen.blit(scaled_image, (580, 70))

        # Draw buttons for each algorithm
        for rect, name, selected in zip(self.algorithm_rects, self.algorithm_names, [self.bfs_selected, self.dfs_selected, self.dls_selected, self.id_selected, self.greedy_selected, self.a_star_selected, self.weighted_a_star_selected]):
            if selected:
                color = ORANGE
            else:
                color = BLUE
            
            pygame.draw.rect(screen, color, rect)
            start_text = self.font.render(name, True, WHITE)
            start_text_pos = start_text.get_rect(center=rect.center)
            screen.blit(start_text, start_text_pos)

        # Update the display
        pygame.display.flip()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.goback.collidepoint(mouse_pos):
                    return "goback"
                
                # Check if any algorithm button is clicked
                for i, rect in enumerate(self.algorithm_rects):
                    if rect.collidepoint(mouse_pos):
                        # Reset all selected algorithms to False
                        self.bfs_selected = False
                        self.dfs_selected = False
                        self.dls_selected = False
                        self.id_selected = False
                        self.greedy_selected = False
                        self.a_star_selected = False
                        self.weighted_a_star_selected = False
                        
                        # Set the clicked algorithm to True directly
                        if i == 0:
                            self.bfs_selected = True
                        elif i == 1:
                            self.dfs_selected = True
                        elif i == 2:
                            self.dls_selected = True
                        elif i == 3:
                            self.id_selected = True
                        elif i == 4:
                            self.greedy_selected = True
                        elif i == 5:
                            self.a_star_selected = True
                        elif i == 6:
                            self.weighted_a_star_selected = True

                        

        return False


    def get_selected_algorithms(self):
        return (
            self.bfs_selected,
            self.dfs_selected,
            self.dls_selected,
            self.id_selected,
            self.greedy_selected,
            self.a_star_selected,
            self.weighted_a_star_selected
        )