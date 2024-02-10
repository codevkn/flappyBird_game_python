import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Home")

# Load background images
background_files = ["bg01.png", "bg02.png", "bg03.png"]
background_img = pygame.image.load(os.path.join("resources", "bg_home", random.choice(background_files)))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (150, 150, 150)

# Button parameters
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
PLAY_BUTTON_POS = (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50)
QUIT_BUTTON_POS = (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Load highest score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save highest score
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_home_screen():
    # Draw background
    WIN.blit(background_img, (0, 0))

    # Draw title with gradient color
    title_text = title_font.render("Codev", True, (255, 0, 0), (255, 255, 0))  # Gradient from red to yellow
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WIN.blit(title_text, title_rect)

    # Draw play button
    play_button_color = LIGHT_GRAY
    play_hover_color = GRAY

    mouse_pos = pygame.mouse.get_pos()
    if PLAY_BUTTON_POS[0] < mouse_pos[0] < PLAY_BUTTON_POS[0] + BUTTON_WIDTH and \
       PLAY_BUTTON_POS[1] < mouse_pos[1] < PLAY_BUTTON_POS[1] + BUTTON_HEIGHT:
        play_button_color = play_hover_color

    draw_rounded_rect(WIN, play_button_color, (PLAY_BUTTON_POS[0], PLAY_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT))
    play_text = font.render("Play", True, BLACK)
    WIN.blit(play_text, (PLAY_BUTTON_POS[0] + 60, PLAY_BUTTON_POS[1] + 10))

    # Draw quit button
    quit_button_color = LIGHT_GRAY
    quit_hover_color = GRAY

    if QUIT_BUTTON_POS[0] < mouse_pos[0] < QUIT_BUTTON_POS[0] + BUTTON_WIDTH and \
       QUIT_BUTTON_POS[1] < mouse_pos[1] < QUIT_BUTTON_POS[1] + BUTTON_HEIGHT:
        quit_button_color = quit_hover_color

    draw_rounded_rect(WIN, quit_button_color, (QUIT_BUTTON_POS[0], QUIT_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT))
    quit_text = font.render("Quit", True, BLACK)
    WIN.blit(quit_text, (QUIT_BUTTON_POS[0] + 60, QUIT_BUTTON_POS[1] + 10))

    # Draw high score
    high_score = load_high_score()
    high_score_text = font.render(f"High Score: {high_score}", True, GRAY)
    WIN.blit(high_score_text, (10, 10))

    pygame.display.update()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if PLAY_BUTTON_POS[0] < mouse_pos[0] < PLAY_BUTTON_POS[0] + BUTTON_WIDTH and \
                   PLAY_BUTTON_POS[1] < mouse_pos[1] < PLAY_BUTTON_POS[1] + BUTTON_HEIGHT:
                    # Start the game
                    os.system("python game.py")
                elif QUIT_BUTTON_POS[0] < mouse_pos[0] < QUIT_BUTTON_POS[0] + BUTTON_WIDTH and \
                     QUIT_BUTTON_POS[1] < mouse_pos[1] < QUIT_BUTTON_POS[1] + BUTTON_HEIGHT:
                    pygame.quit()
                    sys.exit()

        draw_home_screen()

if __name__ == "__main__":
    main()
