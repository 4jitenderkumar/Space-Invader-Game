import pygame
from pygame import mixer

import random
import math


# Initialize the pygame
pygame.init()

# create the screen - Width, Height
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1) #to play in loop - pass -1

# Title and Icon , Icon - PNG and 32*32 size
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('Mango Salsa - Personal Use.ttf', 32) # Download other fonts from dafont.com

textX = 10
testY = 10


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # blit = draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit = draw
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # BCZ it looks good when we fire the bullet


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop - Makes sure that window doesn't close, our game will run on this loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's R or L
        # KEYDOWN - pressing the key, KEYUP - releasing the key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_UP:
                playerY_change = -4
            if event.key == pygame.K_DOWN:
                playerY_change = 4
            if event.key == pygame.K_SPACE:
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # Player - Checking for boundaries of sapceship so that it doesnt go out of Bound
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:  # SUBSTRACT 64 from 800 , BCZ pixel size was 64*64
        playerX = 736

    # Enemy - Checking for boundaries of Enemy so that it doesnt go out of Bound
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # SUBSTRACT 64 from 800 , BCZ pixel size was 64*64
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)  # if it is 800 then it will come down
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()



# https://www.flaticon.com/
# https://www.freepik.com/
# https://www.online-convert.com/
# https://www.dafont.com/
# https://www.pygame.org/