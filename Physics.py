import math
import pygame

clock = pygame.time.Clock()

tick_dura = 0.5

def Burn(ball, dmg):
    amount = 10
    tick = 0
    while True:
        if (tick >= tick_dura):
            amount -= 1
            ball.hp -= math.floor(dmg / 10)
        if (amount == 0):
            break

        tick += clock.tick(144)/ 1000


def DealDamage(plr_attacker, plr_defender):
    if (plr_defender.armr > 0 + plr_attacker.dmg):
        plr_defender.armr -= plr_attacker.dmg
    else:
        plr_defender.hp -= plr_attacker.dmg
    
    if (plr_attacker.encht == "fire"):
        plr_defender.hp -= plr_attacker.dmg * plr_attacker.enTier
       # Burn(plr_defender, plr_attacker.dmg * plr_attacker.enTier)

def CheckCollision(x1, y1, x2, y2, r1, r2):
    dx = x2 - x1
    dy = y2 - y1
    dist_sq = dx*dx + dy*dy
    rad_sum = r1 + r2

    if dist_sq <= rad_sum*rad_sum:
        return True
    return False

def ResolveCollision(plr1, plr2):
    dx = plr2.x - plr1.x
    dy = plr2.y - plr1.y
    dist = math.sqrt(dx*dx + dy*dy)

    if dist == 0:
        return

    overlap = (plr1.r + plr2.r) - dist
    if overlap > 0:
        nx = dx / dist
        ny = dy / dist
        plr1.x -= nx * overlap / 2
        plr1.y -= ny * overlap / 2
        plr2.x += nx * overlap / 2
        plr2.y += ny * overlap / 2

        tx, ty = -ny, nx 

        v1n = plr1.vx * nx + plr1.vy * ny
        v1t = plr1.vx * tx + plr1.vy * ty
        v2n = plr2.vx * nx + plr2.vy * ny
        v2t = plr2.vx * tx + plr2.vy * ty

        plr1.vx = v2n * nx + v1t * tx
        plr1.vy = v2n * ny + v1t * ty
        plr2.vx = v1n * nx + v2t * tx
        plr2.vy = v1n * ny + v2t * ty

        plr1.dir *= -1
        plr2.dir *= -1

        DealDamage(plr1, plr2)
        DealDamage(plr2, plr1)