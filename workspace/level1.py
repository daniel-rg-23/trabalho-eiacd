import pygame
from seti.sets import *
from opening_page import *
import copy


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
    




class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.overlay_alpha = 128  # Adjust the transparency level (0-255)
        self.overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, self.overlay_alpha))
        self.checkmarks_appeared = False
        self.all_sprites = pygame.sprite.Group()
        self.tiles = []     
        self.quiet_tiles = self.create_game()
        self.movable_tiles = self.create_game1()
        self.match_tiles = self.create_game2()
        self.number_tiles_move = 2
        self.counter = 0
        self.home = pygame.Rect((WIDTH - 96) // 2 -150,(HEIGHT - 96) // 2 +110, 100, 100)
        self.next = pygame.Rect((WIDTH - 96) // 2 ,(HEIGHT - 96) // 2 +110, 100, 100)
        self.resart2 = pygame.Rect((WIDTH - 96) // 2 +150,(HEIGHT - 96) // 2 +110, 100, 100)
        self.resart = pygame.Rect((WIDTH - 96) // 2 - 55,(HEIGHT - 96) // 2 -348, 96, 96)
        self.undo = pygame.Rect((WIDTH - 96) // 2 - 188,(HEIGHT - 96) // 2 - 348, 96, 96)
        self.heuristic=pygame.Rect((WIDTH - 96) // 2 - 322,(HEIGHT - 96) // 2 - 348, 96, 96)
        self.state_stack = []  # Stack to store game states
        self.push_state()
        
    def push_state(self):
        # Push the current state of the game board onto the stack
        self.state_stack.append((copy.deepcopy(self.quiet_tiles), copy.deepcopy(self.movable_tiles), copy.deepcopy(self.match_tiles), self.counter))

    def pop_state(self):
    # Pop the last state from the stack and set the game board to that state
        if self.state_stack:
            prev_state = self.state_stack.pop()
            self.quiet_tiles, self.movable_tiles, self.match_tiles, self.counter = prev_state
            self.draw()  # Redraw the screen after undoing the move
            return prev_state  # Return the popped state
        else:
            print("No moves to undo.")


    def reset_level(self):
        # Reset all game variables to their initial state
        self.quiet_tiles = self.create_game()
        self.movable_tiles = self.create_game1()
        self.match_tiles = self.create_game2()
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
        pygame.draw.rect(self.screen, BLUE, self.next)
        pygame.draw.rect(self.screen, BLUE, self.resart2)

        # Text to display
        text = "Puzzle solved"
        font = pygame.font.SysFont("Calibri", 80, bold=True)  # Use default system font, size 36
        text_surface = font.render(text, True, BLUEGREEN)  # Render text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3 + 15))  # Center the text
        self.screen.blit(text_surface, text_rect)  # Draw text

        text = "You solved this puzzle in 7 moves"
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
        
        image_rect = self.heuristic  # Assuming self.heuristic is a pygame.Rect object
        image = pygame.image.load("lampada.png").convert_alpha()
        resized_image = pygame.transform.scale(image, (50, 50))  # Load your image
        self.screen.blit(resized_image, image_rect)
        

        pygame.draw.rect(self.screen, BLUE, self.heuristic)
        
        pygame.draw.rect(self.screen, BLUE, self.undo)
        
        pygame.draw.rect(self.screen, BLUE, self.resart)



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


    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        # Initialize the grid with all tiles set to 0
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        # Define positions where specific tiles should appear
        quiet_tiles = [(0, 0), (2, 1), (2, 3),(1,3)]  # Example positions
        # Place specific tiles at the defined positions
        for x, y in quiet_tiles:
            grid[y][x] = x + y * GAME_SIZE + 1  # Example: Place tile numbers at specified positions
        return grid
    
    def create_game1(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        tiles_that_move = [(3,2),(1,2)]
        for x, y in tiles_that_move:
            grid[y][x] = x + y * GAME_SIZE + 1
        return grid
    
    def create_game2(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        tiles_to_be_matched = [(0,1),(0,2)]
        
        for x, y in tiles_to_be_matched:
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
                        self.pop_state()
                        return
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    initial_state = copy.deepcopy(self.movable_tiles)  # Store initial state of movable tiles
                    self.move_tile('up')
                    # Check if any tile was moved by comparing current and initial state
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.push_state()  # Push state if tiles were moved
                        self.counter += 1

                elif event.key == pygame.K_DOWN:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('down')
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.push_state()  # Push state if tiles were moved
                        self.counter += 1

                elif event.key == pygame.K_LEFT:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('left')
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.push_state()  # Push state if tiles were moved
                        self.counter += 1
                elif event.key == pygame.K_RIGHT:
                    initial_state = copy.deepcopy(self.movable_tiles)
                    self.move_tile('right')
                    if any(self.movable_tiles[row][col] != initial_state[row][col] for row in range(GAME_SIZE) for col in range(GAME_SIZE)):
                        self.push_state()  # Push state if tiles were moved
                        self.counter += 1
      

        