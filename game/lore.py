"""Readable world lore and tavern menu data for the Pocket Roguelike."""

TAVERN_NAME = "The Hollow Hearth Tavern"
TAVERN_DESCRIPTION = (
    "The fire burns low inside the Hollow Hearth. Maps, sealed letters, and old "
    "relics rest across the table. From here, the road into Etherea begins again."
)

TAVERN_MENU = (
    "Continue Saved Run",
    "Choose Expedition",
    "Tutorial / How to Play",
    "Lore Book",
    "World Progression",
    "Settings",
    "Quit",
)

LORE_PAGES = (
    {
        "title": "ETHEREA",
        "entries": (
            (
                "Etherea",
                "Etherea is a ruined dark fantasy kingdom built on inheritance, old saints, forgotten bloodlines, and sacred places that have rotted into danger. The player is an heir called back to a world that remembers their blood.",
            ),
            (
                "The Hollow Quill",
                "The Hollow Quill sends a letter calling the player back to a forgotten inheritance. In Etherea, inheritance is rarely a gift. It is usually a burden, a debt, or a wound left by the past.",
            ),
            ("Inscription", "Your inheritance was not land. It was the wound beneath it."),
            (
                "The Tavern",
                "The Hollow Hearth Tavern is a safe resting point between expeditions. It is a hub for this pocket roguelike prototype, where old routes and cursed places can still be studied.",
            ),
        ),
    },
    {
        "title": "SAINTS AND RUIN",
        "entries": (
            (
                "The Saints",
                "The old Etherean faith remembers Saint Admus, Saint Magnus, and Tol. They are honored as saints, but the truth behind them is broken and uncertain. In Etherea, holiness and corruption often share the same walls.",
            ),
            (
                "Saint Magnus",
                "Saint Magnus is tied to forbidden experiments, artificial dimensions, and the deeper collapse of Etherea. He may have believed he was saving the kingdom, but some gates do not close cleanly.",
            ),
            (
                "The Horrors",
                "The Horrors are unnatural forces tied to corrupted sacred places, forbidden experiments, and the old kingdom's collapse. They are signs that reality itself has been wounded.",
            ),
        ),
    },
    {
        "title": "TEMPLE OF THE SLEEPERS",
        "entries": (
            (
                "The Temple",
                "The Temple of the Sleepers is one of the oldest sacred places in the world. It is ritualistic and alive in ways stone should not be. Its wings hold trials, seals, corrupted pilgrims, watchers, and guardians.",
            ),
            (
                "The Blood Wing",
                "The current playable prototype is set in the Temple of the Sleepers: Blood Wing. In the full progression, it is a late-game area tied to blood seals, trap chambers, temple guardians, and Vaelrith.",
            ),
            ("Inscription", "The blood has answered. The First Seal remembers."),
            (
                "Vaelrith",
                "Vaelrith is the Herald of the First Seal and the final boss of the current Blood Wing prototype. He represents the Temple's first major late-game trial.",
            ),
        ),
    },
    {
        "title": "THE BIGGER JOURNEY",
        "entries": (
            (
                "The Route",
                "The full Etherea journey begins much earlier than the Blood Wing. It starts with the player's return through inheritance, then moves through the Foundries, the Deeper Well, Saint Admus' Castle, the Cathedral, the Alchemical Laboratory, and further sacred ruins.",
            ),
            (
                "The Prototype",
                "This pocket roguelike does not present the full campaign yet. Blood Wing is available here as a compact late-game prototype while the larger route remains planned.",
            ),
        ),
    },
)
