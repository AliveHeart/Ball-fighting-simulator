import math

def effectDoT(plr, dt):
    if (plr.DoT_dura > 0):
        plr.DoT_tick -= dt
        if (plr.DoT_tick < 0):
            plr.hp -= plr.DoT_dmg
            plr.DoT_dura -= 1
            plr.DoT_tick = 1
    else:
        plr.DoT_dura = 0
        plr.DoT_tick = 1
        plr.DoT_dmg = 0

def applyDoT(plrD, dmg, tier):
    if (plrD.DoT_dura <= 0):
        plrD.DoT_tick = 1
        plrD.DoT_dura = 5 * tier
        plrD.DoT_dmg = (dmg * tier) / 5

def DealDamage(plr_attacker, plr_defender):
    if (plr_defender.armr >= 0 + plr_attacker.dmg):
        plr_defender.armr -= plr_attacker.dmg
    else:
        plr_defender.hp -= plr_attacker.dmg
    
    if (plr_attacker.encht == "fire"):
        applyDoT(plr_defender, plr_attacker.dmg, plr_attacker.enTier)