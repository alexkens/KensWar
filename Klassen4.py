import numpy as np
import pygame


class Bodies:

    def __init__(self, position, mass, color, description):
        self.position = position
        self.mass = mass
        self.color = color
        self.description = description

class Star(Bodies):

    def __init__(self, position, mass, color):
        super().__init__(position, mass, color, description="Star")
        self.radius = int(np.sqrt(mass / np.pi) / 3)

class Planet(Bodies):

    def __init__(self, position, mass, velocity, color):
        super().__init__(position, mass, color, description="Planet")
        self.velocity = velocity
        self.radius = int(np.sqrt(mass / np.pi) / 3)

class Player(Bodies):

    def __init__(self, position, velocity, aim, v_thrust, radius, color, description, image):
        super().__init__(position, 0, color, description)
        self.velocity = velocity
        self.aim = aim
        self.vektor = [0, 0]
        self.aim_turn(1, 0)
        self.v_thrust = v_thrust
        self.alive = True
        self.image = image
        self.radius = radius
        self.thrust = False
        self.shot = False

    def aim_turn(self, way, AIMSTEP):
        self.aim = self.aim + way * AIMSTEP
        if self.aim < 0:
            self.aim += 360
        if self.aim > 360:
            self.aim -= 360
        aim = ((self.aim) * (1 / 180.0)) * np.pi
        self.vektor[0] = np.cos(aim)
        self.vektor[1] = np.sin(aim)

class Shot:
    def __init__(self, pos, v, aim, lifetime):
        self.lifetime = lifetime
        self.pos = pos
        self.v = v
        self.aim = aim


class Background(pygame.sprite.Sprite):
    image = []
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = [pygame.image.load(image_file + "1.jpg"),
                      pygame.image.load(image_file + "2.jpg"),
                      pygame.image.load(image_file + "3.jpg"),
                      pygame.image.load(image_file + "4.jpg"),
                      pygame.image.load(image_file + "5.jpg")]
        '''for i in range(0, 5):
            self.image[i] = self.image[i] pygame.image.load(image_file + str(i+1) +".jpg")'''
        self.rect = self.image[0].get_rect()
        self.rect.left, self.rect.top = location

def velocity_panel(player, screen, WIDTH, HEIGHT):
    Tacho1 = pygame.image.load('graphics/player/Tacho1.png')
    Tacho2 = pygame.image.load('graphics/player/Tacho2.png')
    if player.description == "Player1":
        screen.blit(Tacho1, (57, HEIGHT - 200))
    else:
        screen.blit(Tacho1, (WIDTH - 123, HEIGHT - 200))


    pygame.font.init()
    font = pygame.font.Font("graphics/font/Andromeda-eR2n.ttf", 30, bold=False, italic=False)

    velocity = np.sqrt(player.velocity[0] ** 2 + player.velocity[1] ** 2)
    v = velocity

    velocity = str(velocity)
    velocity = velocity[:5]
    text = player.description + " .. " + velocity
    textsurface = font.render(text, True, (0, 0, 0), (219, 219, 219))
    if player.description == "Player1":
        screen.blit(textsurface, (20,  HEIGHT - 120))
    else:
        screen.blit(textsurface, (WIDTH - 253,  HEIGHT - 120))

    if player.description == "Player1":
        nadel1 = [98, HEIGHT - 130]
    else:
        nadel1 = [WIDTH - 82, HEIGHT - 130]

    if v > 25:
        nadel2 = [nadel1[0] + np.sin(np.radians(115)) * 45,
                  nadel1[1] + np.cos(np.radians(115)) * 45]
    else:
        nadel2 = [nadel1[0] + np.sin(np.radians(240 - (100 * (v / 20)))) * 45,
                  nadel1[1] + np.cos(np.radians(240 - (100 * (v / 20)))) * 45]

    for i in range(-3, 3):
        pygame.draw.aaline(screen, [220, 0, 0], [nadel1[0] + i, nadel1[1]], nadel2)

    if player.description == "Player1":
        screen.blit(Tacho2, (57, HEIGHT - 200))
    else:
        screen.blit(Tacho2, (WIDTH - 123, HEIGHT - 200))

