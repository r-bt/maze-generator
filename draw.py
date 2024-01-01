import pygame
import sys

# Setup pygame
pygame.init()

# Define some constants

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

# Create the grid

grid = [[WHITE] * COLS for _ in range(ROWS)]

selected = []

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Element Drawer")


def get_black_cells():
    origin_x = min([x for (x, y) in selected])
    origin_y = min([y for (x, y) in selected])

    scaled_black_cells = [(x - origin_x, y - origin_y) for (x, y) in selected]

    return scaled_black_cells


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

            print(get_black_cells())
            sys.exit()
            # Print out the drawing (but rescale it to start at (0,0))

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            grid[clicked_row][clicked_col] = (
                BLACK if grid[clicked_row][clicked_col] == WHITE else WHITE
            )

            if (clicked_col, clicked_row) in selected:
                selected.remove((clicked_col, clicked_row))
            else:
                selected.append((clicked_col, clicked_row))

    # Draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                grid[row][col],
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Draw horizontal grid lines
            pygame.draw.line(
                screen, GREEN, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 1
            )

            # Draw vertical grid lines
            pygame.draw.line(
                screen, GREEN, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), 1
            )

    pygame.display.flip()
