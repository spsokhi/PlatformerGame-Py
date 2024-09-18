import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinite Platformer")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player properties
player_size = (50, 50)
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size[1]]
player_vel = [0, 0]
player_speed = 5
gravity = 0.5
jump_strength = -10
is_jumping = False

# Platforms list
platforms = []
platform_width = 100
platform_height = 10

# Initial platforms
platforms.append(pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))  # Ground platform
for i in range(5):
    x = random.randint(0, SCREEN_WIDTH - platform_width)
    y = SCREEN_HEIGHT - (i * 120) - 100
    platforms.append(pygame.Rect(x, y, platform_width, platform_height))

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Horizontal movement
    player_vel[0] = 0
    if keys[pygame.K_LEFT]:
        player_vel[0] = -player_speed
    if keys[pygame.K_RIGHT]:
        player_vel[0] = player_speed

    # Jumping
    if not is_jumping and keys[pygame.K_SPACE]:
        player_vel[1] = jump_strength
        is_jumping = True

    # Apply gravity
    player_vel[1] += gravity

    # Update player position
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]

    # Create player rectangle
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])

    # Check for collision with platforms
    collision = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_vel[1] >= 0:
            player_pos[1] = platform.top - player_size[1]
            player_vel[1] = 0
            is_jumping = False
            collision = True
            break

    if not collision:
        is_jumping = True

    # Keep the player on the screen horizontally
    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] > SCREEN_WIDTH - player_size[0]:
        player_pos[0] = SCREEN_WIDTH - player_size[0]

    # Scroll the screen when the player reaches the upper third
    if player_pos[1] < SCREEN_HEIGHT / 3:
        scroll = SCREEN_HEIGHT / 3 - player_pos[1]
        player_pos[1] = SCREEN_HEIGHT / 3

        # Move platforms down
        for platform in platforms:
            platform.y += scroll

    # Remove platforms that are off the screen
    platforms = [platform for platform in platforms if platform.y < SCREEN_HEIGHT]

    # Add new platforms at the top
    while len(platforms) < 6:
        x = random.randint(0, SCREEN_WIDTH - platform_width)
        y = platforms[-1].y - random.randint(80, 120)
        new_platform = pygame.Rect(x, y, platform_width, platform_height)
        platforms.append(new_platform)

    # Prevent the player from falling off the bottom
    if player_pos[1] > SCREEN_HEIGHT - player_size[1]:
        player_pos[1] = SCREEN_HEIGHT - player_size[1]
        player_vel[1] = 0
        is_jumping = False

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform)

    # Draw the player
    pygame.draw.rect(screen, WHITE, player_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
