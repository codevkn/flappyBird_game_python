import pygame
import random
import os
from home import save_high_score

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load background image
BACKGROUND_IMG = pygame.image.load(os.path.join("resources", "background.png"))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Load sound effects
JUMP_SOUND = pygame.mixer.Sound(os.path.join("resources", "sound_effects", "sfx_wing.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("resources", "sound_effects", "sfx_hit.wav"))
DIE_SOUND = pygame.mixer.Sound(os.path.join("resources", "sound_effects", "sfx_die.wav"))
POINT_SOUND = pygame.mixer.Sound(os.path.join("resources", "sound_effects", "sfx_point.wav"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bird parameters
bird_frames = [pygame.transform.scale(pygame.image.load(os.path.join("resources", "bird", f"bird{i:02}.png")), (50, 38)) for i in range(17)]
bird_index = 0
bird_img = bird_frames[bird_index]
bird_rect = bird_img.get_rect()
bird_rect.center = (100, HEIGHT // 2)
bird_y_speed = 0

# Pipe parameters
pipe_img = pygame.image.load(os.path.join("resources", "pipe.png"))
pipe_img = pygame.transform.scale(pipe_img, (70, 400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
pipe_speed = 5

# Gravity
gravity = 0.25

# Score
score = 0
font = pygame.font.Font(None, 36)

# Load highest score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            content = file.read()
            if content:
                return int(content)
            else:
                return 0
    except FileNotFoundError:
        return 0

# Save highest score
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Game over
game_over = False

# Flag to track if new high score sound has been played
new_high_score_sound_played = False

def draw_window():
    WIN.blit(BACKGROUND_IMG, (0, 0))  # Draw background
    for pipe in pipe_list:
        WIN.blit(pipe_img, pipe)
    WIN.blit(bird_img, bird_rect)
    score_text = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(score_text, (10, 10))
    pygame.display.update()

def move_bird():
    global bird_y_speed, bird_index
    bird_y_speed += gravity
    bird_rect.centery += bird_y_speed
    bird_index = (bird_index + 1) % len(bird_frames)
    bird_img = bird_frames[bird_index]

def move_pipes():
    for pipe in pipe_list:
        pipe.centerx -= pipe_speed
    pipe_list[:] = [pipe for pipe in pipe_list if pipe.right > 0]

def spawn_pipe():
    pipe_heights = [200, 300, 400]
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_img.get_rect(midtop=(500, random_height))
    top_pipe = pipe_img.get_rect(midbottom=(500, random_height - 150))
    pipe_list.extend([bottom_pipe, top_pipe])

def check_collision():
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            HIT_SOUND.play()  # Play hit sound
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        DIE_SOUND.play()  # Play death sound
        return True
    return False

def update_score():
    global score, new_high_score_sound_played
    score += 1
    # Check if new high score is achieved
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        if not new_high_score_sound_played:
            POINT_SOUND.play()  # Play point sound for new high score
            new_high_score_sound_played = True

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_y_speed = -8
                JUMP_SOUND.play()  # Play jump sound
            if event.key == pygame.K_SPACE and game_over:
                bird_rect.center = (100, HEIGHT // 2)
                pipe_list.clear()
                bird_y_speed = 0
                score = 0
                game_over = False
                new_high_score_sound_played = False  # Reset flag
        if event.type == SPAWNPIPE:
            spawn_pipe()
    
    if not game_over:
        move_bird()
        move_pipes()
        game_over = check_collision()
        if not game_over:
            update_score()

    draw_window()

pygame.quit()
