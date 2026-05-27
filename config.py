players = []

Abilities = {"fire" : {"dmg": 0.7, "type": "burn", "tick": 1, "dura" : 7},
        "bfire" : {"dmg": 2, "type": "burn", "tick": 0.5, "dura": 7},
        "poison" : {"dmg": 0.6, "type": "poison", "tick": 1, "dura": 10},
        "virus" : {"dmg": 0.1, "type": "chain", "tick": 1, "dura": 20},
        "frost" : {"dmg": 0.5, "type": "freeze", "tick": 0.5, "dura": 6},
        "static" : {"dmg": 1, "type": "chain", "tick": 0.5, "dura": 3},
        "leech" : {"dmg": 0.6, "type": "leech", "tick": 0.5, "dura": 1},
}

BASE_WIDTH, BASE_HEIGHT = 1280, 720
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

SCREENX = (SCREEN_WIDTH / BASE_WIDTH)
SCREENY = (SCREEN_HEIGHT / BASE_HEIGHT)