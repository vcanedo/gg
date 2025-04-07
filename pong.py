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

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))

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

# Banter settings
banter_subjects = ["You", "Your paddle", "Your skills", "This game"]
banter_verbs = ["are", "seem", "look"]
banter_adjectives = ["terrible", "slow", "weak", "pathetic", "laughable", "unimpressive", "mediocre"]
banter_endings = ["!", "!!", "!!!", "...", "?"]
ascii_faces = ["(¬‿¬)", "(ಠ_ಠ)", "(¬_¬)", "(¬‿¬)", "(ಠ‿ಠ)"]

banter_interval = 5000  # Time in milliseconds between banter
last_banter_time = pygame.time.get_ticks()

def generate_banter():
    subject = random.choice(banter_subjects)
    verb = random.choice(banter_verbs)
    adjective = random.choice(banter_adjectives)
    ending = random.choice(banter_endings)
    face = random.choice(ascii_faces)
    return f"{subject} {verb} {adjective}{ending} {face}"

def draw_banter():
    banter_text = font.render(generate_banter(), True, WHITE)
    screen.blit(banter_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))

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

def draw_scores():
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 2 + 20, 10))
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (SCREEN_WIDTH // 2 - 50, 10))

def draw_winner(winner):
    winner_text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 37))

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
                if (event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL) or \
                   (event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL):
                    running = False

    if in_menu:
        draw_menu()
    else:
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_paddle.move_up()
            if keys[pygame.K_DOWN]:
                player_paddle.move_down()

            # Opponent AI
            if opponent_paddle.rect.centery < ball.rect.centery:
                opponent_paddle.move_down()
            if opponent_paddle.rect.centery > ball.rect.centery:
                opponent_paddle.move_up()

            ball.move()

            # Ball collision with paddles
            if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
                ball.speed_x *= -1

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

            # Random banter
            current_time = pygame.time.get_ticks()
            if current_time - last_banter_time > banter_interval:
                draw_banter()
                last_banter_time = current_time

        # Drawing
        screen.fill(BLACK)
        player_paddle.draw(screen)
        opponent_paddle.draw(screen)
        ball.draw(screen)
        draw_scores()
        if game_over:
            draw_winner(winner)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
