##
# Beach Battles Game CPT
#
# @author Usayd Jahangiri
# @course ICS3UC
# @date 2021/1/28
##

## --- Pygame Setup
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 124, 240)
BEIGE = (255, 242, 0)

# initialize font
pygame.font.init()

# Load background image
background_image = pygame.image.load('beach.png')

## --- Player Attributes
# load player image
player_image = pygame.image.load('tank.png')

# set position
player_x = 375
player_y = 500

# player speed vector
player_Xchange = 0
player_Ychange = 0


## --- Enemy Attributes
# load enemy image (enemies)
pirate_image = []

# set position
pirate_x = []
pirate_y = []

# moving pirate
pirate_moveY = []
pirate_moveX = []

# how many enemies?
num_pirates = 7

# add attributes to all enemies
for i in range(num_pirates):
    pirate_image.append(pygame.image.load('pirate.png'))
    pirate_x.append(random.randint(0, 730))
    pirate_y.append(random.randint(-50, 0))
    pirate_moveY.append(0.7)
    pirate_moveX.append(0)


## --- Fireball Attributes
# load fireball image
fireball_image = pygame.image.load('fireball.png')

# set position
fireball_x = 0
fireball_y = 500

# moving fireball
fireball_moveX = 0
fireball_moveY = 20

# state of fireball (moving or no?)
fireball_state = "set" # not moving


## Text on Game Screen
# Create variable for score
score = 0
text = pygame.font.Font(None, 36) #font size

# score position
text_x = 5
text_y = 5

# font for game over
text_over = pygame.font.Font(None, 64)

## --- Defining Objects
# Define a player
def drawPlayer(x,y):
    screen.blit(player_image, [x,y])

# Define an enemy
def drawPirate(x,y,i):
    screen.blit(pirate_image[i], [x,y])

# Define a fireball
def shootFireball(x,y):
    global fireball_state
    fireball_state = "shoot"
    screen.blit(fireball_image, [x+25, y+16]) # makes fireball center of tank

# Define the score
def drawScore(x, y):
    score_points = text.render("Score: " + str(score), True, WHITE)
    screen.blit(score_points, (x, y))

# Define game over
def gameOver():
    show_over = text_over.render("GAME OVER!!!", True, RED)
    screen.blit(show_over, (250, 250))

# Define collision
def checkCollision(pirate_x, pirate_y, fireball_x, fireball_y):
    # use distance formula ((d = √((x_2-x_1)² + (y_2-y_1)²))
    # (exponent 0.5 can be used to sqaure root formula)
    distance = ((pirate_x - fireball_x)**2 + (pirate_y - fireball_y)**2)**0.5
    if distance <= 27:
        return True
    else:
        return False

# Initialize pygame
pygame.init()

## --- Screen setup
size = (800, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Beach Battles")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

## --- Start screen
# fonts for start screen
start_font = pygame.font.Font(None, 45)
control_font = pygame.font.Font(None, 25)
title_font = pygame.font.Font(None, 60)

# screen starts at page 1
show_screen = True
screen_page = 1

# --- Start screen page loop ---
while not done and show_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if user clicks again, game will begin
            screen_page += 1
            if screen_page == 2:
                show_screen = False

    # set start screen background
    screen.fill(BLUE)
    # Text on screen
    if screen_page == 1:
        screen_text = control_font.render("Press mouse button to start", True, WHITE)
        screen.blit(screen_text, [10, 575])

        screen_text = start_font.render("Controls:", True, WHITE)
        screen.blit(screen_text, [330, 250])

        screen_text = control_font.render("- use arrow keys to move UP, DOWN, LEFT and RIGHT", True, WHITE)
        screen.blit(screen_text, [210, 300])

        screen_text = control_font.render("- press SPACE to shoot fireball", True, WHITE)
        screen.blit(screen_text, [210, 330])

        screen_text = title_font.render("BEACH BATTLES", True, WHITE)
        screen.blit(screen_text, [230, 20])
    # Limit to 60 FPS
    clock.tick(60)

    # update screen
    pygame.display.flip()


### --- Main Program Loop ---
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            # manual control of player
            if event.key == pygame.K_RIGHT:
                player_Xchange = 10
            elif event.key == pygame.K_LEFT:
                player_Xchange = -10
            elif event.key == pygame.K_UP:
                player_Ychange = -10
            elif event.key == pygame.K_DOWN:
                player_Ychange = 10
             # manual control of fireball
            elif event.key == pygame.K_SPACE:
                if fireball_state == "set":
                    fireball_x = player_x
                    shootFireball(fireball_x, fireball_y)

        # User let up on a key
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_Xchange = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_Ychange = 0

## Game Logic and Boundries

    # Move player according to speed vector
    player_x = player_x + player_Xchange
    player_y = player_y + player_Ychange

    for i in range(num_pirates):
        # Move enemy according to speed vector
        pirate_y[i] = pirate_y[i] + pirate_moveY[i]


    # Player Boundries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    if player_y <= 475:
        player_y = 475
    elif player_y >= 536:
        player_y = 536

    # Enemy Logic
    for i in range(num_pirates):

        # check collision
        collision = checkCollision(pirate_x[i], pirate_y[i], fireball_x, fireball_y)
        if collision:
            fireball_y = 500
            fireball_state = "set"
            pirate_x[i] = random.randint(0, 730)
            pirate_y[i] = random.randint(-50, 0)
            score += 15

        # makes enemies faster after more points scored
        if score >= 150:
            pirate_moveY[i] = 0.9
        if score >= 500:
            pirate_moveY[i] = 1
        if score >= 1000:
            pirate_moveY[i] =  1.1


    # fireball Boundries
    if fireball_y <= 0:
        fireball_y = 500
        fireball_state = "set" # reset to starting position


    # Don't put any draw functions above this
    # Display background image starting from top corner (0,0)
    screen.blit(background_image, [0,0])

## --- Calling Code

    # call fireball moving
    if fireball_state == "shoot":
        shootFireball(fireball_x, fireball_y)
        fireball_y -= fireball_moveY

    # call player
    drawPlayer(player_x, player_y)

    # call score
    drawScore(text_x, text_y)

    # call pirate(s)
    for i in range(num_pirates):
        drawPirate(pirate_x[i], pirate_y[i], i)
        # game over text if enemy reaches border
        if pirate_y[i] >= 425:
           pirate_y[i] = 425
           screen.fill(BLACK) # make screen black
           gameOver()
           screen_text = control_font.render("Total Score: " +str(score), True, GREEN)
           screen.blit(screen_text, [330, 350])

## --- Display
    # Update display
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()