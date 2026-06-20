"""Campaign metadata for Etherea: Ashes of the Saints."""

CAMPAIGN_VERSION = "v0.2.2 - Playable Tavern and Foundries Update"

AREA_REGISTRY = {
    "tavern": {
        "name": "The Hollow Hearth Tavern",
        "status": "hub",
        "order": 0,
        "theme": "warm_dark_gold",
        "description": "A safe hearth between expeditions, where maps and old debts wait beside the fire.",
    },
    "tutorial_estate": {
        "name": "Tutorial: The Hollow Road",
        "status": "playable",
        "order": 1,
        "theme": "neutral_dark_road",
        "description": "The Hollow Quill called you home, but inheritance in Etherea is rarely a gift.",
    },
    "foundries_and_forges": {
        "name": "Foundries and Forges",
        "status": "playable",
        "order": 2,
        "theme": "red_orange_forge",
        "description": "The Foundries still breathe below the old kingdom, though no living smith remains.",
    },
    "deeper_well": {
        "name": "The Deeper Well",
        "status": "planned",
        "order": 3,
        "theme": "blue_dark_water_stone",
        "description": "It was not dug for water, but to bury what the saints could not name.",
    },
    "saint_admus_castle": {
        "name": "Saint Admus' Castle",
        "status": "planned",
        "order": 4,
        "theme": "cold_stone",
        "description": "A hereditary fortress where devotion outlived the people who built it.",
    },
    "etherean_cathedral": {
        "name": "Etherean Cathedral",
        "status": "planned",
        "order": 5,
        "theme": "sacred_ruin",
        "description": "The old faith remains standing, even after its saints have gone silent.",
    },
    "saint_magnus_laboratory": {
        "name": "Saint Magnus / Alchemical Laboratory",
        "status": "planned",
        "order": 6,
        "theme": "alchemy_green",
        "description": "Sacred study curdled into experiment beneath the saint's sealed chambers.",
    },
    "sacred_barbarian_forest": {
        "name": "Sacred Forest / Barbarian Forest",
        "status": "planned",
        "order": 7,
        "theme": "forest_ash",
        "description": "A borderland where older rites survived beneath the ruined kingdom.",
    },
    "hall_of_court": {
        "name": "Hall of Court",
        "status": "planned",
        "order": 8,
        "theme": "court_marble",
        "description": "The dead court still keeps its records, its debts, and its accusations.",
    },
    "throne_room": {
        "name": "Throne Room",
        "status": "planned",
        "order": 9,
        "theme": "royal_decay",
        "description": "A seat of rule left hollow by bloodline, silence, and old vows.",
    },
    "gate_of_hell": {
        "name": "Gate of Hell",
        "status": "planned",
        "order": 10,
        "theme": "hellfire",
        "description": "A threshold the kingdom named only after it had already opened.",
    },
    "castle_of_vaalmurth": {
        "name": "Castle of Vaalmurth",
        "status": "planned",
        "order": 11,
        "theme": "black_stone",
        "description": "The old castle watches over a legacy that refuses to die quietly.",
    },
    "ashen_forest": {
        "name": "Ashen Forest",
        "status": "planned",
        "order": 12,
        "theme": "ashen_forest",
        "description": "The trees remember the fire, even where the ash has long since settled.",
    },
    "temple_of_sleepers": {
        "name": "Temple of the Sleepers",
        "status": "planned",
        "order": 13,
        "theme": "sleeping_stone",
        "description": "A sacred refuge turned inward, built around seals that should never have been disturbed.",
    },
    "blood_wing": {
        "name": "Temple of the Sleepers: Blood Wing",
        "status": "playable_prototype",
        "order": 14,
        "theme": "crimson_blood",
        "description": "A late-game Temple trial of blood seals, corrupted pilgrims, and Vaelrith, Herald of the First Seal.",
    },
    "purgatory": {
        "name": "Purgatory",
        "status": "planned",
        "order": 15,
        "theme": "pale_ash",
        "description": "A place between judgment and return, where the faithful wait without relief.",
    },
    "crystalline_dimension": {
        "name": "Crystalline Dimension",
        "status": "planned",
        "order": 16,
        "theme": "crystalline_void",
        "description": "A final fracture beyond Etherea, where form and memory no longer agree.",
    },
}


def campaign_areas() -> list[tuple[str, dict[str, object]]]:
    return sorted(AREA_REGISTRY.items(), key=lambda item: int(item[1]["order"]))
