import pygame, os
import sys
import math
import random
import Physics
import Combat

from config import players, SCREENX, SCREENY, global_speed

base_dir = os.path.dirname(os.path.abspath(__file__))

pygame.init()

running = True
clock = pygame.time.Clock()

modes = pygame.display.list_modes()
screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Ball fighting simulator")

Fullscreen = False

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
SCREENX, SCREENY = (SCREEN_WIDTH / 1280), (SCREEN_HEIGHT / 720)

resl_Buttons = []

middleButtonRect = pygame.Rect((SCREEN_WIDTH/2.5), (SCREEN_HEIGHT/2), 150 * (SCREENX), 80 * (SCREENX))
downButtonRect = pygame.Rect((SCREEN_WIDTH/2.5), (SCREEN_HEIGHT/1.5), 150 * (SCREENX), 80 * (SCREENX))
optionRECT = pygame.Rect((SCREEN_WIDTH/2.4), (SCREEN_HEIGHT/3.1), 170 * (SCREENX), 50 * (SCREENX))
bottomRect = pygame.Rect((SCREEN_WIDTH/2.55), (SCREEN_HEIGHT/1.2), 170 * (SCREENX), 50 * (SCREENX))

Black = (0,0,0)
WHITE = (255, 255, 255)
Green = (0,255,0)
LGreen = (26,255,60)

fire_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'fire.png')).convert_alpha()
bfire_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'bfire.png')).convert_alpha()
poison_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'poison.png')).convert_alpha()
virus_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'virus.png')).convert_alpha()
static_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'static.png')).convert_alpha()
frost_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'frost.png')).convert_alpha()
leech_Image = pygame.image.load(os.path.join(base_dir, 'Assets', 'images', 'leech.png')).convert_alpha()

tick = 0
gameTick = 0
dt = 0
Frame = 0
FPS = 0

bigFont = pygame.font.Font(None, int(72 * SCREENX))
Font = pygame.font.Font(None, int(52 * SCREENX))
tinyFont = pygame.font.Font(None, int(24 * SCREENX))

def draw_button(button_rect, button_text, clr1, clr2):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, clr1, button_rect)
    else:
        pygame.draw.rect(screen, clr2, button_rect)

    # Center text on button
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

class Player:
    def __init__(self, x, y, r, hp, armr, dmg, clr, spd, encht, tier, ult,vx=0, vy=0):
        self.x = x * SCREENX
        self.y = y * SCREENY
        self.r = r * (SCREENY)
        self.clr = clr

        self.hp = hp
        self.armr = armr
        self.dmg = dmg
        self.spd = spd * (SCREENY)

        angle = random.uniform(0, 360)
        rad = math.radians(angle)

        self.vx = math.cos(rad) * spd
        self.vy = math.sin(rad) * spd

        self.ultmeter = 0
        self.ult = ult

        self.encht = encht
        self.enTier = tier

        self.DoTs = {}

        self.pause = False
        self.disabled = False
        self.iframe = False

        self.collision_cooldown = 0

        self.font = pygame.font.Font(None, int(math.floor(r/1.5) * SCREENX))
        self.text_surface = self.font.render(str(hp) + " + " + str(armr), True, WHITE)
    
    def draw(self):
        displayString = ""
        if (self.armr > 0) :
            displayString = str(math.ceil(self.hp)) + " + " + str(math.ceil(self.armr))
        else:
            displayString = str(math.ceil(self.hp))

        self.text_surface = self.font.render(displayString, True, WHITE)

        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.r)
        pygame.draw.circle(screen, self.clr, (self.x, self.y), self.r - 5 * SCREENY)
        screen.blit(self.text_surface, (self.x - self.r/2, self.y))

    def move(self, dt):
        if (self.pause == True):
            return
        
        self.x += self.vx * dt * global_speed
        self.y += self.vy * dt * global_speed

        collided = False
        if self.x < self.r:
            self.x = self.r
            self.vx *= -1
            collided = True
        elif self.x > SCREEN_WIDTH - self.r:
            self.x = SCREEN_WIDTH - self.r 
            self.vx *= -1
            collided = True

        if self.y < self.r:
            self.y = self.r 
            self.vy *= -1
            collided = True
        elif self.y > SCREEN_HEIGHT - self.r:
            self.y = SCREEN_HEIGHT - self.r 
            self.vy *= -1
            collided = True
        
        if (collided == True):
            if (self.armr > 0):
                self.armr -= 1
            else:
                self.hp -= 1

def initiateBattle():
    #--------------------(X position, Y postion, radius, health, armor, damage, colour, speed, effect, tier, ultimate)
    # same colour balls won't damage eachother
    players.append(Player(100, 100, 60, 500, 100, 5, (255,0,0), 500, "fire", 1, "none"))  # red ball
    players.append(Player(300, 200, 60, 500, 100, 5, (0,255,0), 500, "poison", 1, "none"))  # green ball
    players.append(Player(500, 400, 60, 500, 100, 5, (10,10,10), 500, "bfire", 1, "none"))  # black ball
    players.append(Player(500, 600, 60, 500, 100, 5, (0,255,255), 500, "frost", 1, "none"))  # cyan  ball
    players.append(Player(300, 600, 60, 500, 100, 5, (0,100,255), 500, "static", 1, "none")) # blue ball
    players.append(Player(300, 300, 60, 500, 100, 5, (1, 50, 32), 500, "virus", 1, "none"))  # dark green ball
    players.append(Player(200, 500, 60, 500, 100, 5, (50, 10, 32), 500, "leech", 1, "none"))  # dark red ball
    #players.append(Player(500, 500, 80, 500, 100, 5, (125, 125, 125), 800, "mage", 1, "none")) # - Special ball

def mainMenu():
    mainText = bigFont.render("Ball fighting simulator", True, WHITE)
    PlayText = Font.render("Play", True, WHITE)
    SettingText = Font.render("Settings", True, WHITE)
    ExitText = Font.render("Exit", True, WHITE)

    screen.blit(mainText, ((SCREEN_WIDTH/3.5), (SCREEN_HEIGHT/5)))

    draw_button(middleButtonRect, PlayText, Green, LGreen)
    draw_button(downButtonRect, SettingText, Black, Black)
    draw_button(bottomRect, ExitText, Black, Black)

def Settings():
    mainText = bigFont.render("Settings", True, WHITE)
    reslText = Font.render("Resolution :", True, WHITE)
    optText = Font.render(str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT), True, Black)

    screen.blit(mainText, ((SCREEN_WIDTH/2.5), (SCREEN_HEIGHT/6)))
    screen.blit(reslText, ((SCREEN_WIDTH/4), (SCREEN_HEIGHT/3)))

    draw_button(optionRECT, optText, WHITE, (125, 125, 125))

    if (resolutionPanel == True):
        resl_Buttons = []
        for index, res in enumerate(modes):
            if (res == screen.get_size()):
                continue

            optText_temp = Font.render(str(res[0]) + "x" + str(res[1]), True, Black)
            optRect_temp = pygame.Rect((SCREEN_WIDTH/2.4), (SCREEN_HEIGHT/3.1) + (50 * (index + 1)), 170 * (SCREENX), 50 * (SCREENX))
                
            draw_button(optRect_temp, optText_temp, WHITE, (125, 125, 125))

            resl_Buttons.append([optRect_temp, index]) 

def Game():
    global gameTick
    global FPS
    gameTick += dt
    if (gameTick >= 1):
        FPS = math.floor(1 / dt)
        gameTick = 0

    screen.blit(tinyFont.render(str(FPS) + " FPS", True, WHITE), (0, 0))

    for plr in players:
        plr.move(dt)
        plr.draw()

        if (plr.collision_cooldown > 0):
            plr.collision_cooldown -= dt

        Combat.effectDoT(plr, dt)

        if (plr.hp <= 0):
            players.remove(plr)

        for index, DoT in enumerate(plr.DoTs):
            scaleX = (plr.r/2) * (SCREENX)
            scaleY = (plr.r/2) * (SCREENY)

            posY = (plr.y - (plr.r + 10) * SCREENY) - scaleY
            posX = plr.x + ((index - 1) * scaleX)

            if DoT == "fire":
                screen.blit(pygame.transform.scale(fire_Image, (scaleX, scaleY)), (posX, posY))
            if DoT == "bfire":
                screen.blit(pygame.transform.scale(bfire_Image, (scaleX, scaleY)), (posX, posY))
            if DoT == "poison":
                screen.blit(pygame.transform.scale(poison_Image, (scaleX, scaleY)), (posX, posY))
            if DoT == "static":
                screen.blit(pygame.transform.scale(static_Image, (scaleX, scaleY)), (posX, posY))
            if DoT == "virus":
                screen.blit(pygame.transform.scale(virus_Image, (scaleX, scaleY)), (posX, posY))
            if DoT == "frost":
                screen.blit(pygame.transform.scale(frost_Image, (scaleX, scaleY)), (posX, posY))
            if DoT == "leech":
                screen.blit(pygame.transform.scale(leech_Image, (scaleX, scaleY)), (posX, posY))

            screen.blit(tinyFont.render(str(plr.DoTs[DoT]["tier"]), True, WHITE), (posX, posY))
            screen.blit(tinyFont.render(str(plr.DoTs[DoT]["dura"]), True, WHITE), (posX, (plr.y - (plr.r/2 + 15) * SCREENY) - scaleY))
    if (Frame % 4 == 0) :
        for i in range(len(players)):
            for j in range(i+1, len(players)):
                p1 = players[i]
                p2 = players[j]

                if Physics.CheckCollision(p1.x, p1.y, p2.x, p2.y, p1.r, p2.r):
                    Physics.ResolveCollision(p1, p2, dt)

state = "menu"
resolutionPanel = False

while running == True:
    Frame += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if (tick > 0.01):
            tick = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (middleButtonRect.collidepoint(event.pos) and state == "menu"):
                    state = "game"

                    #for i in range(1, 30):
                    initiateBattle()
                if (downButtonRect.collidepoint(event.pos) and state == "menu"):
                    state = "settings"
                if (optionRECT.collidepoint(event.pos) and state == "settings"):
                    resolutionPanel = True
                if (bottomRect.collidepoint(event.pos) and state == "menu"):
                    running = False
                
                for button in resl_Buttons:
                    if (button[0].collidepoint(event.pos) and state == "settings" and resolutionPanel == True):
                            screen = pygame.display.set_mode(modes[button[1]])

                            SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
                            SCREENX, SCREENY = (SCREEN_WIDTH / 1280), (SCREEN_HEIGHT / 720)

                            middleButtonRect = pygame.Rect((SCREEN_WIDTH/2.5), (SCREEN_HEIGHT/2), 150 * (SCREENX), 80 * (SCREENX))
                            downButtonRect = pygame.Rect((SCREEN_WIDTH/2.5), (SCREEN_HEIGHT/1.5), 150 * (SCREENX), 80 * (SCREENX))
                            optionRECT = pygame.Rect((SCREEN_WIDTH/2.4), (SCREEN_HEIGHT/3.1), 170 * (SCREENX), 50 * (SCREENX))

                            resolutionPanel = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE] == True):
        if (state != "menu"):
            state = "menu"
            resolutionPanel = False
            players = []
    elif (keys[pygame.K_F11] == True):
        if (Fullscreen == False):
            Fullscreen = True
            screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
        else:
            Fullscreen = False
            screen = pygame.display.set_mode(modes[0])
    if (keys[pygame.K_SPACE] == True and keys[pygame.K_LSHIFT] == False):
        global_speed = 0.5
    elif (keys[pygame.K_LSHIFT] == True and keys[pygame.K_SPACE] == False):
        global_speed = 2
    elif (keys[pygame.K_SPACE] == True and keys[pygame.K_LSHIFT] == True):
        global_speed = 0.1
    else:
        global_speed = 1

    screen.fill(Black)

    if (state == "game"):
       Game()
    elif (state == "menu"):
       mainMenu()
    elif (state == "settings"):
       Settings()                   
        
    pygame.display.flip()
    dt = clock.tick(500) / 1000
    tick += dt

pygame.quit()