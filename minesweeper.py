import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Game variables
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed_cells = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mine_locations = []

# Font for numbers
font = pygame.font.Font(None, 36)

# Load mine and flag images
mine_image = pygame.image.load("mine.png")
mine_image = pygame.transform.scale(mine_image, (CELL_SIZE, CELL_SIZE))
flag_image = pygame.image.load("flag.png")
flag_image = pygame.transform.scale(flag_image, (CELL_SIZE, CELL_SIZE))

# Functions
def initialize_grid():
    global grid, mine_locations

    # Place mines randomly
    mine_locations = random.sample(range(GRID_SIZE**2), GRID_SIZE)
    for index in mine_locations:
        row, col = divmod(index, GRID_SIZE)
        grid[row][col] = -1  # -1 represents a mine

    # Calculate numbers for each cell
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != -1:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if 0 <= row + dr < GRID_SIZE and 0 <= col + dc < GRID_SIZE and grid[row + dr][col + dc] == -1:
                            grid[row][col] += 1

def reveal_cell(row, col):
    global revealed_cells

    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE) or revealed_cells[row][col]:
        return

    revealed_cells[row][col] = True

    if grid[row][col] == 0:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                reveal_cell(row + dr, col + dc)

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            if revealed_cells[row][col]:
                if grid[row][col] == -1:
                    screen.blit(mine_image, rect)
                elif grid[row][col] > 0:
                    number_text = font.render(str(grid[row][col]), True, BLACK)
                    screen.blit(number_text, rect.move(CELL_SIZE // 3, CELL_SIZE // 4))
            else:
                screen.blit(flag_image, rect)

def game_over():
    font_game_over = pygame.font.Font(None, 72)
    text_game_over = font_game_over.render("Game Over", True, RED)
    screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 2 - text_game_over.get_height() // 2))

# Main game loop
initialize_grid()
clock = pygame.time.Clock()
game_running = True
game_won = False

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                row, col = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                if (row, col) in mine_locations:
                    game_over()
                    game_running = False
                else:
                    reveal_cell(row, col)
                    if all(revealed_cells[i][j] or (i, j) in mine_locations for i in range(GRID_SIZE) for j in range(GRID_SIZE)):
                        game_won = True
                        game_running = False
            elif event.button == 3:  # Right mouse button
                row, col = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
                if not revealed_cells[row][col]:
                    revealed_cells[row][col] = True  # Marked cells are revealed on right-click

    screen.fill(GRAY)
    draw_grid()
    pygame.display.flip()
    clock.tick(60)

# Display victory message
if game_won:
    font_victory = pygame.font.Font(None, 72)
    text_victory = font_victory.render("You Win!", True, (0, 128, 0))
    screen.blit(text_victory, (WIDTH // 2 - text_victory.get_width() // 2, HEIGHT // 2 - text_victory.get_height() // 2))
    pygame.display.flip()

# Wait for a key press before quitting
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()
