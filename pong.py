import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and ball dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 14

# Speeds
PADDLE_SPEED = 6
BALL_SPEED_X = 6
BALL_SPEED_Y = 6

# Difficulty settings
DIFFICULTY_LEVELS = {'easy': 3, 'medium': 6, 'hard': 9}
difficulty = 'medium'

reaction_delay_map = {'easy': 300, 'medium': 150, 'hard': 60}
error_margin_map = {'easy': 60, 'medium': 30, 'hard': 10}

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Paddle class
class Paddle:
    def __init__(self, x, y, speed=PADDLE_SPEED):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = speed

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        self.touches = 0
        self.color = WHITE
        self.target_color = WHITE
        self.size_increase = 0
        self.target_size_increase = 0

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        r = min(255, self.color[0] + (self.target_color[0] - self.color[0]) // 10)
        g = max(0, self.color[1] + (self.target_color[1] - self.color[1]) // 10)
        b = max(0, self.color[2] + (self.target_color[2] - self.color[2]) // 10)
        self.color = (r, g, b)

        if self.size_increase < self.target_size_increase:
            self.size_increase += 0.2
            self.rect.inflate_ip(0.2, 0.2)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        self.touches = 0
        self.color = WHITE
        self.target_color = WHITE
        self.size_increase = 0
        self.target_size_increase = 0
        self.rect.width = BALL_SIZE
        self.rect.height = BALL_SIZE

    def increase_speed(self):
        multiplier = {'easy': 1.05, 'medium': 1.1, 'hard': 1.2}[difficulty]
        self.speed_x *= multiplier
        self.speed_y *= multiplier
        red_value = min(255, self.target_color[0] + 20)
        self.target_color = (red_value, 255 - red_value, 255 - red_value)
        self.target_size_increase += 4

# Initialize objects
player_paddle = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, DIFFICULTY_LEVELS[difficulty])
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

# Scores
player_score = 0
opponent_score = 0
WINNING_SCORE = 10
font = pygame.font.Font(None, 74)

# Menu setup
menu_font = pygame.font.Font(None, 74)
menu_items = ['Easy', 'Medium', 'Hard']
selected_item = 1
in_menu = True

# Draw menu
def draw_menu():
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        color = WHITE if index == selected_item else (100, 100, 100)
        text = menu_font.render(item, True, color)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100 + index * 100))
    pygame.display.flip()

# Draw UI
def draw_scores():
    screen.blit(font.render(str(player_score), True, WHITE), (SCREEN_WIDTH // 2 + 20, 10))
    screen.blit(font.render(str(opponent_score), True, WHITE), (SCREEN_WIDTH // 2 - 50, 10))

def draw_winner(winner):
    text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 37))

def draw_countdown(count):
    countdown_font = pygame.font.Font(None, SCREEN_HEIGHT)
    countdown_text = str(count) if count > 0 else "GO"
    opacity = 128 if count > 0 else 28
    surf = countdown_font.render(countdown_text, True, WHITE)
    surf.set_alpha(opacity)
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(surf, rect)

# Game loop variables
running = True
game_over = False
clock = pygame.time.Clock()
countdown = 3
countdown_start_time = None
last_ai_update = 0

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if in_menu:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    difficulty = menu_items[selected_item].lower()
                    opponent_paddle.speed = DIFFICULTY_LEVELS[difficulty]
                    in_menu = False
                    countdown = 3
                    countdown_start_time = None
                    player_score = 0
                    opponent_score = 0
                    game_over = False
            else:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    in_menu = True
                elif event.key in (pygame.K_q, pygame.K_d) and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    running = False

    if in_menu:
        draw_menu()
    else:
        if countdown > 0:
            if countdown_start_time is None:
                countdown_start_time = pygame.time.get_ticks()
            elapsed_time = (pygame.time.get_ticks() - countdown_start_time) // 1000
            if elapsed_time >= 1:
                countdown -= 1
                countdown_start_time = pygame.time.get_ticks()
            screen.fill(BLACK)
            draw_countdown(countdown)
        else:
            if countdown == 0 and pygame.time.get_ticks() - countdown_start_time < 2000:
                draw_countdown(countdown)

            if not game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    player_paddle.move_up()
                if keys[pygame.K_DOWN]:
                    player_paddle.move_down()

                # Ensure predicted_y is defined for first-time use
                if 'predicted_y' not in locals():
                    predicted_y = SCREEN_HEIGHT // 2

                # Update AI target position at interval
                current_time = pygame.time.get_ticks()
                if current_time - last_ai_update >= reaction_delay_map[difficulty]:
                    last_ai_update = current_time

                    if ball.speed_x < 0:
                        future_y = ball.rect.y + (ball.speed_y * abs(opponent_paddle.rect.x - ball.rect.x) // abs(ball.speed_x))
                        if future_y < 0:
                            future_y = -future_y
                        elif future_y > SCREEN_HEIGHT:
                            future_y = SCREEN_HEIGHT - (future_y - SCREEN_HEIGHT)
                    else:
                        future_y = ball.rect.centery

                    predicted_y = future_y + random.randint(-error_margin_map[difficulty], error_margin_map[difficulty])

                # Move every frame toward the last predicted target
                if opponent_paddle.rect.centery < predicted_y - 10:
                    opponent_paddle.move_down()
                elif opponent_paddle.rect.centery > predicted_y + 10:
                    opponent_paddle.move_up()

                ball.move()

                if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
                    ball.speed_x *= -1
                    ball.touches += 1
                    if ball.touches % 5 == 0:
                        ball.increase_speed()

                if ball.rect.left <= 0:
                    player_score += 1
                    ball.reset()
                if ball.rect.right >= SCREEN_WIDTH:
                    opponent_score += 1
                    ball.reset()

                if player_score >= WINNING_SCORE:
                    game_over = True
                    winner = "Player"
                elif opponent_score >= WINNING_SCORE:
                    game_over = True
                    winner = "Opponent"

            screen.fill(BLACK)
            if countdown == 0 and pygame.time.get_ticks() - countdown_start_time < 2000:
                draw_countdown(countdown)
            player_paddle.draw(screen)
            opponent_paddle.draw(screen)
            ball.draw(screen)
            draw_scores()
            if game_over:
                draw_winner(winner)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
