players = []

NamesDOT = ["fire", "bfire", "poison", "virus", "frost", "static", "leech"]

Abilities = {"fire" : {"dmg": 0.7, "type": "burn", "tick": 1, "dura" : 7},
        "bfire" : {"dmg": 2, "type": "burn", "tick": 0.5, "dura": 7},
        "poison" : {"dmg": 0.6, "type": "poison", "tick": 1, "dura": 7},
        "virus" : {"dmg": 0.1, "type": "chain", "tick": 1, "dura": 15},
        "frost" : {"dmg": 0.3, "type": "freeze", "tick": 0.5, "dura": 4},
        "static" : {"dmg": 1, "type": "chain", "tick": 1, "dura": 2},
        "leech" : {"dmg": 0.4, "type": "leech", "tick": 0.25, "dura": 1},
}

BASE_WIDTH, BASE_HEIGHT = 1280, 720
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

global_speed = 1

SCREENX = (SCREEN_WIDTH / BASE_WIDTH)
SCREENY = (SCREEN_HEIGHT / BASE_HEIGHT)