import math

Abilities = {"fire" : {"dmg": 0.7, "type": "burn", "tick": 1, "dura" : 7},
        "bfire" : {"dmg": 2, "type": "burn", "tick": 0.5, "dura": 7},
        "poison" : {"dmg": 1, "type": "burn", "tick": 1, "dura": 10},
}

def effectDoT(plr, dt):
    if (len(plr.DoTs) > 0):
        for effect, dot in list(plr.DoTs.items()):
            dot["tick"] -= dt
            if dot["tick"] <= 0:
                plr.hp -= dot["dmg"] / dot["dura"]
                dot["dura"] -= 1
                dot["tick"] = Abilities[effect]["tick"] 

            if dot["dura"] <= 0:
                del plr.DoTs[effect]
    else:
        plr.DoTs = {}

def applyDoT(plrD, dmg, effect,tier):
    if (effect not in plrD.DoTs):
        Dot = Abilities[effect]
        newDoT = {"dmg": (dmg * tier * Dot["dmg"]), "tick": Dot["tick"], "dura": Dot["dura"]}
        plrD.DoTs[effect] = newDoT


def DealDamage(plr_attacker, plr_defender):
    if (plr_defender.armr >= 0 + plr_attacker.dmg):
        plr_defender.armr -= plr_attacker.dmg
    else:
        plr_defender.hp -= plr_attacker.dmg
    
    if (plr_attacker.encht != "none"):
        applyDoT(plr_defender, plr_attacker.dmg, plr_attacker.encht ,plr_attacker.enTier)