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

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Ball dimensions
BALL_SIZE = 14

# Speeds
PADDLE_SPEED = 6
BALL_SPEED_X = 6
BALL_SPEED_Y = 6

# Difficulty settings
DIFFICULTY_LEVELS = {
    'easy': 3,
    'medium': 6,
    'hard': 9
}
difficulty = 'medium'  # Change this to 'easy', 'medium', or 'hard' to set difficulty

# Create the screen
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
        self.touches = 0  # Track the number of touches
        self.color = WHITE  # Initial color of the ball
        self.target_color = WHITE  # Target color for gradual redness
        self.size_increase = 0  # Track size increase
        self.target_size_increase = 0  # Target size increase for gradual growth

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Gradually adjust color towards target color
        r = min(255, self.color[0] + (self.target_color[0] - self.color[0]) // 10)
        g = max(0, self.color[1] + (self.target_color[1] - self.color[1]) // 10)
        b = max(0, self.color[2] + (self.target_color[2] - self.color[2]) // 10)
        self.color = (r, g, b)

        # Gradually adjust size towards target size
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
        self.touches = 0  # Reset touches
        self.color = WHITE  # Reset color
        self.target_color = WHITE  # Reset target color
        self.size_increase = 0  # Reset size
        self.target_size_increase = 0  # Reset target size
        self.rect.width = BALL_SIZE
        self.rect.height = BALL_SIZE

    def increase_speed(self):
        multiplier = {'easy': 1.05, 'medium': 1.1, 'hard': 1.2}[difficulty]
        self.speed_x *= multiplier
        self.speed_y *= multiplier

        # Set target redness
        red_value = min(255, self.target_color[0] + 20)  # Cap at 255
        self.target_color = (red_value, 255 - red_value, 255 - red_value)

        # Set target size increase
        self.target_size_increase += 4

# Initialize paddles and ball
player_paddle = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, DIFFICULTY_LEVELS[difficulty])
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

# Initialize scores
player_score = 0
opponent_score = 0

# Font for displaying scores
font = pygame.font.Font(None, 74)

# Winning score
WINNING_SCORE = 10

# Menu settings
menu_font = pygame.font.Font(None, 74)
menu_items = ['Easy', 'Medium', 'Hard']
selected_item = 1  # Default to 'Medium'

def draw_menu():
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        color = WHITE if index == selected_item else (100, 100, 100)
        menu_text = menu_font.render(item, True, color)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100 + index * 100))
    pygame.display.flip()

# Main game loop
running = True
game_over = False
in_menu = True
clock = pygame.time.Clock()
countdown = 3  # Countdown starts at 3
countdown_start_time = None

def draw_scores():
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 2 + 20, 10))
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (SCREEN_WIDTH // 2 - 50, 10))

def draw_winner(winner):
    winner_text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 37))

def draw_countdown(count):
    countdown_font = pygame.font.Font(None, SCREEN_HEIGHT)  # Large font for countdown
    countdown_text = str(count) if count > 0 else "GO"
    opacity = 128 if count > 0 else 28  # Countdown is semi-opaque, "GO" is fully opaque
    countdown_surface = countdown_font.render(countdown_text, True, (255, 255, 255))
    countdown_surface.set_alpha(opacity)  # Set opacity based on the text
    countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(countdown_surface, countdown_rect)

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
            else:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    in_menu = True  # Return to menu
                elif (event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL) or \
                     (event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL):
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
            # Allow the game to start while "GO" is displayed
            if countdown == 0 and pygame.time.get_ticks() - countdown_start_time < 2000:
                draw_countdown(countdown)  # Display "GO" in the background

            if not game_over:
                keys = pygame.key.get_pressed()
                # Player paddle controls
                if keys[pygame.K_UP]:
                    player_paddle.move_up()
                if keys[pygame.K_DOWN]:
                    player_paddle.move_down()

                # Fixed Opponent AI
                if ball.speed_x < 0:  # Only predict when the ball is moving toward the opponent
                    future_ball_y = ball.rect.y + (ball.speed_y * abs(opponent_paddle.rect.x - ball.rect.x) // abs(ball.speed_x))
                    if future_ball_y < 0:  # Handle top wall bounce
                        future_ball_y = -future_ball_y
                    elif future_ball_y > SCREEN_HEIGHT:  # Handle bottom wall bounce
                        future_ball_y = SCREEN_HEIGHT - (future_ball_y - SCREEN_HEIGHT)
                else:
                    future_ball_y = ball.rect.centery  # Stay centered when the ball is moving away

                if opponent_paddle.rect.centery < future_ball_y:
                    opponent_paddle.move_down()
                elif opponent_paddle.rect.centery > future_ball_y:
                    opponent_paddle.move_up()

                ball.move()

                # Ball collision with paddles
                if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
                    ball.speed_x *= -1
                    ball.touches += 1
                    if ball.touches % 5 == 0:  # Increase speed every 5 touches
                        ball.increase_speed()

                # Ball out of bounds
                if ball.rect.left <= 0:
                    player_score += 1
                    ball.reset()
                if ball.rect.right >= SCREEN_WIDTH:
                    opponent_score += 1
                    ball.reset()

                # Check for winner
                if player_score >= WINNING_SCORE:
                    game_over = True
                    winner = "Player"
                elif opponent_score >= WINNING_SCORE:
                    game_over = True
                    winner = "Opponent"

            # Drawing
            screen.fill(BLACK)
            if countdown == 0 and pygame.time.get_ticks() - countdown_start_time < 2000:
                draw_countdown(countdown)  # Keep displaying "GO" for 2 seconds
            player_paddle.draw(screen)
            opponent_paddle.draw(screen)
            ball.draw(screen)
            draw_scores()
            if game_over:
                draw_winner(winner)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
