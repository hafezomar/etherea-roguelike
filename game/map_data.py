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
