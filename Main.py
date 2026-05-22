import pygame
import sys
import math
import random
import Physics

pygame.init()

running = True
clock = pygame.time.Clock()

Tick = 0
Tick_Dura = 1

Burning = []

screen = pygame.display.set_mode((1280, 720))
Black = (0,0,0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 50)

class Player:
    def __init__(self, x, y, r, hp, armr, dmg, clr, spd, encht, tier,vx=0, vy=0):
        self.x = x
        self.y = y
        self.r = r
        self.hp = hp
        self.armr = armr
        self.dmg = dmg
        self.clr = clr
        self.spd = spd
        self.dir = random.choice([45, 135, 225, 315])
        self.vx = vx
        self.vy = vy
        self.encht = encht
        self.enTier = tier

        self.text_surface = font.render(str(hp) + " + " + str(armr), True, WHITE)
    
    def draw(self):
        self.text_surface = font.render(str(self.hp) + " + " + str(self.armr), True, WHITE)

        pygame.draw.circle(screen, self.clr, (self.x, self.y), self.r)
        screen.blit(self.text_surface, (self.x - self.r/2, self.y))

    def move(self, dt):
        rad = math.radians(self.dir)

        self.x += self.vx + math.cos(rad) * self.spd * dt
        self.y += self.vy + math.sin(rad) * self.spd * dt

        if self.x < 0 + self.r or self.x > 1280 - self.r:
            self.dir = (180 - self.dir) % 360
            self.hp -= 1
        if self.y < 0 + self.r or self.y > 720 - self.r:
            self.dir = (-self.dir) % 360
            self.hp -= 1


plr_1 = Player(500, 500, 80, 100, 100, 3, (255, 0, 0), 800, "fire", 1)
plr_2 = Player(500, 500, 80, 100, 0, 3, (0, 0, 255), 900, "none", 0)


while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE] == True):
        running = False

    screen.fill(Black)
    plr_1.draw()
    plr_2.draw()

    pygame.display.flip()
    dt = clock.tick(144) / 1000

    plr_1.move(dt)
    plr_2.move(dt)

    if (Physics.CheckCollision(plr_1.x, plr_1.y, plr_2.x, plr_2.y, plr_1.r, plr_2.r) == True):
        Physics.ResolveCollision(plr_1, plr_2)

pygame.quit()