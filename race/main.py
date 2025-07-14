import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SKY, CAR
from road import draw_road

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

# Car state
car_x = 0
car_speed = 200
car_pos = 0

def main():
    global car_x, car_pos
    running = True
    while running:
        screen.fill(SKY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= 30
        if keys[pygame.K_RIGHT]:
            car_x += 30

        car_pos += car_speed

        draw_road(screen, car_x, car_pos)

        pygame.draw.rect(screen, CAR, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 100, 50, 80))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
