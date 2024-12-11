import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load assets (images and sounds)
BACKGROUND = pygame.image.load("background.jpg")  # Your background image
PLAYER_IMAGE = pygame.image.load("spaceship.png")  # Your spaceship image
ENEMY_IMAGE = pygame.image.load("alien.png")  # Your alien image
LASER_IMAGE = pygame.image.load("laser.png")  # Your laser image

# Resize images
BACKGROUND =  pygame.transform.scale(BACKGROUND, (1000,1000))
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (50, 50))
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (50, 50))
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (5, 20))

# Set up fonts
font = pygame.font.SysFont("Arial", 36)

# Set up sound effects
pygame.mixer.music.load("background_music.mp3")  # Background music
pygame.mixer.music.play(-1, 0.0)  # Play background music in loop
laser_sound = pygame.mixer.Sound("laser_sound.wav")
explosion_sound = pygame.mixer.Sound("explosion_sound.wav")

# Game variables
player_speed = 10
laser_speed = 7
enemy_speed = 2
enemy_frequency = 100  # Frequency of enemies (lower is more frequent)
score = 0
lives = 3
level = 1
game_over = False
laser_cooldown = 300  # Milliseconds between laser shots
last_shot_time = 0  # Tracks the time of the last laser fired

# Set up the player's spaceship
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 60
player_rect = pygame.Rect(player_x, player_y, 50, 50)

# Set up laser list
lasers = []

# Set up enemies list
enemies = []

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(BACKGROUND, (0, 0))  # Draw the background

    if not game_over:
        # Handle events (keyboard and quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Continuous movement when holding down keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Continuous shooting while holding spacebar
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= laser_cooldown:
                laser_rect = pygame.Rect(player_x + 22, player_y, 5, 20)
                lasers.append(laser_rect)
                laser_sound.play()  # Play laser sound
                last_shot_time = current_time

        # Update player position
        player_rect.x = player_x
        if player_rect.x < 0:
            player_rect.x = 0
        if player_rect.x > WIDTH - player_rect.width:
            player_rect.x = WIDTH - player_rect.width

        # Move lasers
        for laser in lasers[:]:
            laser.y -= laser_speed
            if laser.y < 0:
                lasers.remove(laser)

        # Move enemies
        if random.randint(1, enemy_frequency) == 1:
            enemy_x = random.randint(0, WIDTH - 50)
            enemy_rect = pygame.Rect(enemy_x, -50, 50, 50)
            enemies.append(enemy_rect)

        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1  # Deduct a life if the enemy reaches the bottom
            if enemy.colliderect(player_rect):
                enemies.remove(enemy)
                lives -= 1
                explosion_sound.play()  # Play explosion sound

        # Check for laser collisions with enemies
        for laser in lasers[:]:
            for enemy in enemies[:]:
                if laser.colliderect(enemy):
                    lasers.remove(laser)
                    enemies.remove(enemy)
                    score += 1  # Increase score
                    explosion_sound.play()

        # Draw the player's spaceship
        screen.blit(PLAYER_IMAGE, (player_rect.x, player_rect.y))

        # Draw lasers
        for laser in lasers:
            screen.blit(LASER_IMAGE, (laser.x, laser.y))

        # Draw enemies
        for enemy in enemies:
            screen.blit(ENEMY_IMAGE, (enemy.x, enemy.y))

        # Display score, lives, and level
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
        screen.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))

        # Check for game over
        if lives <= 0:
            game_over = True

        # Level progression
        if score >= level * 10:
            level += 1
            enemy_speed += 0.5
            enemy_frequency = max(20, enemy_frequency - 5)  # Increase enemy spawn rate

    else:
        # Game Over screen
        game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        # Wait for the player to restart or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset the game variables
                    score = 0
                    lives = 3
                    level = 1
                    enemy_speed = 2
                    enemy_frequency = 100
                    lasers.clear()
                    enemies.clear()
                    game_over = False
                if event.key == pygame.K_q:
                    running = False

    pygame.display.update()
    pygame.time.Clock().tick(60)  # 60 FPS

pygame.quit()