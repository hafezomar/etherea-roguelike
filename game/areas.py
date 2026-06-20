"""Campaign metadata for Etherea: Ashes of the Saints."""

CAMPAIGN_VERSION = "v0.2.1 - Tavern, Tutorial, and Lore Polish Update"

AREA_REGISTRY = {
    "tutorial_estate": {
        "name": "Tutorial / Estate Intro",
        "status": "planned",
        "order": 1,
        "description": "The Hollow Quill called you home, but inheritance in Etherea is rarely a gift.",
    },
    "foundries_and_forges": {
        "name": "Foundries and Forges",
        "status": "planned",
        "order": 2,
        "description": "The Foundries still breathe below the old kingdom, though no living smith remains.",
    },
    "deeper_well": {
        "name": "The Deeper Well",
        "status": "planned",
        "order": 3,
        "description": "It was not dug for water, but to bury what the saints could not name.",
    },
    "saint_admus_castle": {
        "name": "Saint Admus' Castle",
        "status": "planned",
        "order": 4,
        "description": "A hereditary fortress where devotion outlived the people who built it.",
    },
    "etherean_cathedral": {
        "name": "Etherean Cathedral",
        "status": "planned",
        "order": 5,
        "description": "The old faith remains standing, even after its saints have gone silent.",
    },
    "saint_magnus_laboratory": {
        "name": "Saint Magnus / Alchemical Laboratory",
        "status": "planned",
        "order": 6,
        "description": "Sacred study curdled into experiment beneath the saint's sealed chambers.",
    },
    "sacred_barbarian_forest": {
        "name": "Sacred Forest / Barbarian Forest",
        "status": "planned",
        "order": 7,
        "description": "A borderland where older rites survived beneath the ruined kingdom.",
    },
    "hall_of_court": {
        "name": "Hall of Court",
        "status": "planned",
        "order": 8,
        "description": "The dead court still keeps its records, its debts, and its accusations.",
    },
    "throne_room": {
        "name": "Throne Room",
        "status": "planned",
        "order": 9,
        "description": "A seat of rule left hollow by bloodline, silence, and old vows.",
    },
    "gate_of_hell": {
        "name": "Gate of Hell",
        "status": "planned",
        "order": 10,
        "description": "A threshold the kingdom named only after it had already opened.",
    },
    "castle_of_vaalmurth": {
        "name": "Castle of Vaalmurth",
        "status": "planned",
        "order": 11,
        "description": "The old castle watches over a legacy that refuses to die quietly.",
    },
    "ashen_forest": {
        "name": "Ashen Forest",
        "status": "planned",
        "order": 12,
        "description": "The trees remember the fire, even where the ash has long since settled.",
    },
    "temple_of_sleepers": {
        "name": "Temple of the Sleepers",
        "status": "planned",
        "order": 13,
        "description": "A sacred refuge turned inward, built around seals that should never have been disturbed.",
    },
    "blood_wing": {
        "name": "Temple of the Sleepers: Blood Wing",
        "status": "playable_prototype",
        "order": 14,
        "description": "A late-game Temple trial of blood seals, corrupted pilgrims, and Vaelrith, Herald of the First Seal.",
    },
    "purgatory": {
        "name": "Purgatory",
        "status": "planned",
        "order": 15,
        "description": "A place between judgment and return, where the faithful wait without relief.",
    },
    "crystalline_dimension": {
        "name": "Crystalline Dimension",
        "status": "planned",
        "order": 16,
        "description": "A final fracture beyond Etherea, where form and memory no longer agree.",
    },
}


def campaign_areas() -> list[tuple[str, dict[str, object]]]:
    return sorted(AREA_REGISTRY.items(), key=lambda item: int(item[1]["order"]))
