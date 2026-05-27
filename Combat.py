from config import players, Abilities, SCREENX, SCREENY
from math import floor

def checkDistance(x1, x2, y1, y2, reqDist):
    dx = x2 - x1
    dy = y2 - y1
    dist_sq = dx**2 + dy**2

    return dist_sq <= (reqDist * (SCREENY))**2

def effectDoT(plr, dt):
    if (len(plr.DoTs) > 0):
        for effect, dot in list(plr.DoTs.items()):
            dot["tick"] -= dt
            if dot["tick"] <= 0:
                if (dot["type"] == "burn"):
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

def applyDoT(plrD, plrA, dmg, effect,tier):
    if (effect not in plrD.DoTs or (effect == "poison" or effect == "bfire")):
        Dot = Abilities[effect]
        if (effect in plrD.DoTs):
            plrD.DoTs[effect]["tier"] = min(plrD.DoTs[effect]["tier"] + 1, 7)
            plrD.DoTs[effect]["dmg"] = (dmg * plrD.DoTs[effect]["tier"] * 0.5 * Dot["dmg"]) / Dot["dura"]
            plrD.DoTs[effect]["dura"] = min(plrD.DoTs[effect]["dura"] + floor((Dot["dura"] / 2)), 60)
        else:
            newDoT = {"dmg": ((dmg * tier * Dot["dmg"]) / Dot["dura"]), "tick": Dot["tick"], "dura": Dot["dura"], "type": Dot["type"], "tier": tier, "attacker": plrA}
            plrD.DoTs[effect] = newDoT

def ultimateAttack(plr):
    if (plr.ult != "none"):
        if (plr.ult == "speed"):
            plr.spd += 100

def DealDamage(plr_attacker, plr_defender):
    if (plr_attacker.disabled == True or plr_defender.iframe == True):
        return 
    plr_attacker.ultmeter += 1
    if (plr_defender.armr >= 0 + plr_attacker.dmg):
        plr_defender.armr -= plr_attacker.dmg
    else:
        if ("bfire" in plr_defender.DoTs or "frost" in plr_defender.DoTs or "virus" in plr_defender.DoTs):
            plr_defender.hp -= plr_attacker.dmg * 1.2
        else:
            plr_defender.hp -= plr_attacker.dmg
    
    if ("static" in plr_attacker.DoTs and plr_defender.encht != "static"):
        for plr in players:
            if checkDistance(plr.x, plr_defender.x, plr.y, plr_defender.y, 200):
                applyDoT(plr, plr_attacker, plr_attacker.dmg, "static", 2)
                plr.hp -= plr_attacker.dmg * 0.6


    if ("virus" in plr_attacker.DoTs):
        if (plr_defender.encht != "virus"):
            applyDoT(plr_defender, plr_attacker, plr_attacker.dmg, "virus", 1)
        applyDoT(plr_attacker, plr_attacker, plr_attacker.dmg, "poison", 2)

    if (plr_attacker.encht != "none"):
        applyDoT(plr_defender, plr_attacker, plr_attacker.dmg, plr_attacker.encht ,plr_attacker.enTier)