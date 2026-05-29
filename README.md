# 🎮 Ball fighting simulator
A simple Python + Pygame project simulating balls with physics, collisions and status effects.
Built as my first ever GitHub project (2026, start of my 12th grade), a start of my journey of exploring **game physics, optimization, and system design**.

## 🚀 Features
- ⚔️ Ball physics & collision resolution. 
- 🛡️ Health, armor, and damage systems.
- 🔥 Status effects: burn, freeze, poison, virus, stacking DoT.
- 🎨 Resolution scaling & settings menu.
- 📊 Performance optimization (60+ FPS with 200+ balls).

### 📈 Performance Notes
- Naive collision resolution (every frame) caused FPS drops to ~25 with 80 balls.
- Optimized by checking collisions every 4 frames → stable 166+ FPS.
- Demonstrates trade‑off between simulation accuracy and performance.

## 🛠️ Tech Stack
- **Language:** Python 3.12.6
- **Library:** pygame-ce 2.5.7

## 🎯 Why this project matters?
This project showcases
- Understanding of **physics simulation** and **collision detection**.
- Implementation of game mechanics (armor, status effects, advantages, etc).
- Practical **optimization strategies** for real-time systems.
- Ability to document and present work professionally.

## How to run
1. Install [pygame-ce](https://pypi.org/project/pygame-ce/)
2. Download this repo
3. Run **'Main.py'** with python