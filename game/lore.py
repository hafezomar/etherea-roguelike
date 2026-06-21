"""World lore and tavern menu data for the Pocket Roguelike."""

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
            ("Etherea", "Etherea is a ruined dark fantasy kingdom built on saints, courts, foundries, forests, sealed temples, old bloodlines, and buried mistakes. It was once powerful, sacred, and structured around royal authority and the Imperial Etherean faith. Now its roads are broken, its holy places are rotting, and its strongest memories survive as monsters, ruins, and sealed doors. Etherea is not just a place the player explores. It is an inheritance the player is forced to confront."),
            ("Inscription", "The kingdom did not die at once. It sank, room by room, prayer by prayer."),
        ),
    },
    {
        "title": "THE PLAYER AND THE INHERITANCE",
        "entries": (
            ("The Heir", "The player is not simply an adventurer. A sealed estate still recognizes their blood, and old systems in the kingdom answer to that bloodline. What first looks like land or property becomes something heavier: debt, memory, responsibility, and the consequences of what Etherea's saints and rulers left behind. The player matters not because they are a chosen hero, but because the kingdom remembers their blood."),
            ("Inscription", "Your name was not invited back. It was recorded."),
        ),
    },
    {
        "title": "THE HOLLOW QUILL",
        "entries": (
            ("The Record-Keeper", "The Hollow Quill begins the larger story by sending the inheritance letter. It may be an order, a supernatural record-keeper, an ancient messenger, or something older that preserves names and debts after kingdoms forget them. It is not clearly good or evil. It knows too much, writes too calmly, and appears when old inheritances awaken."),
            ("The Letter", "Read the Hollow Quill Notice in the Tavern to find the full letter left for the heir."),
        ),
    },
    {
        "title": "THE HOLLOW HEARTH TAVERN",
        "entries": (
            ("A Refuge", "The Hollow Hearth Tavern is the safe hub for this pocket roguelike. It is not the full canonical beginning of the Minecraft RPG story; it is a practical refuge where the player can rest, read lore, speak with the Tavern Keeper, Omar Hafez, Verdan Thorne, and Azael Vire, then choose expeditions from the board."),
            ("Inscription", "The fire burns low inside the Hollow Hearth. Outside, the roads still remember how to kill."),
        ),
    },
    {
        "title": "THE CANON JOURNEY",
        "entries": (
            ("The Intended Route", "Tutorial / Estate Intro -> Foundries and Forges -> The Deeper Well -> Saint Admus' Castle -> Etherean Cathedral -> Saint Magnus / Alchemical Laboratory -> Sacred Forest / Barbarian Forest -> Hall of Court -> Throne Room -> Gate of Hell -> Castle of Vaalmurth -> Ashen Forest -> Temple of the Sleepers -> Blood Wing -> Purgatory -> Crystalline Dimension."),
            ("Prototype Placement", "The pocket roguelike adapts this progression slowly. The Blood Wing is late-game content in the full Etherea world, but it is playable early here because it was the first successful prototype area."),
        ),
    },
    {
        "title": "THE FOUNDRIES AND FORGES",
        "entries": (
            ("The First Descent", "The Foundries and Forges are an early expedition through abandoned industrial ruin: red forge glow, rusted chains, broken anvils, dead smiths, and machinery buried under the kingdom. The Foundries once armed courts, kingdoms, and perhaps saintly orders. Now they breathe without smiths. Zombies, Skeletons, and Goblins are the first enemies used here."),
            ("Inscription", "The forges no longer burn for kings. They breathe for something buried beneath them.\n\nThe last furnace coughs once, then falls silent. Somewhere below, water answers."),
        ),
    },
    {
        "title": "THE DEEPER WELL",
        "entries": (
            ("Blue Darkness", "The Deeper Well is a hidden descent beneath the Foundries. It is not an ordinary well, but a buried place of damp stone, old chains, drowned pilgrims, blue darkness, and things the kingdom tried to lower out of memory. It should become an early-to-mid expedition after the Foundries."),
            ("Inscription", "The Deeper Well was not dug for water. It was dug to bury what the saints could not name."),
        ),
    },
    {
        "title": "SAINT ADMUS",
        "entries": (
            ("Authority and Legacy", "Saint Admus is one of the Three sacred figures remembered by the Imperial Etherean faith. He is tied to sacred authority, castle legacy, old nobility, and the holy-political structure of Etherea. Saint Admus' Castle is a future major area. His name survives as a noble legacy, though the truth beneath his worship remains uncertain."),
        ),
    },
    {
        "title": "SAINT MAGNUS",
        "entries": (
            ("The Open Gate", "Saint Magnus is tied to forbidden experimentation, artificial dimensions, alchemical work, cosmic breaches, and the collapse of sacred truth. He may not have wished to destroy Etherea. He may have believed he was saving it, perfecting it, or preparing it to survive something worse. His future laboratory may connect to the Horrors, artificial worlds, and the Crystalline Dimension."),
            ("Inscription", "He did not open the gate to destroy Etherea. He opened it because he believed Etherea could survive what waited beyond."),
        ),
    },
    {
        "title": "TOL",
        "entries": (
            ("The Third", "Tol is the third figure remembered among the Three. Tol is less clearly understood than Admus and Magnus. The surviving associations are judgment, law, silence, sacrifice, final witness, and truth. The ambiguity is deliberate: in Etherea, not every saintly name has a clean explanation."),
            ("Inscription", "Of Tol, the records speak least. That silence may be the truest record left."),
        ),
    },
    {
        "title": "THE HORRORS",
        "entries": (
            ("A Wounded World", "The Horrors are unnatural forces tied to corrupted sacred places, forbidden experiments, and Etherea's deeper collapse. They are not simply monsters. They are signs that reality itself has been wounded, perhaps through Saint Magnus, the Cathedral, artificial dimensions, and the kingdom's attempt to control forces it did not understand."),
            ("Inscription", "A horror is not born when a monster appears. It is born when the world accepts the monster as part of itself."),
        ),
    },
    {
        "title": "TEMPLE OF THE SLEEPERS",
        "entries": (
            ("The Old Temple", "The Temple of the Sleepers is one of the oldest sacred places in the world, perhaps the oldest temple in the universe. It is not merely a building; it behaves like an ancient ritual machine. Its wings hold trials, seals, corrupted pilgrims, watchers, guardians, trap rooms, ritual halls, and boss chambers. The Sleepers may not be awake, but the Temple acts as if they are listening."),
            ("Inscription", "The Temple does not sleep. It waits."),
        ),
    },
    {
        "title": "THE BLOOD WING",
        "entries": (
            ("The First Seal", "The Blood Wing is a late-game wing of the Temple of the Sleepers. It is tied to blood seals, corrupted worshippers, False Pilgrims, Bloodbound Pilgrims, Sealbound Knights, Overseers, traps, ritual combat chambers, Vaelrith, and the First Seal. It is the first playable prototype area in this Tkinter project, though it belongs near the end of the full Etherea progression."),
            ("Inscription", "The blood has answered. The First Seal remembers."),
        ),
    },
    {
        "title": "VAELRITH",
        "entries": (
            ("Herald of the First Seal", "Vaelrith, Herald of the First Seal, is the final boss of the current Blood Wing prototype. He guards the First Seal inside the Temple and is not the final boss of Etherea. He is a late-game Temple guardian: the first major seal trial the Blood Wing has been preparing the player to face."),
        ),
    },
    {
        "title": "PURGATORY",
        "entries": (
            ("A Later Descent", "Purgatory is a major later area in Etherea. Its map exists in the larger Minecraft project, but its systems, enemies, NPCs, dialogue, quests, and boss logic still need work. It is tied to nightmare, punishment, death, ancient cosmic decay, and The Old One. The Old One's aura and particle systems caused major FPS issues after a Bedrock update, so future effects need to be throttled rather than spammed every tick."),
            ("Inscription", "Purgatory does not punish the dead. It teaches the living what death remembers."),
        ),
    },
    {
        "title": "THE CRYSTALLINE DIMENSION",
        "entries": (
            ("Beautiful, But Wrong", "The Crystalline Dimension is a late-game or final-arc area in the larger Minecraft project. Its map exists, but its systems remain unfinished. It is likely tied to Saint Magnus, artificial dimensions, crystal structures, cosmic experimentation, and the final truth of Etherea. It may be a created or discovered realm that reveals what Magnus truly attempted."),
            ("Inscription", "The crystals shine like salvation. That is what makes them dangerous."),
        ),
    },
    {
        "title": "CURRENT PROTOTYPE NOTE",
        "entries": (
            ("Pocket Roguelike", "This Tkinter game is not the full Etherea RPG. It is a small offline systems prototype inspired by the larger Minecraft Bedrock dark fantasy RPG. It tests tile movement, turn-based combat, dungeon rooms, enemies, bosses, relics, shrines, traps, save/load, lore presentation, the Tavern hub, expedition selection, and Python OOP with Tkinter."),
            ("Scope", "The Blood Wing appears earlier here than it should canonically because it was the first successful prototype area. The project is a compact adaptation of the world, not the whole canon."),
        ),
    },
)
