# Python
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Game")
clock = pygame.time.Clock()

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create platforms
platform = Platform(200, 500, 100, 20)
platforms.add(platform)
all_sprites.add(platform)

# Create enemies
enemy = Enemy(400, 500, 50, 50)
enemies.add(enemy)
all_sprites.add(enemy)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            elif event.key == pygame.K_RIGHT:
                player.go_right()
            elif event.key == pygame.K_SPACE:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            elif event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()

    # Update
    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Maintain FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()
