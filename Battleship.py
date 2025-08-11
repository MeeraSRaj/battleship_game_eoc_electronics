import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE * 2 + 100
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# Ship sizes
SHIPS = [(1, 5), (1, 4), (1, 3), (1, 2), (1, 2)]

# Load assets with error handling
try:
    hit_img = pygame.image.load("explosion.png")
    miss_img = pygame.image.load("splash.png")
    hit_sound = pygame.mixer.Sound("explosion.wav")
    miss_sound = pygame.mixer.Sound("splash.wav")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    sys.exit(1)

# Scale images
hit_img = pygame.transform.scale(hit_img, (CELL_SIZE, CELL_SIZE))
miss_img = pygame.transform.scale(miss_img, (CELL_SIZE, CELL_SIZE))

# Screen setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")
title_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Player:
    def __init__(self, x_offset, name):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.attack_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ships = []
        self.x_offset = x_offset
        self.name = name

    def draw_grid(self, hide_ships=False):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(self.x_offset + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLUE if self.grid[y][x] and not hide_ships else GRAY, rect, 1)
                if self.attack_grid[y][x] == 1:  # Miss
                    screen.blit(miss_img, rect.topleft)
                elif self.attack_grid[y][x] == 2:  # Hit
                    screen.blit(hit_img, rect.topleft)

    def place_ship(self, ship, pos, horizontal):
        x, y = pos
        width, height = ship if horizontal else (ship[1], ship[0])
        if x + width > GRID_SIZE or y + height > GRID_SIZE:
            return False
        for i in range(height):
            for j in range(width):
                if self.grid[y + i][x + j] != 0:
                    return False
        for i in range(height):
            for j in range(width):
                self.grid[y + i][x + j] = 1
        self.ships.append((x, y, width, height))
        return True

    def check_hit(self, x, y):
        if self.grid[y][x] == 1:
            self.attack_grid[y][x] = 2  # Hit
            self.grid[y][x] = 2
            hit_sound.play()
            return True
        elif self.attack_grid[y][x] == 0:
            self.attack_grid[y][x] = 1  # Miss
            miss_sound.play()
        return False

    def all_sunk(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 1:
                    return False
        return True

def draw_ship_preview(pos, ship, horizontal, player):
    x, y = pos
    grid_x = (x - player.x_offset) // CELL_SIZE
    grid_y = y // CELL_SIZE
    width, height = ship if horizontal else (ship[1], ship[0])
    valid = (0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE and
             grid_x + width <= GRID_SIZE and grid_y + height <= GRID_SIZE)
    if valid:
        for i in range(height):
            for j in range(width):
                if player.grid[grid_y + i][grid_x + j] != 0:
                    valid = False
                    break
    color = GREEN if valid else RED
    rect = pygame.Rect(x, y, width * CELL_SIZE, height * CELL_SIZE)
    pygame.draw.rect(screen, color, rect, 2)

def draw_button(text, x, y, width, height, color, hover_color, text_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    current_color = hover_color if button_rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, current_color, button_rect, 0, 10)
    pygame.draw.rect(screen, BLACK, button_rect, 2, 10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def show_instructions():
    screen.fill(DARK_BLUE)
    pygame.draw.rect(screen, LIGHT_GRAY, (30, 30, WINDOW_WIDTH-60, WINDOW_HEIGHT-60), 0, 10)
    
    title = title_font.render("Battleship Instructions", True, BLACK)
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
    
    instructions = [
        "Welcome to Battleship!",
        "1. Ship Placement:",
        "   - Each player gets 5 ships (5, 4, 3, 2, 2)",
        "   - Click and drag to place",
        "   - Press 'R' to rotate ships",
        "   - Other player: Don't look!",
        "2. Gameplay:",
        "   - Take turns attacking opponent's grid",
        "   - Hit = Attack again, Miss = Switch turns",
        "   - Explosion = Hit   Splash = Miss",
        "3. Objective:",
        "   - Sink all enemy ships to win!"
    ]
    
    y_offset = 120
    for line in instructions:
        text = small_font.render(line, True, BLACK)
        screen.blit(text, (70, y_offset))
        y_offset += 35
    
    back_button = draw_button("Back", WINDOW_WIDTH//2-75, WINDOW_HEIGHT-100, 150, 50, BLUE, LIGHT_GRAY, WHITE)
    
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    waiting = False

def get_player_name(player_num):
    screen.fill(DARK_BLUE)
    pygame.draw.rect(screen, LIGHT_GRAY, (30, 30, WINDOW_WIDTH-60, WINDOW_HEIGHT-60), 0, 10)
    
    prompt = font.render(f"Enter Player {player_num} Name:", True, BLACK)
    screen.blit(prompt, (WINDOW_WIDTH//2 - prompt.get_width()//2, 150))
    
    name = ""
    input_active = True
    input_box = pygame.Rect(WINDOW_WIDTH//2 - 150, 220, 300, 50)
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalnum() and len(name) < 15:
                    name += event.unicode
        
        screen.fill(DARK_BLUE)
        pygame.draw.rect(screen, LIGHT_GRAY, (30, 30, WINDOW_WIDTH-60, WINDOW_HEIGHT-60), 0, 10)
        screen.blit(prompt, (WINDOW_WIDTH//2 - prompt.get_width()//2, 150))
        
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        name_surface = font.render(name, True, BLACK)
        screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))
        
        continue_button = draw_button("Continue", WINDOW_WIDTH//2-75, 300, 150, 50, BLUE, LIGHT_GRAY, WHITE)
        
        pygame.display.flip()
        
        if not input_active:
            break
        elif pygame.mouse.get_pressed()[0] and continue_button.collidepoint(pygame.mouse.get_pos()) and name.strip():
            input_active = False
    
    return name.strip() or f"Player {player_num}"

def show_welcome_screen():
    screen.fill(DARK_BLUE)
    pygame.draw.rect(screen, LIGHT_GRAY, (30, 30, WINDOW_WIDTH-60, WINDOW_HEIGHT-60), 0, 10)
    
    title = title_font.render("Battleship", True, YELLOW)
    subtitle = small_font.render("Prepare for naval combat!", True, BLACK)
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
    screen.blit(subtitle, (WINDOW_WIDTH//2 - subtitle.get_width()//2, 160))
    
    start_button = draw_button("Start Game", WINDOW_WIDTH//2-100, 250, 200, 60, BLUE, LIGHT_GRAY, WHITE)
    instr_button = draw_button("Instructions", WINDOW_WIDTH//2-100, 340, 200, 60, BLUE, LIGHT_GRAY, WHITE)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return True
                if instr_button.collidepoint(event.pos):
                    show_instructions()
                    return False
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    
    while True:  # Outer loop for restarting game
        # Show welcome screen
        if not show_welcome_screen():
            show_welcome_screen()
        
        # Get player names
        player1_name = get_player_name(1)
        player2_name = get_player_name(2)
        
        # Initialize players and game state
        player1 = Player(50, player1_name)
        player2 = Player(50 + GRID_SIZE * CELL_SIZE + 50, player2_name)
        current_player = player1
        placing_ships = True
        current_ship_idx = 0
        dragging = False
        horizontal = True
        game_over = False
        play_again_button = None
        quit_button = None

        # Main game loop
        while not game_over:
            screen.fill(WHITE)
            
            # Draw quit button during gameplay
            quit_button = draw_button("Quit", WINDOW_WIDTH - 150, WINDOW_HEIGHT - 70, 100, 40, RED, LIGHT_GRAY, WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and placing_ships:
                        horizontal = not horizontal
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if placing_ships:
                        x, y = event.pos
                        grid_x = (x - current_player.x_offset) // CELL_SIZE
                        grid_y = y // CELL_SIZE
                        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                            dragging = True
                    elif not game_over:
                        x, y = event.pos
                        target_player = player2 if current_player == player1 else player1
                        grid_x = (x - target_player.x_offset) // CELL_SIZE
                        grid_y = y // CELL_SIZE
                        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                            if target_player.attack_grid[grid_y][grid_x] == 0:  # Only proceed if cell is unattacked
                                is_hit = target_player.check_hit(grid_x, grid_y)
                                if is_hit:
                                    if target_player.all_sunk():
                                        game_over = True
                                else:
                                    current_player = player2 if current_player == player1 else player1
                            else:
                                invalid_text = font.render("Already attacked! Try again.", True, RED)
                                screen.blit(invalid_text, (WINDOW_WIDTH // 2 - invalid_text.get_width() // 2, WINDOW_HEIGHT - 80))
                                pygame.display.flip()
                                pygame.time.wait(500)
                if event.type == pygame.MOUSEBUTTONUP and placing_ships and dragging:
                    x, y = event.pos
                    grid_x = (x - current_player.x_offset) // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        if current_player.place_ship(SHIPS[current_ship_idx], (grid_x, grid_y), horizontal):
                            current_ship_idx += 1
                            if current_ship_idx >= len(SHIPS):
                                current_ship_idx = 0
                                current_player = player2 if current_player == player1 else player1
                                if current_player == player1:
                                    placing_ships = False
                    dragging = False

            # Draw grids
            if placing_ships:
                current_player.draw_grid(False)
                other_player = player2 if current_player == player1 else player1
                warning_text = font.render(f"{other_player.name}: Please look away!", True, RED)
                screen.blit(warning_text, (WINDOW_WIDTH // 2 - warning_text.get_width() // 2, WINDOW_HEIGHT - 80))
            else:
                player1.draw_grid(True)
                player2.draw_grid(True)

            # Draw UI
            if placing_ships:
                text = font.render(f"{current_player.name} placing ships", True, BLACK)
                screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT - 50))
                if current_ship_idx < len(SHIPS):
                    x, y = pygame.mouse.get_pos()
                    draw_ship_preview((x, y), SHIPS[current_ship_idx], horizontal, current_player)
            else:
                text = font.render(f"{current_player.name}'s turn to launch", True, BLACK)
                screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT - 50))

            pygame.display.flip()
            clock.tick(60)

        # Game over loop
        while game_over:
            screen.fill(WHITE)
            player1.draw_grid(True)  # Show both grids without ships hidden
            player2.draw_grid(True)
            
            winner = current_player
            win_text = font.render(f"{winner.name} wins!", True, BLACK)
            screen.blit(win_text, (WINDOW_WIDTH // 2 - win_text.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
            play_again_button = draw_button("Play Again", WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT // 2 + 20, 150, 50, BLUE, LIGHT_GRAY, WHITE)
            quit_button = draw_button("Quit", WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT // 2 + 20, 150, 50, RED, LIGHT_GRAY, WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button and play_again_button.collidepoint(event.pos):
                        game_over = False
                        break
                    if quit_button and quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()
