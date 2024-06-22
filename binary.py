import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer for audio
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 23
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (250, 255, 120)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CONFETTI_COLORS = [(55, 0, 0), (0, 255, 150), (0, 0, 255), (255, 255, 150), (50, 40, 55), (0, 55, 255)]
MODAL_BORDER_RADIUS = 20

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Binary Search Number Guessing Game")

# Fonts
font = pygame.font.SysFont("Georgia", FONT_SIZE)
large_font = pygame.font.SysFont("Arial", 38)
modal_font = pygame.font.SysFont("Arial", 24)

# Load sound effects
correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")

# Game variables
low = 1
high = 5
target = random.randint(low, high)
attempts = 0
guess = None
name = ''
message = ''
message_color = WHITE
game_active = False
confetti_particles = []

# Modal variables
modal_active = False
start_time = time.time()

# Input box
input_box = pygame.Rect(270, 250, 250, 40)
color_inactive = pygame.Color('pink')
color_active = pygame.Color('dodgerblue2')
text_color = WHITE
color = color_inactive
active = False
text = ''
done = False
name_placeholder_text = "Type your name here..."
guess_placeholder_text = "Type your guess here..."

# Cursor variables
cursor_visible = True
cursor_timer = 0
CURSOR_BLINK_TIME = 500  # milliseconds

# Functions for confetti
def create_confetti():
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(-SCREEN_HEIGHT, 0)  # Start confetti particles off-screen
        speed = random.randint(2, 6)
        color = random.choice(CONFETTI_COLORS)
        confetti_particles.append([x, y, speed, color])

def draw_confetti():
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle[3], (particle[0], particle[1]), 5)
        particle[1] += particle[2]
        if particle[1] > SCREEN_HEIGHT:
            particle[1] = random.randint(-SCREEN_HEIGHT, 0)  # Reset particle above the screen

# Welcome screen loop
while not game_active:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game_active = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    name = text
                    message = f'Welcome, {name}! \n Try to guess the number between {low} and {high}.'
                    message_color = BLACK
                    text = ''
                    game_active = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    
    screen.fill(BLACK)
    welcome_message = large_font.render("Enter your name", True, GREEN)
    screen.blit(welcome_message, (250, 150))

    if text == '':
        display_text = name_placeholder_text
        text_color = (100, 100, 100)  # Gray color for placeholder
    else:
        display_text = text
        text_color = WHITE

    # Add cursor to the end of the text if it's visible
    if cursor_visible and active:
        display_text += '|'

    txt_surface = font.render(display_text, True, text_color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    # Blink the cursor
    if current_time - cursor_timer > CURSOR_BLINK_TIME:
        cursor_visible = not cursor_visible
        cursor_timer = current_time

    pygame.display.flip()

# Game loop
correct = False
while not done:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    try:
                        guess = int(text)
                        attempts += 1
                        if guess < target:
                            message = "Too low! Try again:"
                            message_color = RED
                            wrong_sound.play()
                        elif guess > target:
                            message = "Too high! Try again:"
                            message_color = RED
                            wrong_sound.play()
                        else:
                            message = f"Correct, {name}! The number was {target}. Attempts: {attempts}"
                            message_color = GREEN
                            correct = True
                            create_confetti()
                            modal_active = True  # Activate modal on correct guess
                            correct_sound.play()
                        text = ''
                    except ValueError:
                        message = "Please enter a valid number."
                        message_color = RED
                        wrong_sound.play()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    
    screen.fill(BLACK)
    txt_surface = font.render(message, True, GREEN)
    screen.blit(txt_surface, (50, 90))

    if not modal_active:
        if text == '':
            display_text = guess_placeholder_text
            text_color = (100, 100, 100)  # Gray color for placeholder
        else:
            display_text = text
            text_color = WHITE

        # Add cursor to the end of the text if it's visible
        if cursor_visible and active:
            display_text += '|'

        txt_surface = font.render(display_text, True, text_color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Blink the cursor
        if current_time - cursor_timer > CURSOR_BLINK_TIME:
            cursor_visible = not cursor_visible
            cursor_timer = current_time

    if correct:
        draw_confetti()

    if modal_active:
        # Draw modal background with rounded corners
        modal_rect = pygame.Rect(170, 155, 460, 290)
        pygame.draw.rect(screen, GREEN, modal_rect, border_radius=MODAL_BORDER_RADIUS)

        # Draw modal content
        modal_text = modal_font.render(f"Thank you for playing, {name}!", True, BLACK)
        screen.blit(modal_text, (220, 205))
        
        # Calculate and display game duration
        end_time = time.time()
        game_duration = round(end_time - start_time, 2)
        modal_duration = modal_font.render(f"Game duration: {game_duration} seconds", True, BLACK)
        screen.blit(modal_duration, (220, 245))

    pygame.display.flip()

    if correct:
        pygame.time.wait(5000)  # Wait for 5 seconds before quitting
        done = True

pygame.quit()