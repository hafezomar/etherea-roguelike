"""
Etherea: Blood Wing data models.

Pure data classes, enumerations, and factory functions.  The generated project
arrived with this file stripped of much of its Python punctuation; this version
restores the intended model layer while keeping the engine-facing API intact.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class PlayerClass(Enum):
    WARDEN = "Warden"
    ASHEN_BLADE = "Ashen Blade"
    DREAMSEER = "Dreamseer"


class Difficulty(Enum):
    PILGRIM = "Pilgrim"
    WARDEN = "Warden"
    MARTYR = "Martyr"


class StatusType(Enum):
    BLEED = "Bleed"
    STUN = "Stun"
    EMPOWERED = "Empowered"


class GameState(Enum):
    AREA_SELECT = "area_select"
    WORLD_PROGRESSION = "world_progression"
    CLASS_SELECT = "class_select"
    DIFFICULTY_SELECT = "difficulty_select"
    PLAYING = "playing"
    SHRINE_PROMPT = "shrine_prompt"
    SHOP_PROMPT = "shop_prompt"
    VICTORY = "victory"
    DEFEAT = "defeat"


@dataclass
class StatusEffect:
    """A timed status effect on a player or enemy."""

    type: StatusType
    duration: int
    damage: int = 0

    def tick(self) -> bool:
        """Reduce duration by one turn. Return True when expired."""
        self.duration -= 1
        return self.duration <= 0

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "duration": self.duration,
            "damage": self.damage,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StatusEffect":
        return cls(
            type=StatusType(data["type"]),
            duration=int(data.get("duration", 0)),
            damage=int(data.get("damage", 0)),
        )


@dataclass(frozen=True)
class Relic:
    """A passive relic granting a permanent bonus."""

    id: str
    name: str
    description: str
    icon: str = "◆"

    def to_dict(self) -> dict:
        return {"id": self.id}


@dataclass
class Player:
    """The player character."""

    name: str
    player_class: PlayerClass
    hp: int
    max_hp: int
    attack: int
    defense: int
    focus: int
    max_focus: int
    x: int = 0
    y: int = 0
    blood_vials: int = 2
    relic_shards: int = 0
    status_effects: List[StatusEffect] = field(default_factory=list)
    relics: List[str] = field(default_factory=list)
    first_hit_this_room: bool = True
    first_attack_this_room: bool = True

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def has_status(self, status_type: StatusType) -> bool:
        return any(effect.type == status_type for effect in self.status_effects)

    def add_status(self, effect: StatusEffect) -> None:
        self.status_effects = [s for s in self.status_effects if s.type != effect.type]
        self.status_effects.append(effect)

    def remove_status(self, status_type: StatusType) -> None:
        self.status_effects = [s for s in self.status_effects if s.type != status_type]

    def has_relic(self, relic_id: str) -> bool:
        return relic_id in self.relics

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "player_class": self.player_class.value,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "focus": self.focus,
            "max_focus": self.max_focus,
            "x": self.x,
            "y": self.y,
            "blood_vials": self.blood_vials,
            "relic_shards": self.relic_shards,
            "status_effects": [s.to_dict() for s in self.status_effects],
            "relics": list(self.relics),
            "first_hit_this_room": self.first_hit_this_room,
            "first_attack_this_room": self.first_attack_this_room,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        player = cls(
            name=data["name"],
            player_class=PlayerClass(data["player_class"]),
            hp=int(data["hp"]),
            max_hp=int(data["max_hp"]),
            attack=int(data["attack"]),
            defense=int(data["defense"]),
            focus=int(data["focus"]),
            max_focus=int(data["max_focus"]),
            x=int(data.get("x", 0)),
            y=int(data.get("y", 0)),
            blood_vials=int(data.get("blood_vials", 2)),
            relic_shards=int(data.get("relic_shards", 0)),
        )
        player.status_effects = [StatusEffect.from_dict(s) for s in data.get("status_effects", [])]
        player.relics = list(data.get("relics", []))
        player.first_hit_this_room = bool(data.get("first_hit_this_room", True))
        player.first_attack_this_room = bool(data.get("first_attack_this_room", True))
        return player


@dataclass
class Enemy:
    """An enemy entity."""

    name: str
    enemy_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    shard_reward: int
    x: int = 0
    y: int = 0
    status_effects: List[StatusEffect] = field(default_factory=list)
    is_boss: bool = False
    boss_phase: int = 1
    has_summoned: bool = False

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def has_status(self, status_type: StatusType) -> bool:
        return any(effect.type == status_type for effect in self.status_effects)

    def add_status(self, effect: StatusEffect) -> None:
        self.status_effects = [s for s in self.status_effects if s.type != effect.type]
        self.status_effects.append(effect)

    def remove_status(self, status_type: StatusType) -> None:
        self.status_effects = [s for s in self.status_effects if s.type != status_type]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "enemy_type": self.enemy_type,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "shard_reward": self.shard_reward,
            "x": self.x,
            "y": self.y,
            "status_effects": [s.to_dict() for s in self.status_effects],
            "is_boss": self.is_boss,
            "boss_phase": self.boss_phase,
            "has_summoned": self.has_summoned,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Enemy":
        enemy = cls(
            name=data["name"],
            enemy_type=data["enemy_type"],
            hp=int(data["hp"]),
            max_hp=int(data["max_hp"]),
            attack=int(data["attack"]),
            defense=int(data["defense"]),
            shard_reward=int(data["shard_reward"]),
            x=int(data.get("x", 0)),
            y=int(data.get("y", 0)),
            is_boss=bool(data.get("is_boss", False)),
            boss_phase=int(data.get("boss_phase", 1)),
            has_summoned=bool(data.get("has_summoned", False)),
        )
        enemy.status_effects = [StatusEffect.from_dict(s) for s in data.get("status_effects", [])]
        return enemy


@dataclass
class RunStats:
    """Tracks stats for the run score summary."""

    turns: int = 0
    enemies_defeated: int = 0
    shards_collected: int = 0
    potions_used: int = 0
    relics_found: int = 0
    shrines_visited: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0

    def to_dict(self) -> dict:
        return {
            "turns": self.turns,
            "enemies_defeated": self.enemies_defeated,
            "shards_collected": self.shards_collected,
            "potions_used": self.potions_used,
            "relics_found": self.relics_found,
            "shrines_visited": self.shrines_visited,
            "damage_dealt": self.damage_dealt,
            "damage_taken": self.damage_taken,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RunStats":
        return cls(
            turns=int(data.get("turns", 0)),
            enemies_defeated=int(data.get("enemies_defeated", 0)),
            shards_collected=int(data.get("shards_collected", 0)),
            potions_used=int(data.get("potions_used", 0)),
            relics_found=int(data.get("relics_found", 0)),
            shrines_visited=int(data.get("shrines_visited", 0)),
            damage_dealt=int(data.get("damage_dealt", 0)),
            damage_taken=int(data.get("damage_taken", 0)),
        )


@dataclass(frozen=True)
class RoomModifier:
    """An atmospheric modifier applied to a room."""

    id: str
    name: str
    description: str
    trap_damage_bonus: int = 0
    shard_bonus: int = 0
    enemy_move_interval: int = 1
    shrine_hp_bonus: int = 0


ALL_RELICS = [
    Relic("thorn_charm", "Thorn-Crowned Charm", "Reflect 1 damage when hit", "♠"),
    Relic("saints_ember", "Saint's Ember", "First attack each room deals +3 damage", "☼"),
    Relic("pale_wing", "Pale Wing Fragment", "+2 defense for 1 turn after Blood Vial", "◊"),
    Relic("bloodglass_ring", "Bloodglass Ring", "Blood Vials also restore 2 focus", "○"),
    Relic("rusted_halo", "Rusted Halo", "+15% crit chance below 40% HP", "☽"),
    Relic("chain_psalm", "Chain Psalm", "Stunned enemies take +2 damage", "⛓"),
    Relic("hollow_medallion", "Hollow Saint Medallion", "Shrines restore +4 extra HP", "✝"),
    Relic("ember_gauntlet", "Ember-Veined Gauntlet", "Class ability costs 1 less focus", "☄"),
]


ROOM_MODIFIERS = [
    RoomModifier(
        "blood_listens",
        "The Blood Listens",
        "Traps deal +1 damage, reliquaries and enemies give +5 shards",
        trap_damage_bonus=1,
        shard_bonus=5,
    ),
    RoomModifier(
        "ashen_silence",
        "Ashen Silence",
        "Enemies move every other turn",
        enemy_move_interval=2,
    ),
    RoomModifier(
        "saintless_dark",
        "Saintless Dark",
        "Shrines restore 4 less HP, enemies drop +3 shards",
        shrine_hp_bonus=-4,
        shard_bonus=3,
    ),
]


CLASS_STATS = {
    PlayerClass.WARDEN: {
        "name": "Warden",
        "hp": 58,
        "attack": 10,
        "defense": 4,
        "focus": 7,
        "ability": "Shield Bash",
        "ability_desc": "3 focus · adjacent · bonus damage + stun",
        "ability_cost": 3,
        "passive": "Iron Resolve",
        "passive_desc": "First hit each room is reduced by 50%",
        "lore": "The Wardens carry the weight of oaths no saint would honor.",
    },
    PlayerClass.ASHEN_BLADE: {
        "name": "Ashen Blade",
        "hp": 46,
        "attack": 14,
        "defense": 2,
        "focus": 8,
        "ability": "Cinder Arc",
        "ability_desc": "4 focus · all adjacent · applies bleed",
        "ability_cost": 4,
        "passive": "Searing Wounds",
        "passive_desc": "Bleeding enemies take +1 damage from your attacks",
        "lore": "Their blades remember the fire that forged them.",
    },
    PlayerClass.DREAMSEER: {
        "name": "Dreamseer",
        "hp": 39,
        "attack": 9,
        "defense": 2,
        "focus": 13,
        "ability": "Dream Lance",
        "ability_desc": "4 focus · range 4 · bonus damage + stun",
        "ability_cost": 4,
        "passive": "Psychic Resonance",
        "passive_desc": "Regain 1 focus when you stun an enemy",
        "lore": "They see what the saints refused to dream.",
    },
}


DIFFICULTY_STATS = {
    Difficulty.PILGRIM: {
        "name": "Pilgrim",
        "desc": "For those who seek the story. Enemies are weakened.",
        "hp_mult": 0.8,
        "atk_bonus": -2,
        "vials": 3,
        "shard_mult": 1.25,
    },
    Difficulty.WARDEN: {
        "name": "Warden",
        "desc": "The intended trial. No mercy, no charity.",
        "hp_mult": 1.0,
        "atk_bonus": 0,
        "vials": 2,
        "shard_mult": 1.0,
    },
    Difficulty.MARTYR: {
        "name": "Martyr",
        "desc": "For those who believe suffering is prayer.",
        "hp_mult": 1.25,
        "atk_bonus": 2,
        "vials": 1,
        "shard_mult": 0.75,
    },
}


ENEMY_DEFS = {
    "false_pilgrim": {
        "name": "False Pilgrim",
        "hp": 25,
        "attack": 7,
        "defense": 1,
        "shard_reward": 8,
        "is_boss": False,
    },
    "overseer": {
        "name": "Overseer",
        "hp": 22,
        "attack": 8,
        "defense": 0,
        "shard_reward": 10,
        "is_boss": False,
    },
    "sealbound_knight": {
        "name": "Sealbound Knight",
        "hp": 42,
        "attack": 10,
        "defense": 4,
        "shard_reward": 17,
        "is_boss": False,
    },
    "bloodbound_pilgrim": {
        "name": "Bloodbound Pilgrim",
        "hp": 34,
        "attack": 11,
        "defense": 2,
        "shard_reward": 15,
        "is_boss": False,
    },
    "vaelrith": {
        "name": "Vaelrith",
        "hp": 85,
        "attack": 16,
        "defense": 5,
        "shard_reward": 120,
        "is_boss": True,
    },
}


def create_player(player_class: PlayerClass, difficulty: Difficulty = Difficulty.WARDEN) -> Player:
    """Create a new player with class stats and difficulty-adjusted vials."""
    stats = CLASS_STATS[player_class]
    diff = DIFFICULTY_STATS[difficulty]
    return Player(
        name=stats["name"],
        player_class=player_class,
        hp=stats["hp"],
        max_hp=stats["hp"],
        attack=stats["attack"],
        defense=stats["defense"],
        focus=stats["focus"],
        max_focus=stats["focus"],
        blood_vials=diff["vials"],
    )


def create_enemy(enemy_type: str, difficulty: Difficulty = Difficulty.WARDEN, x: int = 0, y: int = 0) -> Enemy:
    """Create an enemy scaled by difficulty."""
    definition = ENEMY_DEFS[enemy_type]
    diff = DIFFICULTY_STATS[difficulty]
    hp = max(1, int(definition["hp"] * diff["hp_mult"]))
    attack = max(1, int(definition["attack"] + diff["atk_bonus"]))
    shard_reward = max(1, int(definition["shard_reward"] * diff["shard_mult"]))
    return Enemy(
        name=definition["name"],
        enemy_type=enemy_type,
        hp=hp,
        max_hp=hp,
        attack=attack,
        defense=definition["defense"],
        shard_reward=shard_reward,
        x=x,
        y=y,
        is_boss=definition["is_boss"],
    )
