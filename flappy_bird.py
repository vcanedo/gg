import os
import pygame
import random

# Set SDL_AUDIODRIVER to dummy to suppress ALSA warnings
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
BIRD_SIZE = 20
PIPE_WIDTH = 50

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, BIRD_SIZE, BIRD_SIZE))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.passed = False

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def update(self):
        self.x -= 5

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, BIRD_SIZE, BIRD_SIZE)
        top_pipe_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0

    # Timer for pipe generation
    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

    running = True
    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if event.type == pygame.USEREVENT:
                pipes.append(Pipe(SCREEN_WIDTH))

        bird.update()
        bird.draw(screen)

        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            if pipe.collide(bird):
                running = False
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1

        # Check for collision with ground
        if bird.y + BIRD_SIZE >= SCREEN_HEIGHT:
            running = False

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
