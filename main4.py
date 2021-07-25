import random

import pygame
from pygame import gfxdraw
import numpy as np
import time
import sys
# import os

from Klassen4 import Star, Planet, Player, Background, Shot, velocity_panel

#if getattr(sys, 'frozen', False):
#    os.chdir(sys._MEIPASS)

def rotate(image, rect, angle):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect




# Constants

#TIMESTEP = 0.2
AIMSTEP = 3
GRAVITATIONAL_CONSTANT = 1

GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
WHITE = [255, 255, 255]

PLAYER_SIZE = 20
PLAYER_THRUST = 0.15
FIRE_LENGTH = (5, 20)

SHOT_LIFETIME = 35
SHOT_SPEED = 20
SHOT_SIZE = 4

# Declarations

Background_Count = 0

Shot_list = []

'# Eine Sonne zwei Planeten'
'''Sun = Star((500, 500), 10000, YELLOW)
Earth = Planet([300, 500], 1000, [0, 7], GREEN)
Venus = Planet([100, 500], 2000, [0, -5], GREEN)
Player1 = Player([500, 300], [7, 0], 0, PLAYER_THRUST, PLAYER_SIZE, WHITE, "Player1", pygame.image.load('graphics/player/Spaceship_Red.png'))
Player2 = Player([250,350], [-3, 3], 0, PLAYER_THRUST, PLAYER_SIZE, WHITE, "Player2", pygame.image.load('graphics/player/Spaceship_Blue.png'))
bodies_list = [Sun, Earth, Venus, Player2, Player1]
bodycount = 5'''

'#Zwei Sonnen ein Planet'
Sun = Star((600, 500), 10000, YELLOW)
Sun2 = Star((1200, 500), 10000, YELLOW)
Earth = Planet([900, 200], 3000, [10, 0], GREEN)
Player1 = Player([300, 500], [0, 1], 0, PLAYER_THRUST, PLAYER_SIZE, WHITE, "Player1", pygame.image.load('graphics/player/Spaceship_Red.png'))
Player2 = Player([1000, 500], [0, 5], 0, PLAYER_THRUST, PLAYER_SIZE, WHITE, "Player2", pygame.image.load('graphics/player/Spaceship_Blue.png'))
bodies_list = [Sun, Sun2, Earth, Player2, Player1]
bodycount = 5


# beginning of main
# ----------------------------------------------------------

pygame.init()
infoScreen = pygame.display.Info()
WIDTH = infoScreen.current_w
HEIGHT = infoScreen.current_h
#screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
background = Background("graphics/background/Background", (0, 0))
background2 = Background("graphics/background/Background", (1000, 0))

# music
# -----------------------------------
pygame.mixer.init()
pygame.mixer.music.load("sounds/Sound.wav")
pygame.mixer.music.play(-1, 0.0)

while True:

    # Events/ Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            sys.exit(0)

#----------------------------------------------------------------------
    for event in pygame.event.get():
        if (event.type == pygame.K_LCTRL) and (event.type == pygame.K_q):
            sys.exit(0)
#----------------------------------------------------------------------
#           Zeit Stuff mit TIMESTEP und so
    clock = pygame.time.Clock()
    TIMESTEP = clock.tick(60)/80

#----------------------------------------------------------------------

    # Screen
    screen.fill((0, 0, 0))

    Background_Count += 1.25
    if Background_Count <= 10:
        screen.blit(background.image[0], background.rect)
        screen.blit(background2.image[0], background2.rect)
    if (Background_Count <= 20) &(Background_Count > 10):
        screen.blit(background.image[1], background.rect)
        screen.blit(background2.image[1], background2.rect)
    if (Background_Count <= 30) & (Background_Count > 20):
        screen.blit(background.image[2], background.rect)
        screen.blit(background2.image[2], background2.rect)
    if (Background_Count <= 40) & (Background_Count > 30):
        screen.blit(background.image[3], background.rect)
        screen.blit(background2.image[3], background2.rect)
    if (Background_Count <= 50) & (Background_Count > 40):
        screen.blit(background.image[4], background.rect)
        screen.blit(background2.image[4], background2.rect)
    if Background_Count == 50:
        Background_Count -= 50

    #screen.blit(background.image, background.rect)


    # Player Input
    keys = pygame.key.get_pressed()

    # Player1
    if keys[pygame.K_d]:
        Player1.aim_turn(1, AIMSTEP)
    if keys[pygame.K_a]:
        Player1.aim_turn(-1, AIMSTEP)
    if keys[pygame.K_w]:
        Player1.thrust = True
    else:
        Player1.thrust = False
    if keys[pygame.K_e]:
        Player1.shot = True
    else:
        Player1.shot = False

    # Player2
    if keys[pygame.K_l]:
        Player2.aim_turn(1, AIMSTEP)
    if keys[pygame.K_j]:
        Player2.aim_turn(-1, AIMSTEP)
    if keys[pygame.K_i]:
        Player2.thrust = True
    else:
        Player2.thrust = False
    if keys[pygame.K_o]:
        Player2.shot = True
    else:
        Player2.shot = False


    # actual game ------------------------------- #

    for i in range(bodycount):
        x = bodies_list[i]
        if x.description == "Star":
            continue

        for j in range(bodycount):
            y = bodies_list[j]
            if (i == j) or (y.mass == 0):
                break

            r_quadrat = pow(y.position[0] - x.position[0], 2) + pow(y.position[1] - x.position[1], 2)
            force = TIMESTEP * GRAVITATIONAL_CONSTANT * (y.mass / r_quadrat)

            # shuttle alive
            if (x.mass == 0) & (y.radius > np.sqrt(r_quadrat)):
                x.alive = False
                break

            # alpha
            alpha = np.arctan2(y.position[1] - x.position[1], y.position[0] - x.position[0])

            # v_delta
            mini_v_delta = [0, 0]

            mini_v_delta[0] = force * np.cos(alpha)
            mini_v_delta[1] = force * np.sin(alpha)

            # Distance Calculation
            if type(x) is Player:
                x.velocity[0] = x.velocity[0] + mini_v_delta[0] + x.v_thrust * x.vektor[0] * int(x.thrust)
                x.velocity[1] = x.velocity[1] + mini_v_delta[1] + x.v_thrust * x.vektor[1] * int(x.thrust)
            else:
                x.velocity[0] = x.velocity[0] + mini_v_delta[0]
                x.velocity[1] = x.velocity[1] + mini_v_delta[1]


    # Timestep, Thrust, Shoot, Image ----------------------------- #
    for i in range(bodycount):
        x = bodies_list[i]

        # Star
        if x.description == "Star":
            a = int(x.position[0])
            b = int(x.position[1])
            #pygame.draw.circle(screen, x.color, (a, b), x.radius, 0)
            pygame.gfxdraw.filled_circle(screen, a, b, x.radius, x.color)
            pygame.gfxdraw.aacircle(screen, a, b, x.radius, x.color)
            continue

        x.position[0] = x.position[0] + x.velocity[0] * TIMESTEP
        x.position[1] = x.position[1] + x.velocity[1] * TIMESTEP
        a = int(x.position[0])
        b = int(x.position[1])

        # Planet
        if x.description == "Planet":
            #pygame.draw.circle(screen, x.color, (a, b), x.radius, 0)
            pygame.gfxdraw.filled_circle(screen, a, b, x.radius, x.color)
            pygame.gfxdraw.aacircle(screen, a, b, x.radius, x.color)

        # Player
        if type(x) == Player:

            # Alive
            if x.alive is False:
                continue

            # Direction

            '''direction1 = [x.position[0] + FIRE_LENGTH[1] * x.vektor[0],
                         x.position[1] + FIRE_LENGTH[1] * x.vektor[1]]
            direction2 = [x.position[0] - FIRE_LENGTH[1] * x.vektor[0]*0,
                          x.position[1] - FIRE_LENGTH[1] * x.vektor[1]*0]
            pygame.draw.lines(screen, x.color, False, [direction2, direction1], 3)'''

            # Image
            rect = x.image.get_rect(center=x.position)
            image, rect = rotate(x.image, rect, -x.aim)

            screen.blit(image, rect)


            # Thrust
            if x.thrust is True:
                fire_lenght = random.randint(FIRE_LENGTH[0], FIRE_LENGTH[1])
                direction1 = [x.position[0] - x.vektor[0] * 22,
                             x.position[1] - x.vektor[1] * 22]
                direction2 = [x.position[0] - fire_lenght * x.vektor[0] - x.vektor[0] * 22,
                             x.position[1] - fire_lenght * x.vektor[1] - x.vektor[1] * 22]
                pygame.draw.lines(screen, (255, 165, 0), False, [direction2, direction1], 5)

            # Velocity Panel
            velocity_panel(x, screen, WIDTH, HEIGHT)

            # Shot
            if x.shot is True:
                Shot_list += [Shot([x.position[0] + (PLAYER_SIZE * x.vektor[0]),
                                    x.position[1] + (PLAYER_SIZE * x.vektor[1])],

                                   [x.velocity[0] + (SHOT_SPEED * x.vektor[0]),
                                    x.velocity[1] + (SHOT_SPEED * x.vektor[1])],

                                   [x.vektor[0], x.vektor[1]],

                                   SHOT_LIFETIME)]

    # Shot List
    Shot_deletion_list = []
    
    if len(Shot_list) > 0:

        for i in range(len(Shot_list)):
            shot = Shot_list[i]
            shot.pos[0] += shot.v[0] * TIMESTEP
            shot.pos[1] += shot.v[1] * TIMESTEP

            pygame.draw.aaline(screen, GREEN, [shot.pos[0], shot.pos[1]],
                               [shot.pos[0] - (shot.aim[0] * SHOT_SIZE), shot.pos[1] - (shot.aim[1] * SHOT_SIZE)])

            # Shot collision
            kollision = False
            for j in range(bodycount):
                body = bodies_list[j]
                distance = np.sqrt(pow(shot.pos[0] - body.position[0], 2) + pow(shot.pos[1] - body.position[1], 2))
                if distance < body.radius:
                    kollision = True
                    Shot_deletion_list = Shot_deletion_list + [shot]
                    if type(body) == Player:
                        body.alive = False


            shot.lifetime -= 1
            if shot.lifetime == 0:
                if kollision is False:
                    Shot_deletion_list = Shot_deletion_list + [shot]


        if len(Shot_deletion_list) > 0:
            for i in range(len(Shot_deletion_list)):
                Shot_list.remove(Shot_deletion_list[i])


    pygame.display.update()
    #time.sleep(1)