from config import players, Abilities, SCREENX, SCREENY, NamesDOT, global_speed
from math import floor
from random import randint

def checkDistance(x1, x2, y1, y2, reqDist):
    dx = x2 - x1
    dy = y2 - y1
    dist_sq = dx**2 + dy**2

    return dist_sq <= (reqDist * (SCREENY))**2

def effectDoT(plr, dt):
    if (len(plr.DoTs) > 0):
        for effect, dot in list(plr.DoTs.items()):
            dot["tick"] -= dt * global_speed
            if dot["tick"] <= 0:
                if (dot["type"] == "burn" and plr.armr > 0):
                    plr.armr -= dot["dmg"]
                else:
                    plr.hp -= dot["dmg"]
                
                dot["dura"] -= 1
                dot["tick"] = Abilities[effect]["tick"]

                if (effect == "leech"):
                    dot["attacker"].hp += dot["dmg"]

                if (dot["type"] == "freeze"):
                    if (dot["dura"] >= Abilities[effect]["dura"] / 2):
                        plr.pause = True
                        plr.disabled = True
                    else:
                        plr.pause = False
                        plr.disabled = False
                #if (dot["type"] == "chain"):
                    #plr.disabled = True

            if dot["dura"] <= 0:
                del plr.DoTs[effect]
                plr.pause = False
                plr.disabled = False
    else:
        plr.DoTs = {}
        plr.pause = False
        plr.disabled = False

def applyDoT(plrD, plrA, dmg, effect,tier, stack):
    if (effect not in plrD.DoTs or (effect == "poison" or effect == "bfire") or stack == True):
        Dot = Abilities[effect]
        if (effect in plrD.DoTs):
            plrD.DoTs[effect]["tier"] = min(plrD.DoTs[effect]["tier"] + 1, 7)
            plrD.DoTs[effect]["dmg"] = (dmg * plrD.DoTs[effect]["tier"] * 0.5 * Dot["dmg"]) / Dot["dura"]
            plrD.DoTs[effect]["dura"] = min(plrD.DoTs[effect]["dura"] + floor((Dot["dura"] / 2)), 60)
        else:
            newDoT = {"dmg": ((dmg * tier * Dot["dmg"]) / Dot["dura"]), "tick": Dot["tick"], "dura": Dot["dura"], "type": Dot["type"], "tier": tier, "attacker": plrA}
            plrD.DoTs[effect] = newDoT

def ultimateAttack(plr, dt):
        if (plr.encht == "fire"):
            if (plr.ult_dura <= 0 and plr.ult == False):
                plr.enTier += 2
                plr.dmg *= 2
                plr.tick = 1

                plr.ult = True
                plr.ult_dura = 10
                plr.tick = 1
            elif (plr.ult_dura > 0 and plr.ult == True):
                plr.ult_dura -= dt
                plr.tick -= dt
                if plr.tick <= 0:
                    plr.tick = 1
                    for plrx in players:
                        if (plrx.encht != "fire" and checkDistance(plrx.x, plr.x, plrx.y, plr.y, (plrx.r * 4))):
                            applyDoT(plrx, plr, plr.dmg, "fire", 2, True)
                            print("found ball " + plrx.encht)
                            plrx.hp -= plr.dmg * 0.5

            elif (plr.ult_dura <= 0 and plr.ult == True):
                plr.enTier -= 2
                plr.dmg = plr.dmg / 2

                plr.ult = False
                plr.ultmeter = 0
                plr.tick = 1
                plr.ult_dura = 0



def elementAdvantages(plr_defender, plr_attacker):
    if (plr_defender.armr <= 0):
         if ("bfire" in plr_defender.DoTs or "frost" in plr_defender.DoTs or "virus" in plr_defender.DoTs):
            plr_defender.hp -= plr_attacker.dmg * 0.2

    if ("static" in plr_attacker.DoTs and plr_defender.encht != "static"):
        for plr in players:
            if plr.encht != "static" and checkDistance(plr.x, plr_defender.x, plr.y, plr_defender.y, (plr.r * 3)):
                applyDoT(plr, plr_attacker, plr_attacker.dmg, "static", 1, False)
                plr.hp -= plr_attacker.dmg * 0.2

    if ("virus" in plr_attacker.DoTs):
        if (plr_defender.encht != "virus"):
            applyDoT(plr_defender, plr_attacker, plr_attacker.dmg, "virus", 1, False)
        applyDoT(plr_attacker, plr_attacker, plr_attacker.dmg, "poison", 1, False)

def DealDamage(plr_attacker, plr_defender):
    if (plr_attacker.disabled == True or plr_defender.iframe == True):
        return 
    
    if (plr_attacker.ultmeter < 100):
        plr_attacker.ultmeter += 10

    if (plr_defender.armr >= 0 + plr_attacker.dmg):
        plr_defender.armr -= plr_attacker.dmg
    else:
        plr_defender.hp -= plr_attacker.dmg

    elementAdvantages(plr_defender, plr_attacker)

    if (plr_attacker.encht != "none" and plr_attacker.encht != "mage"):
        applyDoT(plr_defender, plr_attacker, plr_attacker.dmg, plr_attacker.encht ,plr_attacker.enTier, False)
    elif (plr_attacker.encht == "mage"):
        applyDoT(plr_defender, plr_attacker, plr_attacker.dmg + randint(-5, 5), NamesDOT[randint(0, 6)], randint(1, 7), True)