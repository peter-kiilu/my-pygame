import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen and game settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Catch the Falling Objects')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game Variables
basket_width = 100
basket_height = 20
basket_x = (screen_width - basket_width) // 2
basket_speed = 10
score = 0
game_over = False

# Falling object variables
falling_object_radius = 15
falling_object_speed = 5
falling_objects = []

# Set up the font for score
font = pygame.font.SysFont('Arial', 30)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Basket class to handle movement
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((basket_width, basket_height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (basket_x, screen_height - 30)

    def move(self, dx):
        if 0 < self.rect.centerx + dx < screen_width:
            self.rect.centerx += dx

# Falling object class to handle the falling objects
class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((falling_object_radius * 2, falling_object_radius * 2))
        pygame.draw.circle(self.image, RED, (falling_object_radius, falling_object_radius), falling_object_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), 0)

    def update(self):
        self.rect.y += falling_object_speed
        if self.rect.y > screen_height:
            self.kill()  # Remove the object if it reaches the bottom of the screen

# Initialize game objects
basket = Basket()
all_sprites = pygame.sprite.Group()
all_sprites.add(basket)
falling_objects_group = pygame.sprite.Group()

# Main game loop
while not game_over:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket.move(-basket_speed)
    if keys[pygame.K_RIGHT]:
        basket.move(basket_speed)

    # Create new falling objects randomly
    if random.randint(1, 50) == 1:
        falling_object = FallingObject()
        all_sprites.add(falling_object)
        falling_objects_group.add(falling_object)

    # Update all sprites
    all_sprites.update()

    # Check for collisions
    for falling_object in falling_objects_group:
        if basket.rect.colliderect(falling_object.rect):
            falling_object.kill()  # Remove the object
            score += 1  # Increase score when caught

    # Draw everything
    all_sprites.draw(screen)

    # Display the score
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
