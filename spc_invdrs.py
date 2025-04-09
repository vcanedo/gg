import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player setup
player_width = 50
player_height = 30
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Enemy setup
enemy_width = 40
enemy_height = 30
enemy_speed = 2
enemies = [{"x": random.randint(0, SCREEN_WIDTH - enemy_width), "y": random.randint(50, 150)} for _ in range(5)]

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    # Enemy movement and drawing
    for enemy in enemies:
        enemy["y"] += enemy_speed
        if enemy["y"] > SCREEN_HEIGHT:
            enemy["y"] = random.randint(50, 150)
            enemy["x"] = random.randint(0, SCREEN_WIDTH - enemy_width)
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy_width, enemy_height))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
