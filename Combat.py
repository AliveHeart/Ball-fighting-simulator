Abilities = {"fire" : {"dmg": 0.7, "type": "burn", "tick": 1, "dura" : 7},
        "bfire" : {"dmg": 2, "type": "burn", "tick": 0.5, "dura": 7},
        "poison" : {"dmg": 1, "type": "burn", "tick": 1, "dura": 10},
        "virus" : {"dmg": 1, "type": "burn", "tick": 1, "dura": 20},
        "frost" : {"dmg": 0.5, "type": "freeze", "tick": 0.5, "dura": 6},
}

def effectDoT(plr, dt):
    if (len(plr.DoTs) > 0):
        for effect, dot in list(plr.DoTs.items()):
            dot["tick"] -= dt
            if dot["tick"] <= 0:
                plr.hp -= dot["dmg"]
                dot["dura"] -= 1
                dot["tick"] = Abilities[effect]["tick"]

                if (dot["type"] == "freeze"):
                    if (dot["dura"] >= Abilities[effect]["dura"] / 2):
                        plr.pause = True
                        plr.disabled = True
                    else:
                        plr.pause = False
                        plr.disabled = False

            if dot["dura"] <= 0:
                del plr.DoTs[effect]
                plr.pause = False
                plr.disabled = False
    else:
        plr.DoTs = {}

def applyDoT(plrD, dmg, effect,tier):
    if (effect not in plrD.DoTs or (effect == "poison" or effect == "bfire")):
        Dot = Abilities[effect]
        if (effect in plrD.DoTs):
            plrD.DoTs[effect]["tier"] = min(plrD.DoTs[effect]["tier"] + 1, 7)
            plrD.DoTs[effect]["dmg"] = (dmg * plrD.DoTs[effect]["tier"] * Dot["dmg"]) / Dot["dura"]
            plrD.DoTs[effect]["dura"] += Dot["dura"]
            print(f"upgraded {effect} by tier " + str(tier) + " and duration " + str(plrD.DoTs[effect]["dura"]))
        else:
            newDoT = {"dmg": ((dmg * tier * Dot["dmg"]) / Dot["dura"]), "tick": Dot["tick"], "dura": Dot["dura"], "type": Dot["type"], "tier": tier}
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
    
    if ("virus" in plr_attacker.DoTs):
        if (plr_defender.encht != "virus"):
            applyDoT(plr_defender, plr_attacker.dmg, "virus", 1)
        applyDoT(plr_attacker, plr_attacker.dmg, "poison", 2)

    if (plr_attacker.encht != "none"):
        applyDoT(plr_defender, plr_attacker.dmg, plr_attacker.encht ,plr_attacker.enTier)