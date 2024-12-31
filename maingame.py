import pygame
from pygame.locals import *
import time
import os
import sys
# Set working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# Initializing Pygame
pygame.init()

# Window parameters
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
# Levels can be created in Paint; don't forget to add them to the list on line 29.
# Colors
WHITE = (255, 255, 255)  # Background color
RED = (255, 0, 0)  # Color for hitboxes
BLACK = (0, 0, 0)  # Wall color
TARGET_COLOR = (3, 198, 252)  # Portal
# You can create fake objects by adding +1 to one of the values (e.g., fake walls could be (1,0,0)).
# Player
player_size = 30
player_pos = [47, 47]
player_speed = 5

# Player texture
player_texture = pygame.image.load("Cube.png")
player_texture = pygame.transform.scale(player_texture, (player_size, player_size))

# Setting levels and spawn positions
background_files = [
    ["lvl1.png", (47, 47)],
    ["lvl2.png", (320, 70)],
    ["lvl3.png", (47, 33)]
]
current_background_index = 0
background = pygame.image.load(background_files[current_background_index][0])
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_pixels = pygame.surfarray.array3d(background).transpose(1, 0, 2)

# Collision detection
def can_move(new_pos, dx, dy):
    test_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
    if dx > 0:  # Moving right
        for y in range(test_rect.top, test_rect.bottom):
            if test_rect.right < WIDTH and (background_pixels[y][test_rect.right] == BLACK).all():
                return False
    elif dx < 0:  # Moving left
        for y in range(test_rect.top, test_rect.bottom):
            if test_rect.left > 0 and (background_pixels[y][test_rect.left - 1] == BLACK).all():
                return False
    if dy > 0:  # Moving down
        for x in range(test_rect.left, test_rect.right):
            if test_rect.bottom < HEIGHT and (background_pixels[test_rect.bottom][x] == BLACK).all():
                return False
    elif dy < 0:  # Moving up
        for x in range(test_rect.left, test_rect.right):
            if test_rect.top > 0 and (background_pixels[test_rect.top - 1][x] == BLACK).all():
                return False
    return True

# Smooth movement function
def smooth_move(screen, start_pos, end_pos, texture, background, size):
    steps = 10  # Number of frames for animation
    for i in range(1, steps + 1):
        interpolated_x = start_pos[0] + (end_pos[0] - start_pos[0]) * i / steps
        interpolated_y = start_pos[1] + (end_pos[1] - start_pos[1]) * i / steps
        screen.blit(background, (0, 0))
        scaled_texture = pygame.transform.scale(texture, (size, size))
        screen.blit(scaled_texture, (interpolated_x, interpolated_y))
        pygame.display.flip()
        time.sleep(0.01)  # Delay for smoothness

# Function to switch backgrounds
def switch_background():
    global current_background_index, background, background_pixels, player_pos
    current_background_index = (current_background_index + 1) % len(background_files)
    background_file, new_position = background_files[current_background_index]
    background = pygame.image.load(background_file)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_pixels = pygame.surfarray.array3d(background).transpose(1, 0, 2)
    player_pos[0], player_pos[1] = new_position

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Handling key presses
    keys = pygame.key.get_pressed()
    move_direction = None

    if keys[K_w]:
        move_direction = (0, -1)
    elif keys[K_s]:
        move_direction = (0, 1)
    elif keys[K_a]:
        move_direction = (-1, 0)
    elif keys[K_d]:
        move_direction = (1, 0)

    if move_direction:
        dx, dy = move_direction
        start_pos = player_pos[:]
        while True:
            new_pos = [player_pos[0] + dx, player_pos[1] + dy]
            if not (0 <= new_pos[0] < WIDTH and 0 <= new_pos[1] < HEIGHT):
                break
            if not can_move(player_pos, dx, dy):
                break

            # Checking for target color
            color_at_new_pos = background_pixels[player_pos[1] + dy][player_pos[0] + dx]
            if (color_at_new_pos == TARGET_COLOR).all():
                switch_background()
                break

            player_pos[0] += dx
            player_pos[1] += dy
        smooth_move(screen, start_pos, player_pos, player_texture, background, player_size)

    # Rendering
    screen.blit(background, (0, 0))

    # Drawing the player
    scaled_texture = pygame.transform.scale(player_texture, (player_size, player_size))
    screen.blit(scaled_texture, player_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
