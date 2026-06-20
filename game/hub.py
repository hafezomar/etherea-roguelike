"""Small data definitions for the playable Hollow Hearth Tavern."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NPC:
    id: str
    name: str
    title: str
    position: tuple[int, int]
    dialogue: tuple[str, ...]


TAVERN_NPCS = (
    NPC(
        "keeper",
        "Tavern Keeper",
        "Hollow Hearth Host",
        (3, 3),
        (
            "Welcome to the Hollow Hearth. Roads die outside these walls, but maps still remember them.",
            "Use the Expedition Board when you are ready. The Blood Wing is no place for a fresh soul, but this prototype lets you face it early.",
            "Start with the Tutorial if your blade hand is uncertain.",
        ),
    ),
    NPC(
        "omar_hafez",
        "Omar Hafez",
        "Creator of Etherea",
        (14, 3),
        (
            "I built this world one ruin at a time. Some doors are finished. Some are still only promises.",
            "The Blood Wing belongs near the end of the journey, but prototypes are strange things. They let you glimpse the future early.",
            "Do not judge the kingdom by one room. Etherea is larger than what stands before you.",
        ),
    ),
    NPC(
        "verdan_thorne",
        "Verdan Thorne",
        "Keeper of Beasts",
        (3, 8),
        (
            "Every beast leaves a record. Teeth, claw marks, blood patterns... all of it speaks.",
            "One day, I will keep a proper bestiary for you. For now, survive long enough to give me something to write down.",
            "False Pilgrims, Overseers, Sealbound Knights... names matter. A named horror is easier to face than an unknown one.",
        ),
    ),
    NPC(
        "azael_vire",
        "Azael Vire",
        "Blade for Hire",
        (14, 8),
        (
            "Coin buys steel. Trust costs more.",
            "If companions ever join your road, remember this: the quiet ones usually live longer.",
            "I know names in the dark. Not all of them are enemies. Not all of them are friends.",
        ),
    ),
)

INHERITANCE_NOTICE = (
    "THE HOLLOW QUILL NOTICE\n\n"
    "Etherea was once a kingdom of saints, courts, foundries, forests, and sealed temples.\n\n"
    "You were called back through inheritance. Not glory. Not duty. Inheritance.\n\n"
    "A forgotten estate bears your blood. A sealed letter bears your name. Somewhere beneath the ruined kingdom, old debts still recognize you.\n\n"
    "The Hollow Quill wrote first.\n\n"
    "Your inheritance was not land.\nIt was the wound beneath it.\n\n"
    "The Foundries and Forges are where the road should truly begin. The Blood Wing is one of the late paths."
)

HOLLOW_QUILL_LETTER = (
    "A LETTER FROM THE HOLLOW QUILL\n\n"
    "To the heir of a house the kingdom tried to forget,\n\n"
    "Your name has returned to our records.\n\n"
    "The estate east of the old road has remained sealed beyond the memory of most men, but blood does not forget what stone refuses to say.\n\n"
    "You have inherited more than walls.\n\n"
    "Beneath the land lies a debt older than your family, older than the court, older perhaps than the saints who blessed this kingdom into ruin.\n\n"
    "Come to Etherea. Claim what was left to you.\n\n"
    "Your inheritance was not land.\nIt was the wound beneath it.\n\n"
    "- The Hollow Quill"
)
