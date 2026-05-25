import math
import Combat

def CheckCollision(x1, y1, x2, y2, r1, r2):
    dx = x2 - x1
    dy = y2 - y1
    dist_sq = dx*dx + dy*dy
    rad_sum = r1 + r2

    if dist_sq <= rad_sum*rad_sum:
        return True
    return False

import math

def ResolveCollision(plr1, plr2, dt):
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

        spd1 = math.sqrt(plr1.vx**2 + plr1.vy**2)
        spd2 = math.sqrt(plr2.vx**2 + plr2.vy**2)
        if spd1 != 0:
            plr1.vx = plr1.vx / spd1 * plr1.spd
            plr1.vy = plr1.vy / spd1 * plr1.spd
        if spd2 != 0:
            plr2.vx = plr2.vx / spd2 * plr2.spd
            plr2.vy = plr2.vy / spd2 * plr2.spd


        if plr1.collision_cooldown <= 0 and plr2.collision_cooldown <= 0:
            if (plr1.clr != plr2.clr):
                Combat.DealDamage(plr1, plr2)
                Combat.DealDamage(plr2, plr1)

            plr1.collision_cooldown = 0.05
            plr2.collision_cooldown = 0.05
