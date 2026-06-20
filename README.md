# Etherea: Ashes of the Saints - Pocket Roguelike

## Overview

This is a small offline Tkinter roguelike inspired by my larger Minecraft Bedrock dark fantasy RPG project, Etherea: Ashes of the Saints.

The current playable content is **Temple of the Sleepers: Blood Wing**, a four-room late-game prototype with class selection, difficulty modes, relics, traps, shrines, save/load, and Vaelrith at the First Seal. It is a compact systems project, not a replacement for the Minecraft version or a full campaign.

## Campaign Foundation

Blood Wing is not the beginning of Etherea's canon progression. The larger route starts with the Tutorial / Estate Intro, continues through the Foundries and Forges and the Deeper Well, and reaches the Temple of the Sleepers much later.

Version v0.2.0 adds an in-game campaign registry and World Progression screen. The planned areas are metadata only for now; Blood Wing remains the only playable area.

## Current Features

- Three playable classes: Warden, Ashen Blade, and Dreamseer
- Three difficulty modes: Pilgrim, Warden, and Martyr
- Tile-based combat, enemy turns, class abilities, relics, traps, shrines, and a shard shop
- Four Blood Wing rooms ending with Vaelrith, Herald of the First Seal
- Save/load with safe defaults for future area-based content
- World Progression view showing the wider Etherea route
- Original class and enemy art rendered through Tkinter
- Fullscreen toggle with F11
- Unit tests for game systems, saves, room data, and campaign metadata

## Project Structure

    etherea-blood-wing/
    ├── main.py
    ├── CHANGELOG.md
    ├── game/
    │   ├── areas.py       # Canon campaign registry
    │   ├── engine.py      # Tkinter UI, game flow, combat, save/load
    │   ├── map_data.py    # Blood Wing rooms and room metadata
    │   └── models.py      # Game data models and enums
    ├── assets/
    ├── saves/
    └── tests/

## How to Run

Python 3.10 or newer is recommended. Tkinter is included with standard Windows Python installations.

    python main.py

If Python is not on your PATH:

    & "C:\Users\crazy\anaconda3\python.exe" main.py

## Controls

| Key | Action |
| --- | --- |
| 1 / Enter | Start the Blood Wing late-game prototype |
| 2 / W | Open World Progression from the demo select |
| WASD or arrow keys | Move / navigate menus |
| Space | Attack |
| Q | Class ability |
| E | Use Blood Vial |
| R | Recover focus |
| B / L | Save / load |
| F11 / Esc | Enter / leave fullscreen |

## Systems Practiced

This project is meant to practice Python OOP, Tkinter UI work, game state, combat logic, JSON save/load, tests, and modular content design. It uses only the Python standard library and Tkinter: no Pygame or external game framework.

## Scope

This update deliberately does not add the Foundries, Deeper Well, or a large campaign. Those areas exist as structured campaign metadata so future updates can add them gradually without reframing Blood Wing as the first level.
