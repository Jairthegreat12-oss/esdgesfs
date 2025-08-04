import pygame
import random
import sys
import requests
from io import BytesIO

# --- Initialization ---
# Initialize all the imported Pygame modules
pygame.init()

# --- Game Window Setup ---
# Set the dimensions of the game window
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# --- Game Clock ---
# Create a clock object to control the frame rate
clock = pygame.time.Clock()
fps = 60

# --- Font and Colors ---
# Define the font for displaying the score
font = pygame.font.SysFont('Bauhaus 93', 60)
# Define the color for the text
white = (255, 255, 255)

# --- Game Variables ---
# Gravity affects how fast the bird falls
gravity = 0.6
# The bird's current vertical velocity
bird_movement = 0
# Flag to track if the game is over
game_over = False
# Flag to track if the game has started
game_started = False
# Time interval (in milliseconds) for creating new pipes
pipe_frequency = 1500  # 1.5 seconds
# Get the current time to track pipe generation
last_pipe = pygame.time.get_ticks() - pipe_frequency
# Player's score
score = 0
high_score = 0
# Flag to track if the score has been awarded for passing a pipe
pass_pipe = False
# Ground scrolling position and speed
ground_scroll = 0
scroll_speed = 4


# --- Helper function to load images from URLs ---
def load_image_from_url(url):
    """
    Loads an image from a URL and returns it as a Pygame surface.
    Includes error handling for network issues or invalid URLs.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        image_data = BytesIO(response.content)
        return pygame.image.load(image_data).convert_alpha()
    except (requests.exceptions.RequestException, pygame.error) as e:
        print(f"Error loading image from {url}: {e}")
        # Return a placeholder surface if image loading fails
        fallback_surface = pygame.Surface((50, 50))
        fallback_surface.fill((255, 0, 0)) # Red square as a fallback
        return fallback_surface


# --- Load Images ---
# Load the background, ground, and button images using the helper function
bg_image = load_image_from_url('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/background-day.png')
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height - 64))

ground_image = load_image_from_url('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/base.png')
ground_image = pygame.transform.scale(ground_image, (screen_width, 64))

button_img = load_image_from_url('https://i.ibb.co/X4s2sW9/restart.png')

message_img = load_image_from_url('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/message.png')
message_img = pygame.transform.scale(message_img, (200, 300))

gameover_img = load_image_from_url('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/gameover.png')
gameover_img = pygame.transform.scale(gameover_img, (200, 50))


# --- Bird Class ---
class Bird(pygame.sprite.Sprite):
    """
    Represents the player's bird. Handles its movement, animation, and drawing.
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        # List of URLs for bird animation frames
        bird_image_urls = [
            'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/bluebird-downflap.png',
            'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/bluebird-midflap.png',
            'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/bluebird-upflap.png'
        ]
        # Load bird images from the URLs
        for url in bird_image_urls:
            self.images.append(load_image_from_url(url))

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0 # Vertical velocity
        self.clicked = False

    def update(self):
        # --- Gravity ---
        if game_started and not game_over:
            self.vel += gravity
            if self.vel > 8: # Terminal velocity
                self.vel = 8
            if self.rect.bottom < screen_height - 64: # Don't fall through ground
                self.rect.y += int(self.vel)

        if not game_over:
            # --- Jump ---
            # Check for mouse click or spacebar press
            if (pygame.mouse.get_pressed()[0] == 1 or pygame.key.get_pressed()[pygame.K_SPACE]) and not self.clicked:
                self.clicked = True
                self.vel = -10 # Jump strength
            if not (pygame.mouse.get_pressed()[0] == 1 or pygame.key.get_pressed()[pygame.K_SPACE]):
                self.clicked = False

            # --- Animation ---
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # --- Rotation ---
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # Point the bird downwards when the game is over
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# --- Pipe Class ---
class Pipe(pygame.sprite.Sprite):
    """
    Represents the pipe obstacles.
    """
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image_from_url('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/pipe-green.png')
        self.image = pygame.transform.scale(self.image, (80, 400))
        self.rect = self.image.get_rect()
        # Position 1 is top, -1 is bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - 75]
        if position == -1:
            self.rect.topleft = [x, y + 75]

    def update(self):
        if game_started:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

# --- Button Class ---
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# --- Helper Functions ---
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.vel = 0
    return 0

# --- Sprite Groups ---
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 20, button_img)

# --- Main Game Loop ---
running = True
while running:
    clock.tick(fps)

    # --- Draw Background and Ground ---
    screen.blit(bg_image, (0, 0))
    screen.blit(ground_image, (ground_scroll, screen_height - 64))

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)) and not game_started and not game_over:
            game_started = True

    # --- Update Sprites ---
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # --- Game Logic ---
    if game_started and not game_over:
        # --- Score ---
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and \
               bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and not pass_pipe:
                pass_pipe = True
            if pass_pipe and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
        
        # --- Pipe Generation ---
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe, top_pipe)
            last_pipe = time_now

        # --- Ground Scrolling ---
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

    # --- Display Score ---
    if game_started and not game_over:
        draw_text(str(score), font, white, int(screen_width / 2), 20)
    
    # --- Collision Detection ---
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= screen_height - 64:
        game_over = True
        game_started = False

    # --- Game State Management ---
    if not game_started and not game_over:
        screen.blit(message_img, (screen_width // 2 - 100, screen_height // 2 - 150))

    if game_over:
        if score > high_score:
            high_score = score
        screen.blit(gameover_img, (screen_width // 2 - 100, screen_height // 2 - 100))
        draw_text(f'Score: {score}', font, white, screen_width // 2 - 70, screen_height // 2 - 40)
        draw_text(f'Best: {high_score}', font, white, screen_width // 2 - 60, screen_height // 2 - 170)
        if restart_button.draw():
            game_over = False
            score = reset_game()

    pygame.display.update()

pygame.quit()
sys.exit()
