# Etherea: Ashes of the Saints - Pocket Roguelike

Version v0.3.1 - Equipment Asset Pass

## Overview

Etherea: Ashes of the Saints - Pocket Roguelike is a small offline Tkinter RPG inspired by my larger Minecraft Bedrock dark fantasy world, Etherea: Ashes of the Saints.

The project now begins at the playable Hollow Hearth Tavern. It is a safe hub where the player can speak to simple NPCs, read the Hollow Quill Notice, inspect the inheritance letter, use the Expedition Board, and leave for the current playable areas.

## Playable Areas

- Tutorial: The Hollow Road - a three-room introduction to movement, exits, traps, shrines, and combat
- Foundries and Forges - a four-room early-game expedition through abandoned industrial ruins
- The Deeper Well - a five-room blue-water descent beneath the Foundries
- Temple of the Sleepers: Blood Wing - the original late-game prototype with Vaelrith at the First Seal

Blood Wing remains late-game prototype content. The Deeper Well is the newest playable early-game expedition.

## Features

- Playable Hollow Hearth Tavern hub
- Interactable Tavern bed that restores HP, focus, and Blood Vials
- Tavern Keeper, Omar Hafez, Verdan Thorne, and Azael Vire dialogue interactions
- Inheritance Board and two-page Hollow Quill letter
- Expedition Board for tutorial, Foundries, Blood Wing, and planned areas
- Equipment inventory with Helmet, Chestplate, Pants, Greaves, Boots, and Weapon slots
- Equipment icons linked from the included manifest for starter and reward gear
- Area reward gear and a Tavern shop for upgrading Blood Vial capacity to 3
- Enemy health bars and refreshed Blood Vials after each completed expedition
- Three classes: Warden, Ashen Blade, and Dreamseer
- Three difficulty modes: Pilgrim, Warden, and Martyr
- Zombie, Skeleton, and Goblin early-game enemies
- Existing Blood Wing enemies, relics, shrines, traps, save/load, and Vaelrith fight
- Lore Book, tutorial/help screen, World Progression, and safe menu back navigation
- Tavern ambience through the included MP3 on Windows
- Fullscreen with F11

## Project Structure

    etherea-pocket-roguelike/
    ├── main.py
    ├── README.md
    ├── CHANGELOG.md
    ├── game/
    │   ├── areas.py       # Campaign order, area status, and themes
    │   ├── audio.py       # Windows Tavern MP3 playback
    │   ├── hub.py         # Tavern NPCs and inheritance text
    │   ├── lore.py        # Lore Book and menu content
    │   ├── map_data.py    # Tavern, tutorial, Foundries, Deeper Well, and Blood Wing rooms
    │   ├── engine.py      # Tkinter UI, game flow, combat, save/load
    │   └── models.py      # Classes, enemies, and data models
    ├── assets/
    ├── saves/
    └── tests/

## How to Run

Python 3.10 or newer is recommended. This is a Tkinter-only project: no Pygame or external game library is required.

    python main.py

If Python is not on your PATH, use your Python executable directly.

## Controls

| Key | Action |
| --- | --- |
| Up / Down or W / S | Navigate menus |
| Enter | Confirm a menu option |
| Esc / Backspace | Return from safe menu screens |
| WASD or arrow keys | Move during an expedition |
| Space | Attack an adjacent enemy |
| Q | Use class ability |
| E | Use Blood Vial |
| R | Recover focus |
| F | Interact with Tavern objects/NPCs or use an exit tile |
| B / L | Save / load |
| I | Open inventory |
| F11 / Esc | Enter / leave fullscreen |

## Audio Notes

Tavern ambience is included as `assets/audio/tavern.mp3`. It starts on launch, pauses when an expedition begins, and returns when you reach the Tavern.

## Tests

    python -m unittest discover -s tests -v
