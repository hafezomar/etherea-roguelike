# Etherea: Ashes of the Saints - Pocket Roguelike

Version v0.2.2.1 - Tutorial Exit and Tavern Rest Hotfix

## Overview

Etherea: Ashes of the Saints - Pocket Roguelike is a small offline Tkinter RPG inspired by my larger Minecraft Bedrock dark fantasy world, Etherea: Ashes of the Saints.

The project now begins at the playable Hollow Hearth Tavern. It is a safe hub where the player can speak to simple NPCs, read the Hollow Quill Notice, inspect the inheritance letter, use the Expedition Board, and leave for the current playable areas.

## Playable Areas

- Tutorial: The Hollow Road - a two-room introduction to movement, exits, traps, and combat
- Foundries and Forges - a three-room early-game expedition through abandoned industrial ruins
- Temple of the Sleepers: Blood Wing - the original late-game prototype with Vaelrith at the First Seal

Blood Wing remains late-game prototype content. The Deeper Well is still planned next and is registered with a blue water-and-stone theme, but it is not playable yet.

## Features

- Playable Hollow Hearth Tavern hub
- Interactable Tavern bed that restores HP, focus, and Blood Vials
- Tavern Keeper, Omar Hafez, Verdan Thorne, and Azael Vire dialogue interactions
- Inheritance Board and two-page Hollow Quill letter
- Expedition Board for tutorial, Foundries, Blood Wing, and planned areas
- Three classes: Warden, Ashen Blade, and Dreamseer
- Three difficulty modes: Pilgrim, Warden, and Martyr
- Zombie, Skeleton, and Goblin early-game enemies
- Existing Blood Wing enemies, relics, shrines, traps, save/load, and Vaelrith fight
- Lore Book, tutorial/help screen, World Progression, and safe menu back navigation
- Optional standard-library audio support for future WAV files
- Fullscreen with F11

## Project Structure

    etherea-pocket-roguelike/
    ├── main.py
    ├── README.md
    ├── CHANGELOG.md
    ├── game/
    │   ├── areas.py       # Campaign order, area status, and themes
    │   ├── audio.py       # Optional future WAV support
    │   ├── hub.py         # Tavern NPCs and inheritance text
    │   ├── lore.py        # Lore Book and menu content
    │   ├── map_data.py    # Tavern, tutorial, Foundries, and Blood Wing rooms
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
| F11 / Esc | Enter / leave fullscreen |

## Audio Notes

Audio is optional and safely disabled when unsupported. No sound files are included. On Windows, future WAV files can be placed in assets/audio/ with names such as tavern.wav, combat.wav, boss.wav, and click.wav.

## Tests

    python -m unittest discover -s tests -v
