import pygame
from seti.sets import *
from opening_page import *
import copy
from collections import deque
import heapq
from algorithm import *



TILESIZE = 200
GAME_SIZE = 4
pygame.font.init()


class Tile():
    def __init__(self,game,x,y, text,color):
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
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE
    def left(self):
        return self.rect.x - TILESIZE >= 0
    def up(self):
        return self.rect.y - TILESIZE >= 0
    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE
        
class Game5:
    QUIET_TILES = [(0, 1), (1, 1), (1, 3), (2, 2)]
    MOVABLE_TILES = [(0,0), (2, 3)]
    MATCH_TILES = [(0, 3), (1,2)]
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.overlay_alpha = 128  # Adjust the transparency level (0-255)
        self.overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        self.checkmarks_appeared = False
        self.tiles = []   
        self.all_sprites = pygame.sprite.Group()        
        self.tiles_that_are_quiet = Game5.QUIET_TILES
        self.tiles_that_move = Game5.MOVABLE_TILES
        self.tiles_to_be_matched = Game5.MATCH_TILES
        self.quiet_tiles = self.create_gameA()
        self.movable_tiles = self.create_game1A()
        self.match_tiles = self.create_game2A()
        self.number_tiles_move = 2
        self.initial_state = self.grid_to_matrix()
        self.initial_threes = self.find_threes(self.initial_state)
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
    
    def goal_state_func(self, state):
        return state[1][0] == 2 and state[2][0] == 2

    def move_tile1(self, state, direction, row1, col1, row2, col2):
        new_state = copy.deepcopy(state)
        moved = False

        if direction == 'up':
            # Move tile from (row1, col1) upwards
            while row1 > 0 and new_state[row1 - 1][col1] != 1:
                new_state[row1][col1], new_state[row1 - 1][col1] = new_state[row1 - 1][col1], new_state[row1][col1]
                if (row1 - 1, col1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                row1 -= 1
                moved = True

            # Move tile from (row2, col2) upwards
            while row2 > 0 and new_state[row2 - 1][col2] != 1:
                new_state[row2][col2], new_state[row2 - 1][col2] = new_state[row2 - 1][col2], new_state[row2][col2]
                if (row2 - 1, col2) not in self.initial_threes:
                    new_state[row2][col2] = 0
                row2 -= 1
                moved = True

        elif direction == 'down':
            # Move tile from (row1, col1) downwards
            while row1 < GAME_SIZE - 1 and new_state[row1 + 1][col1] != 1:
                new_state[row1][col1], new_state[row1 + 1][col1] = new_state[row1 + 1][col1], new_state[row1][col1]
                if (row1 + 1, col1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                row1 += 1
                moved = True

            # Move tile from (row2, col2) downwards
            while row2 < GAME_SIZE - 1 and new_state[row2 + 1][col2] != 1:
                new_state[row2][col2], new_state[row2 + 1][col2] = new_state[row2 + 1][col2], new_state[row2][col2]
                if (row2 + 1, col2) not in self.initial_threes:
                    new_state[row2][col2] = 0
                row2 += 1
                moved = True

        elif direction == 'left':
            # Move tile from (row1, col1) leftwards
            while col1 > 0 and new_state[row1][col1 - 1] != 1:
                new_state[row1][col1], new_state[row1][col1 - 1] = new_state[row1][col1 - 1], new_state[row1][col1]
                if (row1, col1 - 1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                col1 -= 1
                moved = True

            # Move tile from (row2, col2) leftwards
            while col2 > 0 and new_state[row2][col2 - 1] != 1:
                new_state[row2][col2], new_state[row2][col2 - 1] = new_state[row2][col2 - 1], new_state[row2][col2]
                if (row2, col2 - 1) not in self.initial_threes:
                    new_state[row2][col2] = 0
                col2 -= 1
                moved = True

        elif direction == 'right':
            # Move tile from (row1, col1) rightwards
            while col1 < GAME_SIZE - 1 and new_state[row1][col1 + 1] != 1:
                new_state[row1][col1], new_state[row1][col1 + 1] = new_state[row1][col1 + 1], new_state[row1][col1]
                if (row1, col1 + 1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                col1 += 1
                moved = True

            # Move tile from (row2, col2) rightwards
            while col2 < GAME_SIZE - 1 and new_state[row2][col2 + 1] != 1:
                new_state[row2][col2], new_state[row2][col2 + 1] = new_state[row2][col2 + 1], new_state[row2][col2]
                if (row2, col2 + 1) not in self.initial_threes:
                    new_state[row2][col2] = 0
                col2 += 1
                moved = True

        return new_state, moved



    def operators_func(self, state):
        successors = []  # List to store successor states

        # Find the position of the '2' tiles
        for row1 in range(len(state)):
            for col1 in range(len(state[0])):
                if state[row1][col1] == 2:
                    for row2 in range(row1, len(state)):
                        for col2 in range(len(state[0])):
                            if state[row2][col2] == 2 and (row1 != row2 or col1 != col2):
                                # Try moving the tile in each direction and add the resulting state to the successors list
                                new_state_up = self.move_tile1(state, 'up', row1, col1, row2, col2)
                                new_state_down = self.move_tile1(state, 'down', row1, col1, row2, col2)
                                new_state_left = self.move_tile1(state, 'left', row1, col1, row2, col2)
                                new_state_right = self.move_tile1(state, 'right', row1, col1, row2, col2)

                                # Add only the valid new states to the successors list
                                if new_state_up:
                                    successors.append((new_state_up, 'up'))

                                if new_state_down:
                                    successors.append((new_state_down, 'down'))

                                if new_state_left:
                                    successors.append((new_state_left, 'left'))

                                if new_state_right:
                                    successors.append((new_state_right, 'right'))

        return successors



    def grid_to_matrix(self):
        matrix = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]

        # Iterate over each tile
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                # Check the type of tile and update the board matrix accordingly
                if (col, row) in self.QUIET_TILES:
                    matrix[row][col] = 1  # Quiet tile
                elif (col, row) in self.MOVABLE_TILES:
                    matrix[row][col] = 2  # Movable tile
                elif (col, row) in self.MATCH_TILES:
                    matrix[row][col] = 3  # Match tile

        return matrix


    def find_threes(self, matrix):
        threes = []
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if val == 3:
                    threes.append((i, j))
        return threes

    
    def solve_puzzle(self):
        # Get the initial state using the grid_to_matrix method
        initial_state_matrix = self.initial_state
        
        # Create a helper function to call move_tile with the correct parameters
        def move_tile_with_direction(direction):
            self.move_tile(direction)

        # Assuming goal_state_func and operators_func are defined somewhere
        solver = Algorithm(initial_state_matrix, self.goal_state_func, self.operators_func, move_tile_with_direction)

        # Call the solving algorithm method
        result_node = solver.breadth_first_search()

        # Apply the solution to the game
        if result_node:
            solution = solver.trace_path(result_node)  # Call trace_path on the solver instance
            self.apply_solution(solution)  # Pass the solution to apply_solution()
        else:
            print("No solution found.")

    def apply_solution(self, solution):
        # Clear the state stack and reset the counter
        self.state_stack.clear()
        self.counter = 0

        # Iterate through the solution path and update the game state
        for state, direction in solution:
            self.state_stack.append(copy.deepcopy(state))
            self.counter += 1
            self.move_tile(direction)  # Move the tile based on the direction

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
        self.quiet_tiles = self.create_gameA()
        self.movable_tiles = self.create_game1A()
        self.match_tiles = self.create_game2A()
        
        self.number_tiles_move = 2
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

        text = "Perfect move: 6 moves"
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
        font = pygame.font.SysFont("Calibri", 36)  # Use default system font, size 36
        text_surface = font.render(text, True, LIGHTBLUE)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 186, self.screen.get_height() // 3 -291))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text

        # Text to display
        text = "Record: 0"
        font = pygame.font.SysFont("Calibri", 36)  # Use default system font, size 36
        text_surface = font.render(text, True, LIGHTBLUE)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 182, self.screen.get_height() // 3 -233))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text
        
        # Text to display
        text = "Perfect: 6"
        font = pygame.font.SysFont("Calibri", 36)  # Use default system font, size 36
        text_surface = font.render(text, True, LIGHTBLUE)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 183, self.screen.get_height() // 3 -175))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text

    def create_gameA(self):
        # Initialize the grid with all tiles set to 0
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        # Define positions where specific tiles should appear

        # Place specific tiles at the defined positions
        for x, y in self.QUIET_TILES:
            grid[y][x] = x + y * GAME_SIZE + 1  # Example: Place tile numbers at specified positions
        return grid
    
    def create_game1A(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]

        for x, y in self.MOVABLE_TILES:
            grid[y][x] = x + y * GAME_SIZE + 1
        return grid
    
    def create_game2A(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]

        
        for x, y in self.MATCH_TILES:
            grid[y][x] = x + y * GAME_SIZE + 1
        return grid
    def create_game(self):
        # Initialize the grid with all tiles set to 0
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        # Define positions where specific tiles should appear

        # Place specific tiles at the defined positions
        for x, y in self.tiles_that_are_quiet:
            grid[y][x] = x + y * GAME_SIZE + 1  # Example: Place tile numbers at specified positions
        return grid
    
    def create_game1(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]

        for x, y in self.tiles_that_move:
            grid[y][x] = x + y * GAME_SIZE + 1
        return grid
    
    def create_game2(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]

        
        for x, y in self.tiles_to_be_matched:
            grid[y][x] = x + y * GAME_SIZE + 1
        return grid
        

    def draw_tiles(self):
        # Define the size and position of the square area where the grid will be drawn
        square_size = min(self.screen.get_width(), self.screen.get_height()) - 50  # Adjust as needed
        square_x = (self.screen.get_width() - square_size) // 2
        square_y = (self.screen.get_height() - square_size) // 2 + 90

        # Calculate the size of each grid cell based on the square size and the game size
        cell_size = square_size // GAME_SIZE

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
                    self.circle_color = PURPLE
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
                    tile_color = PURPLE

                    # Draw the movable tile
                    tile_rect = pygame.Rect(tile_x, tile_y, cell_size - 10, cell_size - 10)  # Adjusted to fit inside the grid lines
                    pygame.draw.rect(self.screen, tile_color, tile_rect)

                    # Check if the movable tile is over a match tile
                    if (col, row) in [(x, y) for y in range(GAME_SIZE) for x in range(GAME_SIZE) if self.match_tiles[y][x] != 0]:
                        
                        # Draw the checkmark symbol
                        # Coordinates for the checkmark lines
                        checkmark_lines = [
                            [(tile_x + 40, tile_y + 75), (tile_x + 77, tile_y + 150)],  # Line 1
                            [(tile_x + 77, tile_y + 150), (tile_x + 137, tile_y + 30)]    # Line 2
                        ]

                        # Draw each line segment with thicker lines (thickness = 10)
                        for line in checkmark_lines:
                            pygame.draw.line(self.screen, SOFTPURPLE, line[0], line[1], 35)
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
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                if self.movable_tiles[row][col] != 0:
                    movable_in_line = True
                    break

        # If there are no movable tiles in the line, return
        if not movable_in_line:
            return

        # Otherwise, perform movement for the entire line in the specified direction
        
        if direction == 'up':
            for col in range(GAME_SIZE):
                for row in range(1, GAME_SIZE):
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
            for col in range(GAME_SIZE):
                for row in range(GAME_SIZE - 2, -1, -1):
                    if self.movable_tiles[row][col] != 0:
                        for k in range(row, GAME_SIZE - 1):
                            if self.movable_tiles[k + 1][col] == 0 and self.quiet_tiles[k + 1][col] == 0:
                                self.movable_tiles[k + 1][col] = self.movable_tiles[k][col]
                                self.movable_tiles[k][col] = 0
                            elif self.movable_tiles[k + 1][col] == self.movable_tiles[k][col]:
                                # Merge the tiles if they have the same value
                                self.movable_tiles[k + 1][col] *= 2
                                self.movable_tiles[k][col] = 0
                                break

        elif direction == 'left':
            for row in range(GAME_SIZE):
                for col in range(1, GAME_SIZE):
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
            for row in range(GAME_SIZE):
                for col in range(GAME_SIZE - 2, -1, -1):
                    if self.movable_tiles[row][col] != 0:
                        for k in range(col, GAME_SIZE - 1):
                            if self.movable_tiles[row][k + 1] == 0 and self.quiet_tiles[row][k + 1] == 0:
                                self.movable_tiles[row][k + 1] = self.movable_tiles[row][k]
                                self.movable_tiles[row][k] = 0
                            elif self.movable_tiles[row][k + 1] == self.movable_tiles[row][k]:
                                # Merge the tiles if they have the same value
                                self.movable_tiles[row][k + 1] *= 2
                                self.movable_tiles[row][k] = 0
                                break

        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
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


    def run(self):
        self.playing = True
        self.grid_to_matrix()
        while self.playing:
            self.events()
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
        cell_size = square_size // GAME_SIZE

        # Set the thickness of the grid lines
        line_thickness = 12  # Adjust as needed

        # Draw horizontal grid lines within the square area
        for row in range(0, GAME_SIZE + 1):
            pygame.draw.line(self.screen, BLUE, (square_x, square_y + row * cell_size),
                            (square_x + square_size, square_y + row * cell_size), line_thickness)

        # Draw vertical grid lines within the square area
        for col in range(0, GAME_SIZE + 1):
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

    
    def events(self):
        
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
                    self.apply_solution(self.initial_state)  # Call the pop_state method to restore the previous game state
                # Handle other mouse button clicks
            elif event.type == pygame.KEYDOWN:
                # Push the current game state onto the stack before handling movement commands
                self.push_state()
                # Handle key presses
                if event.key == pygame.K_UP:
                    initial_state = copy.deepcopy(self.movable_tiles)  # Store initial state of movable tiles
                    self.move_tile('up')
                    
                    # Check if any tile was moved by comparing current and initial state
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.counter += 1
                elif event.key == pygame.K_DOWN:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('down')
                    
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.counter += 1
                elif event.key == pygame.K_LEFT:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('left')
                    
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.counter += 1
                elif event.key == pygame.K_RIGHT:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('right')
                    
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.counter += 1

class TreeNode:
    def __init__(self, state, parent=None, direction=None, heuristic=0, cost=0, g=0, h=0):
        self.state = state
        self.direction = direction
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost  # Added cost attribute
        self.g = g  # Added g attribute
        self.h = h  # Added h attribute
        self.children = []

    def __lt__(self, other):
        return self.cost < other.cost  # Compare using the cost attribute
    
    
    
    
# Define Algorithm class
class Algorithm:
    def __init__(self, initial_state, goal_state_func, operators_func):
        self.initial_state = initial_state
        self.goal_state_func = goal_state_func
        self.operators_func = operators_func

    def trace_path(self, node):
            path = []
            while node:
                path.append((TreeNode.state, TreeNode.direction))  # Store both state and direction as a tuple
                node = TreeNode.parent
            return reversed(path)
    
    @staticmethod
    def cost_func(current_state, successor_state):
        return 1

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

    def breadth_first_search(self):
        root = TreeNode(self.initial_state)
        queue = deque([root])
        
        # Check the type of the initial state
        if not isinstance(self.initial_state, list) or not all(isinstance(row, list) for row in self.initial_state):
            raise ValueError("Initial state must be a list of lists.")
        
        visited = set([tuple(map(tuple, self.initial_state))])  # Convert the initial state to a tuple of tuples

        while queue:
            node = queue.popleft()

            if self.goal_state_func(node.state):
                return node

            for direction in ['up', 'down', 'left', 'right']:
                for state in self.operators_func(node.state, direction):
                    # Ensure state is a list of lists
                    if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                        raise ValueError("State must be a list of lists.")
                    
                    state_tuple = tuple(map(tuple, state))  # Convert the state to a tuple of tuples
                    
                    if state_tuple not in visited:
                        visited.add(state_tuple)  # Add the state tuple to the visited set
                        child_node = TreeNode(state=state, parent=node, direction=direction)
                        node.children.append(child_node)  # Append the child_node to node's children
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

            for state in self.operators_func(node.state):
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

            for state in self.operators_func(node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node)
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

            for state in self.operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    successor_node = TreeNode(state, current_node, heuristic_func(state))
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None
    
    def a_star_search(self, goal_state_func, cost_func, successors_func):
        open_list = []
        initial_node = TreeNode(self.initial_state, g=0, h=self.manhattan_distance(self.initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(tuple(map(tuple, current_node.state)))  # Convert list to tuple and add to closed_list

            for successor in successors_func(current_node.state):
                successor_tuple = tuple(map(tuple, successor))  # Convert list to tuple
                if successor_tuple not in closed_list:
                    g_value = current_node.cost + cost_func(current_node.state, successor)
                    h_value = self.manhattan_distance(successor)
                    successor_node = TreeNode(successor, parent=current_node, cost=g_value + h_value)
                    heapq.heappush(open_list, successor_node)

        return None


    def weighted_a_star_search(self, goal_state_func, heuristic_func, cost_func, successors_func, weight):
        open_list = []
        initial_node = TreeNode(self.initial_state, g=0, h=Algorithm.manhattan_distance(self.initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(tuple(map(tuple, current_node.state)))  # Convert list to tuple and add to closed_list

            for successor in successors_func(current_node.state):
                successor_tuple = tuple(map(tuple, successor))  # Convert list to tuple
                if successor_tuple not in closed_list:
                    g_value = current_node.g + cost_func(current_node.state, successor)
                    h_value = weight * heuristic_func(successor)  # Apply weight to the heuristic value
                    successor_node = TreeNode(successor, parent=current_node, g=g_value, h=h_value)
                    heapq.heappush(open_list, successor_node)

        return None
