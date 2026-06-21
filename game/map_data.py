"""
Etherea: Blood Wing — Map Data
Hand-designed room layouts, metadata, and tile definitions.
Each room is an 18-wide × 12-tall grid of characters.
Tile legend:
  #  wall           .  floor          ~  blood trap
  !  reliquary      †  saint shrine   >  gold exit
  @  player start   P  False Pilgrim  O  Overseer
  K  Sealbound Knight   B  Bloodbound Pilgrim   V  Vaelrith
"""
# ═══════════════════════════════════════════════════════════════
# ENEMY MARKERS — maps grid characters to enemy type ids
# ═══════════════════════════════════════════════════════════════
ENEMY_MARKERS = {
    "Z": "zombie",
    "S": "skeleton",
    "G": "goblin",
    "P": "false_pilgrim",
    "O": "overseer",
    "K": "sealbound_knight",
    "B": "bloodbound_pilgrim",
    "V": "vaelrith",
}
# ═══════════════════════════════════════════════════════════════
# ROOM LAYOUTS — 18 × 12 character grids
# ═══════════════════════════════════════════════════════════════
ROOMS = [
    # ── Room 0: Blood-Worn Entrance ──────────────────────────
    [
        "##################",
        "#.......~...!....#",
        "#................#",
        "#.P.........†....#",
        "#................#",
        "#....~...........#",
        "#................#",
        "#.@..........P...#",
        "#................#",
        "#..~.........P...#",
        "#................>",
        "##################",
    ],
    # ── Room 1: Hall of Sleeping Chains ──────────────────────
    [
        "##################",
        "#....#.....#.....#",
        "#....#.~...#.....#",
        "#....#.....#..†..#",
        "#.@..#.....#.....#",
        "#....#...........#",
        "#..........O.....#",
        "#....~...........#",
        "#...........#....#",
        "#...........#..K.#",
        "#..~........#....>",
        "##################",
    ],
    # ── Room 2: Ritual Combat Chamber ────────────────────────
    [
        "##################",
        "#................#",
        "#..#..........#..#",
        "#..#....B.....#..#",
        "#................#",
        "#.....~..~.......#",
        "#................#",
        "#..@.........O...#",
        "#..#..........#..#",
        "#..#....!.....#..#",
        "#..........~.....>",
        "##################",
    ],
    # ── Room 3: First Seal Arena ─────────────────────────────
    [
        "##################",
        "#................#",
        "#................#",
        "#......†.........#",
        "#................#",
        "#................#",
        "#........V.......#",
        "#................#",
        "#................#",
        "#................#",
        "#..@.............#",
        "##################",
    ],
]
# ═══════════════════════════════════════════════════════════════
# ROOM METADATA
# ═══════════════════════════════════════════════════════════════
ROOM_META = [
    {
        "name": "Blood-Worn Entrance",
        "subtitle": (
            "The first stones of the Blood Wing remember "
            "every pilgrim who turned back too late."
        ),
        "objective": "Defeat all enemies to unlock the exit.",
    },
    {
        "name": "Hall of Sleeping Chains",
        "subtitle": (
            "The chains do not move, but their shadows "
            "reach for the floor beneath your feet."
        ),
        "objective": "Defeat all enemies to unlock the exit.",
    },
    {
        "name": "Ritual Combat Chamber",
        "subtitle": (
            "A red seal has been carved into the floor. "
            "The old ritual still expects an answer."
        ),
        "objective": "Defeat all enemies to unlock the exit.",
    },
    {
        "name": "First Seal Arena",
        "subtitle": (
            "The seal opens like an eye. "
            "Vaelrith has been waiting beneath it."
        ),
        "objective": "Defeat Vaelrith, Herald of the First Seal.",
    },
]


TAVERN_ROOMS = [
    [
        "##################",
        "#................#",
        "#.....h..........#",
        "#..n..........n..#",
        "#................#",
        "#......e.....s...#",
        "#................#",
        "#....l.....i.....#",
        "#..n..........n..#",
        "#..........@.....#",
        "#....b...........#",
        "##################",
    ],
]

TAVERN_META = [
    {
        "name": "The Hollow Hearth Tavern",
        "subtitle": "The fire burns low. Maps, sealed letters, and old relics wait across the table.",
        "objective": "Press F near the board, bookshelf, notice, bed, or a tavern guest.",
    },
]

TUTORIAL_ROOMS = [
    [
        "##################",
        "#@...............#",
        "#....!...........#",
        "#................#",
        "#..............>.#",
        "#................#",
        "#................#",
        "#................#",
        "#................#",
        "#................#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#....Z...........#",
        "#......~.........#",
        "#................#",
        "#..........S.....#",
        "#......!.........#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@....†..........#",
        "#................#",
        "#....Z....!......#",
        "#................#",
        "#.......~........#",
        "#..........G.....#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
]

TUTORIAL_META = [
    {
        "name": "The Returned Path",
        "subtitle": "The road to Etherea begins beneath an overcast sky.",
        "objective": "Move, inspect the reliquary, and reach the exit.",
    },
    {
        "name": "Grave of First Steps",
        "subtitle": "The first dead rise slowly, as if remembering how to walk.",
        "objective": "Defeat the Zombie and Skeleton, then take the exit home.",
    },
    {
        "name": "Estate Chapel Ruin",
        "subtitle": "A small altar remains where the old road gives way to the forges.",
        "objective": "Use the shrine if needed, clear the risen dead, and return home.",
    },
]

FOUNDRIES_ROOMS = [
    [
        "##################",
        "#@...............#",
        "#....Z...........#",
        "#................#",
        "#......!.........#",
        "#................#",
        "#................#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#......~.........#",
        "#....S...........#",
        "#................#",
        "#..........G.....#",
        "#........~.......#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#....G...........#",
        "#..........Z.....#",
        "#................#",
        "#......S.........#",
        "#........~.......#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@....†..........#",
        "#................#",
        "#....Z.......G...#",
        "#................#",
        "#........~.......#",
        "#......S.....!...#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
]

FOUNDRIES_META = [
    {
        "name": "Cold Anvil Gate",
        "subtitle": "The forges no longer burn for kings. They breathe for something buried beneath them.",
        "objective": "Clear the gate and continue into the Foundries.",
    },
    {
        "name": "Furnace Walk",
        "subtitle": "Embers sleep beneath the iron plates, waiting for careless feet.",
        "objective": "Defeat the scavengers and cross the furnace walk.",
    },
    {
        "name": "Broken Bellows Chamber",
        "subtitle": "The last furnace listens for a hand that will never return.",
        "objective": "Clear the chamber and return to the Hollow Hearth.",
    },
    {
        "name": "Ash-Covered Sluice",
        "subtitle": "A cracked altar watches the runoff from the buried furnaces.",
        "objective": "Clear the sluice, search the reliquary, and return to the Hollow Hearth.",
    },
]

DEEPER_WELL_ROOMS = [
    [
        "##################",
        "#@...............#",
        "#....†...........#",
        "#................#",
        "#.......~........#",
        "#..........Z.....#",
        "#................#",
        "#....!...........#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#......~.........#",
        "#....Z...........#",
        "#................#",
        "#..........S.....#",
        "#................#",
        "#.......!........#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#................#",
        "#....G.......Z...#",
        "#................#",
        "#.......~........#",
        "#..........†.....#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#....S...........#",
        "#................#",
        "#.......~....!...#",
        "#................#",
        "#..........G.....#",
        "#................#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
    [
        "##################",
        "#@...............#",
        "#....Z.......S...#",
        "#................#",
        "#.......~........#",
        "#................#",
        "#..........G.....#",
        "#....†......!....#",
        "#................#",
        "#..............>.#",
        "#................#",
        "##################",
    ],
]

DEEPER_WELL_META = [
    {
        "name": "The Chained Mouth",
        "subtitle": "Cold water gathers below the final furnace, carrying ash into the dark.",
        "objective": "Find the old descent and clear the drowned approach.",
    },
    {
        "name": "Drowned Steps",
        "subtitle": "Each step is worn smooth by pilgrims who were never meant to return.",
        "objective": "Defeat the dead and cross the flooded stair.",
    },
    {
        "name": "Blue Echo Chamber",
        "subtitle": "The walls repeat sounds that no living throat has made.",
        "objective": "Clear the chamber and use the shrine if the Well has taken too much.",
    },
    {
        "name": "Wellkeeper's Gallery",
        "subtitle": "Rusting hooks hang above the water like a patient set of teeth.",
        "objective": "Survive the gallery and search what the Well has kept.",
    },
    {
        "name": "The Lower Cistern",
        "subtitle": "Something beneath the water remembers the names of the drowned.",
        "objective": "Clear the cistern and return to the Hollow Hearth.",
    },
]

AREA_CONTENT = {
    "tavern": {"rooms": TAVERN_ROOMS, "meta": TAVERN_META, "safe_hub": True},
    "tutorial_estate": {"rooms": TUTORIAL_ROOMS, "meta": TUTORIAL_META, "safe_hub": False},
    "foundries_and_forges": {"rooms": FOUNDRIES_ROOMS, "meta": FOUNDRIES_META, "safe_hub": False},
    "deeper_well": {"rooms": DEEPER_WELL_ROOMS, "meta": DEEPER_WELL_META, "safe_hub": False},
    "blood_wing": {"rooms": ROOMS, "meta": ROOM_META, "safe_hub": False},
}
