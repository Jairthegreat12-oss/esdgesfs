import pygame
import sys
import random

# --- Initialization ---
pygame.init()

# --- Game Window Setup ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Classic Pong')

# --- Game Clock ---
clock = pygame.time.Clock()
fps = 60

# --- Colors and Font ---
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
font = pygame.font.Font(None, 64)

# --- Game Objects (Rectangles) ---
# The ball
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)

# The paddles
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# --- Game Variables ---
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# --- Score Variables ---
player_score = 0
opponent_score = 0

# --- Helper Functions ---

def ball_animation():
    """
    Handles the movement and collision of the ball.
    """
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # --- Ball Collision Detection ---
    # Top and bottom walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Left and right walls (scoring)
    if ball.left <= 0:
        player_score += 1
        ball_restart()
    
    if ball.right >= screen_width:
        opponent_score += 1
        ball_restart()

    # Paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    """
    Updates the player's paddle position and keeps it on screen.
    """
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    """
    A simple AI for the opponent's paddle. It tries to follow the ball.
    """
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    
    # Keep the opponent on screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    """
    Resets the ball to the center after a score and gives it a random direction.
    """
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Player input for paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # --- Game Logic ---
    ball_animation()
    player_animation()
    opponent_ai()

    # --- Drawing ---
    # Background
    screen.fill(bg_color)
    
    # Game objects
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    
    # Center line
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # --- Score Display ---
    player_text = font.render(f"{player_score}", True, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, screen_height / 2 - 32))

    opponent_text = font.render(f"{opponent_score}", True, light_grey)
    screen.blit(opponent_text, (screen_width / 2 - 40, screen_height / 2 - 32))

    # --- Update Display ---
    pygame.display.flip()
    clock.tick(fps)

# --- Quit Pygame ---
pygame.quit()
sys.exit()
