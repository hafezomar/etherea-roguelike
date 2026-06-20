# Etherea: Ashes of the Saints - Pocket Roguelike

Version v0.2.1 - Tavern, Tutorial, and Lore Polish Update

## Overview

Etherea: Ashes of the Saints - Pocket Roguelike is a small offline Tkinter RPG inspired by my larger Minecraft Bedrock dark fantasy world, Etherea: Ashes of the Saints.

The Hollow Hearth Tavern acts as the hub between expeditions. It gives the prototype a place to begin without pretending that the current dungeon is the beginning of the full story.

The only playable expedition is Temple of the Sleepers: Blood Wing, a late-game prototype with four rooms, three classes, difficulty modes, relics, traps, shrines, save/load, and Vaelrith at the First Seal.

## Current Features

- Hollow Hearth Tavern hub with keyboard and click navigation
- Expedition Board listing the playable Blood Wing prototype and planned canon areas
- Tutorial / How to Play screen using the game's actual controls and systems
- Lore Book with Etherea, the Hollow Quill, the saints, the Temple, Blood Wing, and Vaelrith
- World Progression screen for the wider canon route
- Warden, Ashen Blade, and Dreamseer classes
- Pilgrim, Warden, and Martyr difficulty modes
- Tile-based combat, class abilities, relics, traps, shrines, and a shard shop
- Zombie and Skeleton enemy definitions prepared for future early-game areas
- JSON save/load with safe area metadata defaults
- Optional standard-library audio support for future WAV files
- Fullscreen toggle with F11

## Scope

Blood Wing remains a playable late-game prototype. The full Etherea route starts earlier with the Tutorial / Estate Intro, Foundries and Forges, and The Deeper Well. Those areas are listed on the Expedition Board and World Progression screen, but are not playable yet.

This project is being expanded through small updates instead of a large campaign rewrite. It is meant to practice Python OOP, Tkinter UI work, game state, combat systems, JSON save/load, data-driven content, and tests.

## Project Structure

    etherea-pocket-roguelike/
    ├── main.py
    ├── README.md
    ├── CHANGELOG.md
    ├── game/
    │   ├── areas.py       # Canon campaign registry
    │   ├── audio.py       # Optional future WAV support
    │   ├── lore.py        # Tavern and lore-book content
    │   ├── engine.py      # Tkinter UI, game flow, combat, save/load
    │   ├── map_data.py    # Blood Wing rooms and room metadata
    │   └── models.py      # Classes, enemies, and game data
    ├── assets/
    ├── saves/
    └── tests/

## How to Run

Python 3.10 or newer is recommended. The game uses Tkinter and the standard library only: no Pygame or external game framework is required.

    python main.py

If Python is not on your PATH:

    & "C:\Users\crazy\anaconda3\python.exe" main.py

## Main Controls

| Key | Action |
| --- | --- |
| Up / Down or W / S | Navigate tavern options |
| Enter | Confirm a menu option |
| Esc / Backspace | Return to the tavern from a menu screen |
| WASD or arrow keys | Move during an expedition |
| Space | Attack an adjacent enemy |
| Q | Use class ability |
| E | Use Blood Vial |
| R | Recover focus |
| B / L | Save / load |
| F11 / Esc | Enter / leave fullscreen |

## Audio Notes

Audio is optional and disabled safely when unsupported. No audio files are bundled. On Windows, future WAV files can be placed in assets/audio/ with names such as tavern.wav, combat.wav, boss.wav, and click.wav.

## Tests

    python -m unittest discover -s tests -v
