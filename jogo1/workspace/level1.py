import pygame
from seti.sets import *
from opening_page import *
from algorithm import AlgorithmPage
import copy
from collections import deque
import time
import heapq

TILESIZE = 200
pygame.font.init()

class Tile:
    def __init__(self,game,x,y, text,color,GAME_SIZE):
        self.GAME_SIZE = GAME_SIZE
        self.game = game
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.x, self.y=x,y
        self.text = text
        self.rect = self.image.get_rect()
        self.color = color
        
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
        
    def right(self):
        return self.rect.x + TILESIZE < self.GAME_SIZE * TILESIZE
    def left(self):
        return self.rect.x - TILESIZE >= 0
    def up(self):
        return self.rect.y - TILESIZE >= 0
    def down(self):
        return self.rect.y + TILESIZE < self.GAME_SIZE * TILESIZE
    

class Game:

    def __init__(self,QUIET_TILES,MOVABLE_TILES,MATCH_TILES,GAME_SIZE,NUMBER,COLOUR,COLOUR2):
        pygame.init()
        self.GAME_SIZE = GAME_SIZE
        self.QUIET_TILES = QUIET_TILES
        self.MOVABLE_TILES = MOVABLE_TILES
        self.MATCH_TILES = MATCH_TILES
        self.colour = COLOUR
        self.colour2 = COLOUR2
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.overlay_alpha = 128  # Adjust the transparency level (0-255)
        self.overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        self.checkmarks_appeared = False
        self.tiles = []   
        self.all_sprites = pygame.sprite.Group()        
        self.quiet_tiles = self.create_game()
        self.movable_tiles = self.create_game1()
        self.match_tiles = self.create_game2()
        self.number_tiles_move = NUMBER
        self.initial_state = self.grid_to_matrix()
        self.home = pygame.Rect((WIDTH - 96) // 2 -150,(HEIGHT - 96) // 2 +110, 100, 100)
        self.resart2 = pygame.Rect((WIDTH - 96) // 2 ,(HEIGHT - 96) // 2 +110, 100, 100)
        self.next = pygame.Rect((WIDTH - 96) // 2 +150,(HEIGHT - 96) // 2 +110, 100, 100)
        self.resart = pygame.Rect((WIDTH - 96) // 2 - 55,(HEIGHT - 96) // 2 -348, 96, 96)
        self.undo = pygame.Rect((WIDTH - 96) // 2 - 188,(HEIGHT - 96) // 2 - 348, 96, 96)
        self.heuristic=pygame.Rect((WIDTH - 96) // 2 - 322,(HEIGHT - 96) // 2 - 348, 96, 96)
        self.state_stack = []  # Stack to store game states
        self.counter = 0
        self.push_state()
        self.lampada = pygame.image.load("lampadamenu1.png")
        self.goback = pygame.image.load("gobackmenu2.png")
        self.reset = pygame.image.load("resetmenu3.png")
        self.homeoverlay = pygame.image.load("homeoverlay.png")
        self.replayoverlay = pygame.image.load("replayoverlay.png")
        self.nextleveloverlay = pygame.image.load("nextleveloverlay.png")

    def grid_to_matrix(self):
        matrix = [[0 for _ in range(self.GAME_SIZE)] for _ in range(self.GAME_SIZE)]

        # Iterate over each tile
        for row in range(self.GAME_SIZE):
            for col in range(self.GAME_SIZE):
                # Check the type of tile and update the board matrix accordingly
                if (col, row) in self.QUIET_TILES:
                    matrix[row][col] = 1  # Quiet tile
                elif (col, row) in self.MOVABLE_TILES:
                    matrix[row][col] = 2  # Movable tile
                elif (col, row) in self.MATCH_TILES:
                    matrix[row][col] = 3  # Match tile
        return matrix

    def solve_puzzle(self, chosen):
        #algorithm_page = AlgorithmPage(WIDTH,HEIGHT)
        selected_algorithms = chosen

        initial_state = self.grid_to_matrix()
        print(initial_state)
        # Instantiate PuzzleSolver with the initial state
        solver = PuzzleSolver(initial_state,self.GAME_SIZE,self.MATCH_TILES)
    
        if selected_algorithms[0]:
            goal_node = solver.breadth_first_search()
        elif selected_algorithms[1]:
            goal_node = solver.depth_first_search()
        elif selected_algorithms[2]:
            goal_node = solver.depth_limited_search(depth_limit=5)
        elif selected_algorithms[3]:
            goal_node = solver.iterative_deepening(depth_limit=10)
        elif selected_algorithms[4]:
            goal_node = solver.greedy_search(PuzzleSolver.manhattan_distance)
        elif selected_algorithms[5]:
            goal_node = solver.a_star_search(solver.goal_state_func, solver.cost_function, solver.operators_func)
        elif selected_algorithms[6]:
            goal_node = solver.weighted_a_star_search(solver.goal_state_func, solver.cost_function, solver.operators_func, w=2)
        
        if goal_node:
            result_directions = solver.retrieve_path(goal_node)
            print(result_directions)
            return result_directions
        else:
            return None

    def apply_solution(self, solution):
        # Clear the state stack and reset the counter
        self.state_stack.clear()
        self.state_stack.append(copy.deepcopy(self.initial_state))  # Add the initial state to the stack
        self.counter = 0

        # Iterate through the solution path and update the game state
        for direction in solution:
            # Move the tile based on the direction
            self.move_tile(direction)
            time.sleep(0.7)
            # Append the current state to the state stack
            self.state_stack.append(copy.deepcopy(self.state_stack[-1]))
            
            # Increment the counter
            self.counter += 1
            self.draw()
        pygame.display.flip()

    def push_state(self):
            # Simplify the state information being pushed for clarity
            state_to_push = (copy.deepcopy(self.quiet_tiles), copy.deepcopy(self.movable_tiles), copy.deepcopy(self.match_tiles), self.counter)
            self.state_stack.append(state_to_push)
        
    def pop_state(self):
        if self.state_stack:
            prev_state = self.state_stack.pop()
            self.quiet_tiles, self.movable_tiles, self.match_tiles, self.counter = prev_state
            self.draw()  # Update the display after undoing the move

    def reset_level(self):
        # Reset all game variables to their initial state
        self.quiet_tiles = self.create_game()
        self.movable_tiles = self.create_game1()
        self.match_tiles = self.create_game2()
        self.counter = 0
        self.checkmarks_appeared = False
        self.draw()  # Redraw the screen after resetting the level

    def draw_overlay(self):
        # Draw the dark overlay transparent page
        self.screen.blit(self.overlay_surface, (0, 0))

        # Light blue rectangle
        rect_width = 600 # Adjust as needed
        rect_height = 500  # Adjust as needed
        rect_x = (self.screen.get_width() - rect_width) // 2
        rect_y = (self.screen.get_height() - rect_height) // 2 
        pygame.draw.rect(self.screen, LIGHTBLUE, (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(self.screen, BLUE, self.home)
        pygame.draw.rect(self.screen, BLUE, self.resart2)
        pygame.draw.rect(self.screen, BLUE, self.next)
        
        scaled_image = pygame.transform.scale(self.homeoverlay, (100,100))
        self.screen.blit(scaled_image, ((self.screen.get_width() - scaled_image.get_width()) // 2-148, 562))

        scaled_image = pygame.transform.scale(self.replayoverlay, (100,100))
        self.screen.blit(scaled_image, ((self.screen.get_width() - scaled_image.get_width()) // 2, 562))

        scaled_image = pygame.transform.scale(self.nextleveloverlay, (100,100))
        self.screen.blit(scaled_image, ((self.screen.get_width() - scaled_image.get_width()) // 2+148, 562))
        # Text to display
        text = "Puzzle solved"
        font = pygame.font.SysFont("Calibri", 80, bold=True)  # Use default system font, size 36
        text_surface = font.render(text, True, BLUEGREEN)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3 + 15))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text

        text = "You solved this puzzle in " + str (self.counter) + " moves"
        font = pygame.font.SysFont("Calibri", 30)  # Use default system font, size 36
        text_surface = font.render(text, True, BLUEGREEN)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3 + 115))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text

        text = "Perfect move: 4 moves"
        font = pygame.font.SysFont("Calibri", 30)  # Use default system font, size 36
        text_surface = font.render(text, True, BLUEGREEN)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3 + 165))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text   

    def draw_rectangles(self):
    
        rect_width = 373 # Adjust as needed
        rect_height = 191 # Adjust as needed
        rect_x = (self.screen.get_width() - rect_width) // 2+193
        rect_y = (self.screen.get_height() - rect_height) // 2 - 394
        pygame.draw.rect(self.screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

        rect_width = 373 # Adjust as neededresized_image = pygame.transform.scale(image, (50, 50))
        rect_height = 83 # Adjust as needed
        rect_x = (self.screen.get_width() - rect_width) // 2-193
        rect_y = (self.screen.get_height() - rect_height) // 2 - 447

        pygame.draw.rect(self.screen, BLUE, (rect_x, rect_y, rect_width, rect_height))
        
        

        pygame.draw.rect(self.screen, BLUE, self.heuristic)
        
        pygame.draw.rect(self.screen, BLUE, self.undo)
        
        pygame.draw.rect(self.screen, BLUE, self.resart)
        
        scaled_image = pygame.transform.scale(self.lampada, (96,96))
        self.screen.blit(scaled_image, ((self.screen.get_width() - scaled_image.get_width()) // 2-323, 104))

        scaled_image = pygame.transform.scale(self.goback, (96,96))
        self.screen.blit(scaled_image, ((self.screen.get_width() - scaled_image.get_width()) // 2-188, 104))

        scaled_image = pygame.transform.scale(self.reset, (96,96))
        self.screen.blit(scaled_image, ((self.screen.get_width() - scaled_image.get_width()) // 2-55, 104))

        # Text to display
        text = "Puzzle 1"
        font = pygame.font.SysFont("Calibri", 45, bold=True)  # Use default system font, size 36
        text_surface = font.render(text, True, LIGHTBLUE)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 -194, self.screen.get_height() // 3 -283))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text


        # Text to display
        text = f"Moves: {self.counter}"
        font = pygame.font.SysFont("Calibri", 40)  # Use default system font, size 36
        text_surface = font.render(text, True, LIGHTBLUE)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 186, self.screen.get_height() // 3 -270))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text
        
        # Text to display
        text = "Perfect: 4"
        font = pygame.font.SysFont("Calibri", 40)  # Use default system font, size 36
        text_surface = font.render(text, True, LIGHTBLUE)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 183, self.screen.get_height() // 3 -190))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text

    def create_game(self):
        # Initialize the grid with all tiles set to 0
        grid = [[0 for _ in range(self.GAME_SIZE)] for _ in range(self.GAME_SIZE)]
        # Define positions where specific tiles should appear

        # Place specific tiles at the defined positions
        for x, y in self.QUIET_TILES:
            grid[y][x] = x + y * self.GAME_SIZE + 1  # Example: Place tile numbers at specified positions
        return grid
    
    def create_game1(self):
        grid = [[0 for _ in range(self.GAME_SIZE)] for _ in range(self.GAME_SIZE)]

        for x, y in self.MOVABLE_TILES:
            grid[y][x] = x + y * self.GAME_SIZE + 1
        return grid
    
    def create_game2(self):
        grid = [[0 for _ in range(self.GAME_SIZE)] for _ in range(self.GAME_SIZE)]

        
        for x, y in self.MATCH_TILES:
            grid[y][x] = x + y * self.GAME_SIZE + 1
        return grid
        

    def draw_tiles(self):
        # Define the size and position of the square area where the grid will be drawn
        square_size = min(self.screen.get_width(), self.screen.get_height()) - 50  # Adjust as needed
        square_x = (self.screen.get_width() - square_size) // 2
        square_y = (self.screen.get_height() - square_size) // 2 + 90

        # Calculate the size of each grid cell based on the square size and the game size
        cell_size = square_size // self.GAME_SIZE

        # Clear the previous tiles list
        self.tiles.clear()
        counter = 0
        # Draw tiles within the grid
        for row, row_tiles in enumerate(self.quiet_tiles):
            for col, tile_value in enumerate(row_tiles):
                # If the tile value is not zero, draw the tile
                if tile_value != 0:
                    # Calculate the pixel position of the tile based on its grid position
                    tile_x = square_x + col * cell_size + 5  # Adjusted to fit inside the grid lines
                    tile_y = square_y + row * cell_size + 5  # Adjusted to fit inside the grid lines

                    # Determine tile color (you can customize this based on your requirements)
                    tile_color = QUIETBLUE

                    # Create the tile object and add it to the tiles list and sprite group
                    tile = pygame.Rect(tile_x, tile_y, cell_size - 10, cell_size - 10)  # Adjusted to fit inside the grid lines
                    pygame.draw.rect(self.screen, tile_color, tile)

        for row, row_tiles in enumerate(self.match_tiles):
            for col, tile_value in enumerate(row_tiles):
                # If the tile value is not zero, draw the tile
                if tile_value != 0:
                    # Calculate the pixel position of the circle based on its grid position
                    circle_x = square_x + col * cell_size + cell_size // 2
                    circle_y = square_y + row * cell_size + cell_size // 2
                    self.circle_radius = cell_size // 5  # Adjust as needed
                    self.circle_color = self.colour
                    pygame.draw.circle(self.screen, self.circle_color, (circle_x, circle_y), self.circle_radius)

        # Draw the movable tiles
        for row, row_tiles in enumerate(self.movable_tiles):
            for col, tile_value in enumerate(row_tiles):
                # If the tile value is not zero, draw the tile
                if tile_value != 0:
                    # Calculate the pixel position of the tile based on its grid position
                    tile_x = square_x + col * cell_size + 5  # Adjusted to fit inside the grid lines
                    tile_y = square_y + row * cell_size + 5  # Adjusted to fit inside the grid lines

                    # Determine tile color
                    tile_color = self.colour

                    # Draw the movable tile
                    tile_rect = pygame.Rect(tile_x, tile_y, cell_size - 10, cell_size - 10)  # Adjusted to fit inside the grid lines
                    pygame.draw.rect(self.screen, tile_color, tile_rect)

                    # Check if the movable tile is over a match tile
                    if (col, row) in [(x, y) for y in range(self.GAME_SIZE) for x in range(self.GAME_SIZE) if self.match_tiles[y][x] != 0]:
                        
                        # Draw the checkmark symbol
                        # Coordinates for the checkmark lines
                        if self.GAME_SIZE==4:
                            checkmark_lines = [
                                [(tile_x + 40, tile_y + 75), (tile_x + 77, tile_y + 150)],  # Line 1
                                [(tile_x + 77, tile_y + 150), (tile_x + 137, tile_y + 30)]    # Line 2
                            ]
                        if self.GAME_SIZE==5:
                            checkmark_lines = [
                                [(tile_x + 23, tile_y + 55), (tile_x + 60, tile_y + 130)],  # Line 1
                                [(tile_x + 60, tile_y + 130), (tile_x + 120, tile_y + 10)]    # Line 2
                            ]

                        # Draw each line segment with thicker lines (thickness = 10)
                        for line in checkmark_lines:
                            pygame.draw.line(self.screen, self.colour2, line[0], line[1], 35)
                        counter+=1
                    else:
                        # Draw the blue circle centered on the tile
                        circle_x = square_x + col * cell_size + cell_size // 2
                        circle_y = square_y + row * cell_size + cell_size // 2
                        circle_radius = cell_size // 5  # Adjust as needed
                        circle_color = LIGHTBLUE
                        pygame.draw.circle(self.screen, circle_color, (circle_x, circle_y), circle_radius)
                        counter=0
                        
        if counter == self.number_tiles_move:
            self.checkmarks_appeared = True

    def new(self):
        self.all_sprites.empty()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False

    def move_tile(self, direction):
        self.tiles_that_move = []
        # Check if there's at least one movable tile in the line
        movable_in_line = False
        for row in range(self.GAME_SIZE):
            for col in range(self.GAME_SIZE):
                if self.movable_tiles[row][col] != 0:
                    movable_in_line = True
                    break

        # If there are no movable tiles in the line, return
        if not movable_in_line:
            return

        # Otherwise, perform movement for the entire line in the specified direction
        
        if direction == 'up':
            for col in range(self.GAME_SIZE):
                for row in range(1, self.GAME_SIZE):
                    if self.movable_tiles[row][col] != 0:
                        for k in range(row, 0, -1):
                            if self.movable_tiles[k - 1][col] == 0 and self.quiet_tiles[k - 1][col] == 0:
                                self.movable_tiles[k - 1][col] = self.movable_tiles[k][col]
                                self.movable_tiles[k][col] = 0
                            elif self.movable_tiles[k - 1][col] == self.movable_tiles[k][col]:
                                # Merge the tiles if they have the same value
                                self.movable_tiles[k - 1][col] *= 2
                                self.movable_tiles[k][col] = 0
                                break
        
        elif direction == 'down':
            for col in range(self.GAME_SIZE):
                for row in range(self.GAME_SIZE - 2, -1, -1):
                    if self.movable_tiles[row][col] != 0:
                        for k in range(row, self.GAME_SIZE - 1):
                            if self.movable_tiles[k + 1][col] == 0 and self.quiet_tiles[k + 1][col] == 0:
                                self.movable_tiles[k + 1][col] = self.movable_tiles[k][col]
                                self.movable_tiles[k][col] = 0
                            elif self.movable_tiles[k + 1][col] == self.movable_tiles[k][col]:
                                # Merge the tiles if they have the same value
                                self.movable_tiles[k + 1][col] *= 2
                                self.movable_tiles[k][col] = 0
                                break

        elif direction == 'left':
            for row in range(self.GAME_SIZE):
                for col in range(1, self.GAME_SIZE):
                    if self.movable_tiles[row][col] != 0:
                        for k in range(col, 0, -1):
                            if self.movable_tiles[row][k - 1] == 0 and self.quiet_tiles[row][k - 1] == 0:
                                self.movable_tiles[row][k - 1] = self.movable_tiles[row][k]
                                self.movable_tiles[row][k] = 0
                            elif self.movable_tiles[row][k - 1] == self.movable_tiles[row][k]:
                                # Merge the tiles if they have the same value
                                self.movable_tiles[row][k - 1] *= 2
                                self.movable_tiles[row][k] = 0
                                break
        
        elif direction == 'right':
            for row in range(self.GAME_SIZE):
                for col in range(self.GAME_SIZE - 2, -1, -1):
                    if self.movable_tiles[row][col] != 0:
                        for k in range(col, self.GAME_SIZE - 1):
                            if self.movable_tiles[row][k + 1] == 0 and self.quiet_tiles[row][k + 1] == 0:
                                self.movable_tiles[row][k + 1] = self.movable_tiles[row][k]
                                self.movable_tiles[row][k] = 0
                            elif self.movable_tiles[row][k + 1] == self.movable_tiles[row][k]:
                                # Merge the tiles if they have the same value
                                self.movable_tiles[row][k + 1] *= 2
                                self.movable_tiles[row][k] = 0
                                break

        for row in range(self.GAME_SIZE):
            for col in range(self.GAME_SIZE):
                if self.movable_tiles[row][col] != 0:
                    self.tiles_that_move.append((col, row))

        self.grid_to_matrix()

    def handle_key_press(self, key):
        if key == pygame.K_UP:
            self.move_tile('up')
        elif key == pygame.K_DOWN:
            self.move_tile('down')
        elif key == pygame.K_LEFT:
            self.move_tile('left')
        elif key == pygame.K_RIGHT:
            self.move_tile('right')


    def run(self, chosen):
        self.playing = True
        self.grid_to_matrix()
        while self.playing:
            self.events(chosen)
            self.update()
            self.draw()
     

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                

        self.all_sprites.update()

    def draw_grid(self):
        # Define the size and position of the square area where the grid will be drawn
        square_size = min(self.screen.get_width(), self.screen.get_height()) - 50  # Adjust as needed
        square_x = (self.screen.get_width() - square_size) // 2
        square_y = (self.screen.get_height() - square_size) // 2 + 90

        # Calculate the size of each grid cell based on the square size and the game size
        cell_size = square_size // self.GAME_SIZE

        # Set the thickness of the grid lines
        line_thickness = 12  # Adjust as needed

        # Draw horizontal grid lines within the square area
        for row in range(0, self.GAME_SIZE + 1):
            pygame.draw.line(self.screen, BLUE, (square_x, square_y + row * cell_size),
                            (square_x + square_size, square_y + row * cell_size), line_thickness)

        # Draw vertical grid lines within the square area
        for col in range(0, self.GAME_SIZE + 1):
            pygame.draw.line(self.screen, BLUE, (square_x + col * cell_size, square_y),
                            (square_x + col * cell_size, square_y + square_size), line_thickness)

    def draw(self):
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_tiles()
        self.draw_rectangles()
        if self.checkmarks_appeared:
            self.draw_overlay() 
            # Blit the blue page surface over the overlay surface
        pygame.display.flip()

    
    def events(self, chosen):
        
        if self.checkmarks_appeared:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.home.collidepoint(mouse_pos):
                       self.playing = False
                       self.reset_level()
                    elif self.resart2.collidepoint(mouse_pos):
                       self.reset_level()
            return False
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.resart.collidepoint(mouse_pos):
                    self.reset_level()
                elif self.undo.collidepoint(mouse_pos):
                    self.pop_state()  # Call the pop_state method to restore the previous game state
                elif self.heuristic.collidepoint(mouse_pos):
                    solution = self.solve_puzzle(chosen)
                    if solution:
                        self.apply_solution(solution)
            # Handle other mouse button clicks
            elif event.type == pygame.KEYDOWN:
                # Push the current game state onto the stack before handling movement commands
                self.push_state()
                # Handle key presses
                if event.key == pygame.K_UP:
                    initial_state = copy.deepcopy(self.movable_tiles)  # Store initial state of movable tiles
                    self.move_tile('up')
                    
                    # Check if any tile was moved by comparing current and initial state
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(self.GAME_SIZE) for col in range(self.GAME_SIZE)):
                        self.counter += 1
                elif event.key == pygame.K_DOWN:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('down')
                    
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(self.GAME_SIZE) for col in range(self.GAME_SIZE)):
                        self.counter += 1
                elif event.key == pygame.K_LEFT:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('left')
                    
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(self.GAME_SIZE) for col in range(self.GAME_SIZE)):
                        self.counter += 1
                elif event.key == pygame.K_RIGHT:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('right')
                    
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(self.GAME_SIZE) for col in range(self.GAME_SIZE)):
                        self.counter += 1


class TreeNode:
    def __init__(self, state, parent=None, direction=None, heuristic=0, cost=0, g=0, h=0,):
        self.state = state
        self.direction = direction
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost
        self.g = g
        self.h = h
        self.children = []

    def __lt__(self, other):
        return self.cost < other.cost

class PuzzleSolver:
    def __init__(self, initial_state,GAME_SIZE,MATCH_TILES):
        self.GAME_SIZE = GAME_SIZE
        self.MATCH_TILES = MATCH_TILES
        self.initial_state = initial_state
        self.initial_threes = self.find_threes(initial_state)

    def find_threes(self, matrix):
        threes = []
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if val == 3:
                    threes.append((i, j))
        return threes

    def goal_state_func(self, state):
        return state[1][0] == 2 and state[2][0] == 2

    def move_tile1(self, state, direction, row1, col1, row2, col2):
        new_state = copy.deepcopy(state)

        if direction == 'up':
            while row1 > 0 and new_state[row1 - 1][col1] != 1:
                new_state[row1][col1], new_state[row1 - 1][col1] = new_state[row1 - 1][col1], new_state[row1][col1]
                if (row1 - 1, col1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                row1 -= 1

            while row2 > 0 and new_state[row2 - 1][col2] != 1:
                new_state[row2][col2], new_state[row2 - 1][col2] = new_state[row2 - 1][col2], new_state[row2][col2]
                if (row2 - 1, col2) not in self.initial_threes:
                    new_state[row2][col2] = 0
                row2 -= 1

        elif direction == 'down':
            while row1 < GAME_SIZE - 1 and new_state[row1 + 1][col1] != 1:
                new_state[row1][col1], new_state[row1 + 1][col1] = new_state[row1 + 1][col1], new_state[row1][col1]
                if (row1 + 1, col1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                row1 += 1

            while row2 < GAME_SIZE - 1 and new_state[row2 + 1][col2] != 1:
                new_state[row2][col2], new_state[row2 + 1][col2] = new_state[row2 + 1][col2], new_state[row2][col2]
                if (row2 + 1, col2) not in self.initial_threes:
                    new_state[row2][col2] = 0
                row2 += 1

        elif direction == 'left':
            while col1 > 0 and new_state[row1][col1 - 1] != 1:
                new_state[row1][col1], new_state[row1][col1 - 1] = new_state[row1][col1 - 1], new_state[row1][col1]
                if (row1, col1 - 1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                col1 -= 1

            while col2 > 0 and new_state[row2][col2 - 1] != 1:
                new_state[row2][col2], new_state[row2][col2 - 1] = new_state[row2][col2 - 1], new_state[row2][col2]
                if (row2, col2 - 1) not in self.initial_threes:
                    new_state[row2][col2] = 0
                col2 -= 1

        elif direction == 'right':
            while col1 < GAME_SIZE - 1 and new_state[row1][col1 + 1] != 1:
                new_state[row1][col1], new_state[row1][col1 + 1] = new_state[row1][col1 + 1], new_state[row1][col1]
                if (row1, col1 + 1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                col1 += 1

            while col2 < GAME_SIZE - 1 and new_state[row2][col2 + 1] != 1:
                new_state[row2][col2], new_state[row2][col2 + 1] = new_state[row2][col2 + 1], new_state[row2][col2]
                if (row2, col2 + 1) not in self.initial_threes:
                    new_state[row2][col2] = 0
                col2 += 1

        return new_state

    def operators_func(self, state):
        successors = []

        for row1 in range(len(state)):
            for col1 in range(len(state[0])):
                if state[row1][col1] == 2:
                    for row2 in range(len(state)):
                        for col2 in range(len(state[0])):
                            if state[row2][col2] == 2 and (row1 != row2 or col1 != col2):
                                new_state_up = self.move_tile1(state, 'up', row1, col1, row2, col2)
                                new_state_down = self.move_tile1(state, 'down', row1, col1, row2, col2)
                                new_state_left = self.move_tile1(state, 'left', row1, col1, row2, col2)
                                new_state_right = self.move_tile1(state, 'right', row1, col1, row2, col2)

                                if new_state_up and new_state_up != state:
                                    successors.append((new_state_up, 'up'))

                                if new_state_down and new_state_down != state:
                                    successors.append((new_state_down, 'down'))

                                if new_state_left and new_state_left != state:
                                    successors.append((new_state_left, 'left'))

                                if new_state_right and new_state_right != state:
                                    successors.append((new_state_right, 'right'))

        return successors



    def breadth_first_search(self):
            root = TreeNode(self.initial_state)
            queue = deque([root])

            if not isinstance(self.initial_state, list) or not all(isinstance(row, list) for row in self.initial_state):
                raise ValueError("Initial state must be a list of lists.")

            visited = set([tuple(map(tuple, self.initial_state))])

            while queue:
                node = queue.popleft()

                if self.goal_state_func(node.state):
                    return node

                for state, direction in self.operators_func(node.state):
                    if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                        raise ValueError("State must be a list of lists.")
                    
                    state_tuple = tuple(map(tuple, state))
                    
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        child_node = TreeNode(state=state, parent=node, direction=direction)
                        node.children.append(child_node)
                        queue.append(child_node)

            return None
    def depth_first_search(self):
        root = TreeNode(self.initial_state)
        stack = deque([root])
        visited = set([tuple(map(tuple, self.initial_state))])

        while stack:
            node = stack.pop()

            if self.goal_state_func(node.state):
                return node

            for state, direction in self.operators_func(node.state):
                if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                    raise ValueError("State must be a list of lists.")
                
                state_tuple = tuple(map(tuple, state))
                
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node, direction=direction)
                    node.children.append(child_node)
                    stack.append(child_node)
        return None

    def depth_limited_search(self, depth_limit):
        def sub_dls(node, depth, visited):
            if self.goal_state_func(node.state):
                return node
            if depth == depth_limit:
                return None

            for state, direction in self.operators_func(node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node, direction=direction)
                    result = sub_dls(child_node, depth + 1, visited)
                    if result:
                        return result
            return None

        visited = set([tuple(map(tuple, self.initial_state))])
        return sub_dls(TreeNode(self.initial_state), 0, visited)
    
    def iterative_deepening(self, depth_limit):
        for depth in range(depth_limit):
            result = self.depth_limited_search(depth)
            if result:
                return result
        return None
    
    @staticmethod
    def manhattan_distance(state):
        distance = 0
        for r, row in enumerate(state):
            for c, val in enumerate(row):
                if val == 2:
                    # Calculate Manhattan distance for the first '2' tile
                    distance += abs(r - 1) + abs(c - 0)
                    # Calculate Manhattan distance for the second '2' tile
                    distance += abs(r - 2) + abs(c - 0)
        return distance
    

    def greedy_search(self, heuristic_func):
        open_list = []
        initial_node = TreeNode(self.initial_state, heuristic=heuristic_func(self.initial_state))
        heapq.heappush(open_list, initial_node)
        
        visited = set([tuple(map(tuple, self.initial_state))])

        while open_list:
            current_node = heapq.heappop(open_list)

            if self.goal_state_func(current_node.state):
                return current_node

            visited.add(tuple(map(tuple, current_node.state)))

            for state, direction in self.operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    successor_node = TreeNode(state, current_node, direction, heuristic=heuristic_func(state))
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None
    
    def cost_function(self, node, w=1):
        return node.g + w * self.manhattan_distance(node.state)


    def a_star_search(self, goal_test_func, cost_func, operators_func):
        return self.weighted_a_star_search(goal_test_func, cost_func, operators_func, w=1)

    def weighted_a_star_search(self, goal_test_func, cost_func, operators_func, w=1):
        open_list = []
        initial_node = TreeNode(
            self.initial_state,
            heuristic=self.manhattan_distance(self.initial_state),
            g=0,
            h=self.manhattan_distance(self.initial_state),
            cost=self.cost_function(TreeNode(self.initial_state), w)
        )
        heapq.heappush(open_list, initial_node)

        visited = set([tuple(map(tuple, self.initial_state))])

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_test_func(current_node.state):
                return current_node

            visited.add(tuple(map(tuple, current_node.state)))

            for state, direction in operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    g = current_node.g + 1  # Assuming each move has a cost of 1
                    h = self.manhattan_distance(state)
                    successor_node = TreeNode(
                        state,
                        parent=current_node,
                        direction=direction,
                        heuristic=h,
                        g=g,
                        h=h
                    )
                    successor_node.cost = cost_func(successor_node, w)
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None

    def retrieve_path(self, node):
        path = []
        while node:
            if node.direction:
                path.append(node.direction)
            node = node.parent
        return path[::-1] if path else ["No path found"]