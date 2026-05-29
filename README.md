# Ball fighting simulator
A simple project about balls fighting eachother by colliding with fun damage, armour and enchantment systems. Something I saw people do in videos and thought it'll be a good starter project idea to upskill. This is my first ever gitHub project, starting 2026. Start of 12th grade.

## How to play
Right now this isn't an executable so you'll have to run it manually through visual studios or any code editor you have. You also need to have pygame installed in order to run it (for now).

## Version
This project uses Python 3.12.6 and pygame-ce 2.5.7

## Features
- Ball physics and collision between balls and screen.
- Health points and armor indications.
- Multiple balls.
- Burn damage balls, freezing balls, virus infecting balls, poison balls, etc.
- DoT stacking balls.
- Resolution scaling (settings coming soon).
- DoT indicators

### Performance Notes
- Naive collision resolution (every frame) caused FPS drops to ~25 with 80 balls.
- Optimized by checking collisions every 3 frames → stable 166+ FPS.
- Demonstrates trade‑off between simulation accuracy and performance.