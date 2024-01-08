import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop It! - Balloon Popping Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (25, 25), 25)
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), HEIGHT))

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.rect.y = HEIGHT
            self.rect.x = random.randint(50, WIDTH-50)

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (10, 10), 10)
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.y -= 10
        if pygame.sprite.spritecollide(self, balloons, True):
            balloons.add(Balloon(random_color()))  # Add a new balloon with a random color when one is popped
            self.kill()
            increase_score()

# Function to generate a random color
def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

# Function to increase the score
def increase_score():
    global score
    score += 1

# Function to display the game over screen
def game_over_screen():
    screen.blit(background, (0, 0))  # Blit the background onto the screen
    font = pygame.font.Font(pixel_font, 36)
    text = font.render("Game Over!", True, YELLOW)  # Change color to yellow
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    score_text = font.render(f"Final Score: {score}", True, YELLOW)  # Change color to yellow
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    pygame.time.delay(3000)  # Display the game over screen for 3 seconds before quitting
    pygame.quit()
    sys.exit()

# Function to display the countdown
def countdown():
    font = pygame.font.Font(pixel_font, 36)
    for i in range(3, 0, -1):
        screen.blit(background, (0, 0))
        countdown_text = font.render(f"Game Starting in {i}...", True, YELLOW)
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

# Load the background image
background = pygame.image.load("1.webp").convert_alpha()

# Create sprite groups
balloons = pygame.sprite.Group()
balls = pygame.sprite.Group()

# Load pixelated font
pixel_font = "PressStart2P.ttf"

# Function to display the welcome message
def display_welcome_message():
    welcome_font = pygame.font.Font(pixel_font, 36)
    welcome_text = welcome_font.render("Welcome to Pop It!", True, YELLOW)
    welcome_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    instructions_font = pygame.font.Font(pixel_font, 18)
    instructions_text1 = instructions_font.render("Click to pop balloons and earn points.", True, YELLOW)
    instructions_text2 = instructions_font.render("Game lasts for 30 seconds. Good luck!", True, YELLOW)

    instructions_rect1 = instructions_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    instructions_rect2 = instructions_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    screen.blit(background, (0, 0))
    screen.blit(welcome_text, welcome_rect)
    screen.blit(instructions_text1, instructions_rect1)
    screen.blit(instructions_text2, instructions_rect2)
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the welcome message for 3 seconds before starting

# Display welcome message
display_welcome_message()

# Display countdown before starting the game
countdown()

# Create initial balloons
for _ in range(5):
    balloons.add(Balloon(random_color()))

# Game variables
score = 0
GAME_DURATION = 30  # in seconds
game_start_time = pygame.time.get_ticks()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls.add(Ball(pygame.mouse.get_pos()))

    # Check game duration
    elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000
    if elapsed_time >= GAME_DURATION:
        game_over_screen()

    screen.blit(background, (0, 0))  # Blit the background onto the screen

    balloons.update()
    balloons.draw(screen)

    balls.update()
    balls.draw(screen)

    # Display timer and score
    timer_font = pygame.font.Font(pixel_font, 14)
    score_font = pygame.font.Font(pixel_font, 14)

    timer_text = timer_font.render(f"Time Left: {GAME_DURATION - elapsed_time}s", True, YELLOW)
    score_text = score_font.render(f"Score: {score}", True, YELLOW)

    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(20)
