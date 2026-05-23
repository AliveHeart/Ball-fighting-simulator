import pygame
import sys
import math
import random
import Physics
import Combat

pygame.init()

running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
Black = (0,0,0)
WHITE = (255, 255, 255)

tick = 0
dt = 0
global_speed = 1

players = []

class Player:
    def __init__(self, x, y, r, hp, armr, dmg, clr, spd, encht, tier,vx=0, vy=0):
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr

        self.hp = hp
        self.armr = armr
        self.dmg = dmg
        self.spd = spd

        angle = random.uniform(0, 360)
        rad = math.radians(angle)

        self.vx = math.cos(rad) * spd
        self.vy = math.sin(rad) * spd

        self.encht = encht
        self.enTier = tier

        self.DoT_tick = 1
        self.DoT_dmg = 0
        self.DoT_dura = 0

        self.collision_cooldown = 0

        self.font = pygame.font.Font(None, math.floor(r/1.5))
        self.text_surface = self.font.render(str(hp) + " + " + str(armr), True, WHITE)
    
    def draw(self):
        self.text_surface = self.font.render(str(math.ceil(self.hp)) + " + " + str(self.armr), True, WHITE)

        pygame.draw.circle(screen, self.clr, (self.x, self.y), self.r)
        screen.blit(self.text_surface, (self.x - self.r/2, self.y))

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x < self.r:
            self.x = self.r
            self.vx *= -1 * global_speed
        elif self.x > 1280 - self.r:
            self.x = 1280 - self.r 
            self.vx *= -1 * global_speed

        if self.y < self.r:
            self.y = self.r 
            self.vy *= -1 * global_speed
        elif self.y > 720 - self.r:
            self.y = 720 - self.r 
            self.vy *= -1 * global_speed


players.append(Player(100, 100, 80, 200, 100, 5, (255,0,0), 300, "fire", 7))  # red ball
players.append(Player(300, 200, 80, 200, 100, 5, (0,255,0), 300, "none", 0))  # green ball
players.append(Player(500, 400, 80, 200, 100, 5, (0,0,255), 300, "none", 0))  # blue ball

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE] == True):
        running = False

    screen.fill(Black)

    for plr in players:
        plr.move(dt)
        plr.draw()

        if (plr.collision_cooldown > 0):
            plr.collision_cooldown -= dt

        Combat.effectDoT(plr, dt)


    pygame.display.flip()
    dt = clock.tick(144) / 1000

    tick += dt
    for i in range(len(players)):
        for j in range(i+1, len(players)):
            p1 = players[i]
            p2 = players[j]

            if Physics.CheckCollision(p1.x, p1.y, p2.x, p2.y, p1.r, p2.r):
                Physics.ResolveCollision(p1, p2, dt)
        

pygame.quit()