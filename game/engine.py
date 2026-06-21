"""
Etherea: Blood Wing — Game Engine
Core engine handling all game logic, rendering, input, and UI.
Built entirely on Tkinter — no third-party dependencies.
"""
import tkinter as tk
import json
import os
import random
import math
import copy
import textwrap
from typing import List, Optional, Tuple
from game.models import (
    PlayerClass, Difficulty, StatusType, GameState,
    StatusEffect, Relic, Player, Enemy, RunStats, RoomModifier,
    ALL_RELICS, ROOM_MODIFIERS, CLASS_STATS, DIFFICULTY_STATS,
    ENEMY_DEFS, create_player, create_enemy,
)
from game.map_data import AREA_CONTENT, ROOMS, ROOM_META, ENEMY_MARKERS
from game.areas import AREA_REGISTRY, CAMPAIGN_VERSION, campaign_areas
from game.audio import AudioManager
from game.hub import HOLLOW_QUILL_LETTER, INHERITANCE_NOTICE, TAVERN_NPCS
from game.lore import LORE_PAGES, TAVERN_DESCRIPTION, TAVERN_MENU, TAVERN_NAME
# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
TILE = 40
GRID_W, GRID_H = 18, 12
CANVAS_W = TILE * GRID_W   # 720
CANVAS_H = TILE * GRID_H   # 480
SIDEBAR_W = 340
WIN_W = CANVAS_W + SIDEBAR_W + 2
WIN_H = 620
# ── Colour palette ───────────────────────────────────────────
C = {
    "bg":           "#0d0d14",
    "panel":        "#12101c",
    "panel_edge":   "#2a2838",
    "wall":         "#252030",
    "wall_hi":      "#302840",
    "floor":        "#16121e",
    "floor_alt":    "#181424",
    "trap":         "#1e0f18",
    "trap_glow":    "#3a1525",
    "reliq":        "#1e1c14",
    "reliq_icon":   "#c9a84c",
    "shrine":       "#141628",
    "shrine_icon":  "#6a8aaa",
    "exit_locked":  "#1a1810",
    "exit_open":    "#2a2518",
    "exit_glow":    "#c9a84c",
    "text":         "#c9c0d4",
    "text_dim":     "#6a6a7a",
    "text_bright":  "#e8e0f0",
    "gold":         "#c9a84c",
    "red":          "#a83232",
    "green":        "#4a9a6a",
    "blue":         "#4a6a9a",
    "purple":       "#7a4a8a",
    "player":       "#4a9a7a",
    "player_out":   "#68c8a0",
    "hp_bar":       "#a83232",
    "hp_bg":        "#2a1818",
    "focus_bar":    "#4a6a9a",
    "focus_bg":     "#18182a",
    "boss_bar":     "#c43a5a",
    "boss_bg":      "#2a1828",
    "crit":         "#f0c040",
    "heal":         "#40c070",
    "bleed":        "#c04040",
}
ENEMY_CLR = {
    "zombie":             "#55704a",
    "skeleton":           "#b6aa91",
    "goblin":             "#6a9a48",
    "false_pilgrim":      "#8a4040",
    "overseer":           "#6a4a7a",
    "sealbound_knight":   "#5a6a8a",
    "bloodbound_pilgrim": "#9a2a2a",
    "vaelrith":           "#c43a5a",
}
ASSET_FILES = {
    "warden": "warden.png",
    "ashen_blade": "ashen-blade.png",
    "dreamseer": "dreamseer.png",
    "zombie": "enemy_zombie.png",
    "skeleton": "enemy_skeleton.png",
    "goblin": "enemy_goblin.png",
    "false_pilgrim": "false-pilgrim.png",
    "overseer": "overseer.png",
    "sealbound_knight": "sealbound-knight.png",
    "bloodbound_pilgrim": "bloodbound-pilgrim.png",
    "vaelrith": "vaelrith.png",
    "tavern_keeper": "npc_tavern_keeper.png",
    "omar_hafez": "npc_omar_hafez_creator.png",
    "verdan_thorne": "npc_verdan_thorne.png",
    "azael_vire": "npc_azael_vire.png",
    "tavern_floor": "tile_tavern_floor.png",
    "expedition_board": "tile_expedition_board.png",
    "lore_bookshelf": "tile_lore_bookshelf.png",
    "hollow_quill_notice": "tile_hollow_quill_notice.png",
    "tavern_bed": "tile_bed_rest.png",
    "tavern_hearth": "tile_tavern_hearth.png",
    "exit_rune": "tile_exit_rune.png",
    "forge_furnace": "tile_forge_furnace.png",
    "deeper_well_marker": "tile_deeper_well_marker.png",
}
TAVERN_TILE_SPRITES = {
    "e": "expedition_board",
    "l": "lore_bookshelf",
    "i": "hollow_quill_notice",
    "b": "tavern_bed",
    "h": "tavern_hearth",
}
TAVERN_NPC_SPRITES = {
    "Tavern Keeper": "tavern_keeper",
    "Omar Hafez": "omar_hafez",
    "Verdan Thorne": "verdan_thorne",
    "Azael Vire": "azael_vire",
}
CLASS_ACCENT = {
    PlayerClass.WARDEN:      "#4a7a5a",
    PlayerClass.ASHEN_BLADE:  "#9a6a3a",
    PlayerClass.DREAMSEER:    "#5a5a9a",
}
TILE_CHARS = set("#.~!†>@") | set(ENEMY_MARKERS.keys())
WALKABLE = set(".~!†>@") | set(ENEMY_MARKERS.keys())
# ═══════════════════════════════════════════════════════════════
# GAME ENGINE
# ═══════════════════════════════════════════════════════════════
class GameEngine:
    """Main engine for Etherea: Blood Wing."""
    # ─── Initialisation ──────────────────────────────────────
    def __init__(self, root=None, headless=False):
        self.headless = headless
        # Game state
        self.state = GameState.TAVERN
        self.area_id = "blood_wing"
        self.area_status = AREA_REGISTRY[self.area_id]["status"]
        self.cleared_areas: set[str] = set()
        self.tavern_index = 0
        self.expedition_index = 0
        self.lore_page = 0
        self.inheritance_page = 0
        self.menu_hitboxes: list[tuple[int, int, int, int, str]] = []
        self.difficulty = Difficulty.WARDEN
        self.selected_class_index = 0
        self.selected_diff_index = 1
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.grid: List[List[str]] = []
        self.room_index = 0
        self.room_modifier: Optional[RoomModifier] = None
        self.event_log: List[str] = []
        self.run_stats = RunStats()
        self.relic_pool = list(ALL_RELICS)
        random.shuffle(self.relic_pool)
        self.turn_count = 0
        self.is_fullscreen = False
        self.exit_pulse_on = False
        self._pulse_job = None
        self._anim_jobs: list = []
        self.images: dict = {}
        self._pending_float_texts: list = []
        self._pending_tile_flashes: list = []
        # Save path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.save_path = os.path.join(self.base_dir, "saves", "blood_wing_save.json")
        self.audio = AudioManager(self.base_dir)
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        if not headless:
            self._setup_ui(root)
    # ─── UI Setup ────────────────────────────────────────────
    def _setup_ui(self, root):
        if root is None:
            self.root = tk.Tk()
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False
        self.root.title("Etherea: Ashes of the Saints - Pocket Roguelike")
        self.root.configure(bg=C["bg"])
        self.root.resizable(True, True)
        # Centre on screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, (sw - WIN_W) // 2)
        y = max(0, (sh - WIN_H) // 2)
        self.root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")
        self.root.minsize(WIN_W, WIN_H)
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=C["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Game canvas
        self.canvas = tk.Canvas(
            self.main_frame, width=CANVAS_W, height=CANVAS_H,
            bg=C["bg"], highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, anchor=tk.N, padx=(1, 0), pady=1)
        # Sidebar
        self.sidebar = tk.Canvas(
            self.main_frame, width=SIDEBAR_W, bg=C["panel"],
            highlightthickness=0,
        )
        self.sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 1), pady=1)
        # Load images
        self._load_images()
        # Key bindings
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<F11>", lambda e: self._toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self._leave_fullscreen())
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        # Initial render
        self._render()
    def _load_images(self):
        """Load character and enemy sprites from assets/.

        Tkinter's PhotoImage keeps images lightweight and dependency-free.  The
        source art is 128x128, so we keep three sizes:
        - *_p: 64px portraits for menus/sidebar
        - *_t: 32px tile sprites for normal entities
        - *_b: 64px boss sprites for Vaelrith
        Every image is stored on self.images to prevent garbage collection.
        """
        asset_dir = os.path.join(self.base_dir, "assets")
        for key, fname in ASSET_FILES.items():
            path = os.path.join(asset_dir, fname)
            if not os.path.exists(path):
                continue
            try:
                img = tk.PhotoImage(file=path)
                self.images[key + "_orig"] = img
                # The bundled art is currently 128x128.  Compute conservative
                # integer downscales so future replacement art still behaves.
                portrait_scale = max(1, max(img.width(), img.height()) // 64)
                tile_scale = max(1, max(img.width(), img.height()) // 32)
                boss_scale = max(1, max(img.width(), img.height()) // 64)
                self.images[key + "_p"] = img.subsample(portrait_scale, portrait_scale)
                self.images[key + "_t"] = img.subsample(tile_scale, tile_scale)
                self.images[key + "_b"] = img.subsample(boss_scale, boss_scale)
            except Exception as exc:
                # Bad/missing art should never stop the game from launching.
                print(f"[assets] could not load {fname}: {exc}")

    def _class_sprite_key(self, player_class: PlayerClass) -> str:
        return {
            PlayerClass.WARDEN: "warden",
            PlayerClass.ASHEN_BLADE: "ashen_blade",
            PlayerClass.DREAMSEER: "dreamseer",
        }.get(player_class, "warden")

    def _entity_sprite_key(self, enemy_type: str) -> str:
        return enemy_type

    def _draw_sprite(self, canvas, key: str, cx: int, cy: int, *, boss: bool = False) -> bool:
        """Draw a sprite image if available. Return True when drawn."""
        suffix = "_b" if boss else "_t"
        img = self.images.get(key + suffix)
        if not img:
            return False
        canvas.create_image(cx, cy, image=img)
        return True

    def run(self):
        if not self.headless:
            self.root.mainloop()
    # ═══════════════════════════════════════════════════════════
    # RENDERING
    # ═══════════════════════════════════════════════════════════
    def _render(self):
        if self.headless:
            return
        if self.state == GameState.TAVERN:
            self._render_tavern()
        elif self.state == GameState.EXPEDITION_BOARD:
            self._render_expedition_board()
        elif self.state == GameState.TUTORIAL:
            self._render_tutorial()
        elif self.state == GameState.LORE_BOOK:
            self._render_lore_book()
        elif self.state == GameState.SETTINGS:
            self._render_settings()
        elif self.state == GameState.INHERITANCE_BOARD:
            self._render_inheritance_board()
        elif self.state == GameState.AREA_SELECT:
            self._render_area_select()
        elif self.state == GameState.WORLD_PROGRESSION:
            self._render_world_progression()
        elif self.state == GameState.CLASS_SELECT:
            self._render_class_select()
        elif self.state == GameState.DIFFICULTY_SELECT:
            self._render_difficulty_select()
        elif self.state in (GameState.PLAYING, GameState.SHRINE_PROMPT, GameState.SHOP_PROMPT):
            self._render_game()
        elif self.state == GameState.VICTORY:
            self._render_victory()
        elif self.state == GameState.DEFEAT:
            self._render_defeat()

    def _menu_button(self, canvas, x: int, y: int, width: int, text: str, action: str, selected: bool = False):
        fill = C["panel_edge"] if selected else C["panel"]
        outline = C["gold"] if selected else C["panel_edge"]
        canvas.create_rectangle(x, y, x + width, y + 34, fill=fill, outline=outline, width=2 if selected else 1)
        canvas.create_text(x + width // 2, y + 17, text=text, fill=C["text_bright"], font=("Consolas", 10, "bold"))
        self.menu_hitboxes.append((x, y, x + width, y + 34, action))

    def _draw_back_button(self, canvas, action: str = "tavern"):
        self._menu_button(canvas, 22, CANVAS_H - 42, 120, "BACK  [Esc]", action)

    def _render_tavern(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        c.create_text(cw // 2, 48, text="ETHEREA: ASHES OF THE SAINTS", fill=C["gold"], font=("Georgia", 23, "bold"))
        c.create_text(cw // 2, 78, text="Pocket Roguelike", fill=C["text_dim"], font=("Georgia", 10, "italic"))
        c.create_text(cw // 2, 111, text=CAMPAIGN_VERSION, fill=C["text_dim"], font=("Consolas", 8))
        c.create_line(130, 128, cw - 130, 128, fill=C["panel_edge"])

        saved = os.path.exists(self.save_path)
        labels = ["New Game", "Continue Saved Run" if saved else "Continue Saved Run (none)", "Tutorial / How to Play", "Lore Book", "World Progression", "Settings", "Quit"]
        actions = ("new_game", "continue", "tutorial", "lore", "world", "settings", "quit")
        x, y, width = cw // 2 - 190, 151, 380
        for index, (label, action) in enumerate(zip(labels, actions)):
            self._menu_button(c, x, y + index * 39, width, label, action, index == self.tavern_index)
        c.create_text(cw // 2, ch - 22, text="Up / Down: select    Enter: confirm    F11: fullscreen",
                      fill=C["text_dim"], font=("Consolas", 8))
        self._render_sidebar_tavern()

    def _render_sidebar_tavern(self):
        s = self.sidebar
        s.delete("all")
        sw = max(SIDEBAR_W, s.winfo_width())
        s.create_text(sw // 2, 42, text="THE HOLLOW HEARTH", fill=C["gold"], font=("Georgia", 17, "bold"))
        s.create_text(sw // 2, 66, text="A safe hearth waits beyond a new run", fill=C["text_dim"], font=("Georgia", 8, "italic"))
        s.create_line(22, 88, sw - 22, 88, fill=C["panel_edge"])
        s.create_text(sw // 2, 126, text="PLAYABLE HUB", fill=C["text_dim"], font=("Consolas", 8, "bold"))
        s.create_text(sw // 2, 157, text="The Hollow Hearth Tavern", fill=C["text_bright"], font=("Georgia", 13, "bold"))
        s.create_text(sw // 2, 178, text="Tutorial and Foundries now available", fill=C["gold"], font=("Consolas", 8))
        s.create_text(sw // 2, 230,
                      text="Start a new run to enter the playable tavern hub and choose an expedition from inside the world.",
                      fill=C["text_dim"], font=("Georgia", 9, "italic"), width=sw - 44)
        s.create_text(sw // 2, 330, text="Maps. Sealed letters. Old relics.", fill=C["text"], font=("Georgia", 10, "italic"))
        s.create_text(sw // 2, 500, text=CAMPAIGN_VERSION, fill=C["text_dim"], font=("Consolas", 8))

    def _render_expedition_board(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        c.create_text(cw // 2, 38, text="EXPEDITION BOARD", fill=C["gold"], font=("Georgia", 22, "bold"))
        c.create_text(cw // 2, 62, text="Prototype access from the Hollow Hearth", fill=C["text_dim"], font=("Georgia", 9, "italic"))

        playable_ids = ("tutorial_estate", "foundries_and_forges", "blood_wing")
        for index, area_id in enumerate(playable_ids):
            area = AREA_REGISTRY[area_id]
            y = 86 + index * 61
            selected = index == self.expedition_index
            color = C["gold"] if area["status"] == "playable_prototype" else C["green"]
            c.create_rectangle(70, y, cw - 70, y + 50, fill=C["panel"], outline=color if selected else C["panel_edge"], width=2 if selected else 1)
            label = "LATE-GAME PROTOTYPE" if area["status"] == "playable_prototype" else "PLAYABLE EXPEDITION"
            c.create_text(92, y + 17, anchor=tk.W, text=label, fill=color, font=("Consolas", 8, "bold"))
            c.create_text(92, y + 35, anchor=tk.W, text=str(area["name"]), fill=C["text_bright"], font=("Georgia", 12, "bold"))
            self.menu_hitboxes.append((70, y, cw - 70, y + 50, f"area:{area_id}"))

        c.create_text(cw // 2, 280, text="PLANNED CAMPAIGN AREAS", fill=C["text_dim"], font=("Consolas", 9, "bold"))
        planned = [(key, data) for key, data in campaign_areas() if data["status"] == "planned"]
        for index, (_, data) in enumerate(planned):
            column = index // 7
            row = index % 7
            x = 42 + column * (cw // 2)
            y = 306 + row * 24
            c.create_text(x, y, anchor=tk.W, text=f"{data['order']:02d}  {data['name']} - Planned",
                          fill=C["text_dim"], font=("Consolas", 8))
        c.create_text(cw // 2, ch - 24, text="Up / Down: choose expedition    Enter: begin    Esc: return to tavern",
                      fill=C["text_dim"], font=("Consolas", 9))
        self._draw_back_button(c)
        self._render_sidebar_tavern()

    def _render_tutorial(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        c.create_rectangle(0, 0, cw, CANVAS_H, fill=C["bg"], outline="")
        c.create_text(cw // 2, 35, text="TUTORIAL / HOW TO PLAY", fill=C["gold"], font=("Georgia", 21, "bold"))
        sections = (
            ("Basic Controls", "WASD or arrow keys move. Walking into an enemy attacks it. Space attacks an adjacent enemy. Q uses your class ability. E drinks a Blood Vial. R recovers focus. B and L save or load."),
            ("Game Loop", "Choose an expedition, class, and difficulty. Explore tile rooms, fight enemies, avoid blood traps, use shrines and reliquaries, then defeat Vaelrith in the Blood Wing prototype."),
            ("Combat", "HP keeps you alive. Attack and defense affect damage. Enemies act after you. Status effects, relics, class abilities, and boss phases can change a fight."),
            ("Tiles", "# walls, . floor, ~ blood trap, ! reliquary, shrine, > exit, and V marks Vaelrith. Step onto shrines, reliquaries, and exits to interact."),
            ("Classes and Difficulty", "Warden is durable, Ashen Blade deals high damage, and Dreamseer uses focus magic. Pilgrim is easier, Warden is the intended trial, and Martyr is the harshest route."),
        )
        y = 72
        for heading, body in sections:
            c.create_text(52, y, anchor=tk.W, text=heading, fill=C["text_bright"], font=("Georgia", 11, "bold"))
            c.create_text(52, y + 16, anchor=tk.W, text=body, fill=C["text_dim"], font=("Consolas", 8), width=cw - 104)
            y += 72
        self._draw_back_button(c)
        self._render_sidebar_tavern()

    def _render_lore_book(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        page = LORE_PAGES[self.lore_page]
        c.create_rectangle(0, 0, cw, CANVAS_H, fill=C["bg"], outline="")
        panel_x, panel_y = 38, 88
        panel_w, panel_h = cw - 76, CANVAS_H - 142
        c.create_text(cw // 2, 33, text="LORE BOOK", fill=C["gold"], font=("Georgia", 21, "bold"))
        c.create_rectangle(panel_x, panel_y, panel_x + panel_w, panel_y + panel_h,
                           fill=C["panel"], outline=C["panel_edge"], width=1)
        c.create_text(cw // 2, panel_y + 26, text=str(page["title"]),
                      fill=C["text_bright"], font=("Georgia", 15, "bold"), width=panel_w - 56)
        c.create_line(panel_x + 28, panel_y + 48, panel_x + panel_w - 28, panel_y + 48, fill=C["panel_edge"])
        y = panel_y + 76
        for heading, body in page["entries"]:
            c.create_text(panel_x + 30, y, anchor=tk.W, text=heading,
                          fill=C["gold"], font=("Georgia", 11, "bold"))
            c.create_text(panel_x + 30, y + 25, anchor=tk.W, text=body,
                          fill=C["text_dim"], font=("Georgia", 9, "italic") if heading == "Inscription" else ("Consolas", 8),
                          width=panel_w - 60)
            y += 90 if len(body) > 180 else 70
        c.create_text(cw // 2, CANVAS_H - 25, text=f"Page {self.lore_page + 1}/{len(LORE_PAGES)}    Left / Right: turn page    Esc: return",
                      fill=C["text_dim"], font=("Consolas", 8))
        self._draw_back_button(c)
        self._render_sidebar_tavern()

    def _render_settings(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        c.create_rectangle(0, 0, cw, CANVAS_H, fill=C["bg"], outline="")
        c.create_text(cw // 2, 80, text="SETTINGS", fill=C["gold"], font=("Georgia", 22, "bold"))
        music = "ON" if self.audio.enabled else "OFF"
        self._menu_button(c, cw // 2 - 170, 145, 340, f"Music: {music}", "music", True)
        c.create_text(cw // 2, 215, text="Tavern ambience plays from assets/audio/tavern.mp3.",
                      fill=C["text_dim"], font=("Georgia", 9, "italic"))
        c.create_text(cw // 2, 240, text="Music pauses when you leave the Tavern and returns when you come home.",
                      fill=C["text_dim"], font=("Consolas", 8))
        c.create_text(cw // 2, 290, text="Press M or Enter to toggle music.", fill=C["text"], font=("Consolas", 9))
        self._draw_back_button(c)
        self._render_sidebar_tavern()

    def _render_inheritance_board(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        c.create_rectangle(0, 0, cw, CANVAS_H, fill=C["bg"], outline="")
        title = "THE HOLLOW QUILL NOTICE" if self.inheritance_page == 0 else "A LETTER FROM THE HOLLOW QUILL"
        body = INHERITANCE_NOTICE if self.inheritance_page == 0 else HOLLOW_QUILL_LETTER
        panel_x, panel_y = 38, 74
        panel_w, panel_h = cw - 76, CANVAS_H - 128
        c.create_text(cw // 2, 34, text=title, fill=C["gold"], font=("Georgia", 20, "bold"), width=cw - 80)
        c.create_rectangle(panel_x, panel_y, panel_x + panel_w, panel_y + panel_h,
                           fill=C["panel"], outline=C["panel_edge"], width=1)
        c.create_text(panel_x + 34, panel_y + 30, anchor=tk.NW, text=body,
                      fill=C["text"] if self.inheritance_page == 0 else C["text_dim"],
                      font=("Georgia", 10), width=panel_w - 68)
        c.create_text(cw // 2, CANVAS_H - 25, text=f"Page {self.inheritance_page + 1}/2    Left / Right: turn page    Esc: return",
                      fill=C["text_dim"], font=("Consolas", 8))
        self._draw_back_button(c, "return_hub")
        self._render_sidebar_tavern()

    def _render_area_select(self):
        c = self.canvas
        c.delete("all")
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        c.create_text(cw // 2, 56, text="ETHEREA: ASHES OF THE SAINTS",
                      fill=C["gold"], font=("Georgia", 25, "bold"))
        c.create_text(cw // 2, 84, text="Pocket Roguelike",
                      fill=C["text_dim"], font=("Georgia", 11, "italic"))
        c.create_text(cw // 2, 108, text=CAMPAIGN_VERSION,
                      fill=C["text_dim"], font=("Consolas", 8))
        c.create_line(cw // 2 - 210, 126, cw // 2 + 210, 126, fill=C["panel_edge"])

        px, py, pw, ph = 96, 160, cw - 192, 166
        c.create_rectangle(px, py, px + pw, py + ph, fill=C["panel"], outline=C["gold"], width=2)
        c.create_text(cw // 2, py + 27, text="PLAY LATE-GAME PROTOTYPE",
                      fill=C["gold"], font=("Consolas", 11, "bold"))
        c.create_text(cw // 2, py + 58, text="Temple of the Sleepers - Blood Wing",
                      fill=C["text_bright"], font=("Georgia", 18, "bold"))
        c.create_text(cw // 2, py + 87,
                      text="Four rooms, three classes, relics, blood seals, and Vaelrith at the First Seal.",
                      fill=C["text_dim"], font=("Georgia", 9, "italic"), width=pw - 36)
        c.create_text(cw // 2, py + 128,
                      text="This is a late-game demo area, not the beginning of Etherea's canon progression.",
                      fill=C["text"], font=("Consolas", 8), width=pw - 36)

        c.create_text(cw // 2, 370, text="WORLD PROGRESSION",
                      fill=C["text_bright"], font=("Georgia", 15, "bold"))
        c.create_text(cw // 2, 396,
                      text="View the planned canon route from the Estate Intro to the Crystalline Dimension.",
                      fill=C["text_dim"], font=("Georgia", 9, "italic"))
        c.create_text(cw // 2, ch - 30,
                      text="Enter or 1: play prototype    2 or W: world progression",
                      fill=C["text_dim"], font=("Consolas", 10))
        self._render_sidebar_title_screen()

    def _render_world_progression(self):
        c = self.canvas
        c.delete("all")
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        c.create_text(cw // 2, 35, text="WORLD PROGRESSION",
                      fill=C["gold"], font=("Georgia", 21, "bold"))
        c.create_text(cw // 2, 58, text="Canon route - current playable content is marked as a prototype",
                      fill=C["text_dim"], font=("Georgia", 9, "italic"))

        areas = [(key, area) for key, area in campaign_areas() if key != "tavern"]
        for index, (_, area) in enumerate(areas):
            column = index // 8
            row = index % 8
            x = 25 + column * (cw // 2)
            y = 92 + row * 45
            status = area["status"]
            color = C["gold"] if status == "playable_prototype" else C["green"] if status == "playable" else C["text"]
            c.create_text(x, y, anchor=tk.W, text=f"{area['order']:02d}  {area['name']}",
                          fill=color, font=("Georgia", 10, "bold"))
            c.create_text(x, y + 14, anchor=tk.W, text=str(area["description"]),
                          fill=C["text_dim"], font=("Consolas", 7), width=cw // 2 - 42)
        c.create_text(cw // 2, ch - 24, text="Backspace, Esc, or W: return to demo select",
                      fill=C["text_dim"], font=("Consolas", 9))
        self._render_sidebar_title_screen()
    # ─── Class Selection ─────────────────────────────────────
    def _render_class_select(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        # Background
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        # Title
        c.create_text(cw // 2, 38, text="ETHEREA", fill=C["gold"],
                       font=("Georgia", 32, "bold"))
        c.create_text(cw // 2, 70, text="Ashes of the Saints  ·  Begin at the Hollow Hearth",
                       fill=C["text_dim"], font=("Georgia", 11, "italic"))
        # Decorative line
        lx = cw // 2
        c.create_line(lx - 180, 90, lx + 180, 90, fill=C["panel_edge"], width=1)
        # Class panels
        classes = [PlayerClass.WARDEN, PlayerClass.ASHEN_BLADE, PlayerClass.DREAMSEER]
        pw = 215
        gap = 15
        total = pw * 3 + gap * 2
        sx = (cw - total) // 2
        for i, pc in enumerate(classes):
            px = sx + i * (pw + gap)
            py = 105
            ph = 335
            stats = CLASS_STATS[pc]
            accent = CLASS_ACCENT[pc]
            selected = (i == self.selected_class_index)
            # Panel background
            border = accent if selected else C["panel_edge"]
            bw = 2 if selected else 1
            c.create_rectangle(px, py, px + pw, py + ph,
                               fill=C["panel"], outline=border, width=bw)
            # Selection indicator
            if selected:
                c.create_rectangle(px + 2, py + 2, px + pw - 2, py + 22,
                                   fill=accent, outline="")
                c.create_text(px + pw // 2, py + 12, text=f"▸ {i + 1} ◂",
                               fill=C["bg"], font=("Consolas", 9, "bold"))
            # Class name
            ny = py + 35
            c.create_text(px + pw // 2, ny, text=stats["name"],
                           fill=C["text_bright"], font=("Georgia", 15, "bold"))
            # Lore
            c.create_text(px + pw // 2, ny + 22, text=stats["lore"],
                           fill=C["text_dim"], font=("Georgia", 8, "italic"),
                           width=pw - 20)
            # Portrait art
            sprite_key = self._class_sprite_key(pc)
            portrait = self.images.get(sprite_key + "_p")
            py_img = ny + 66
            if portrait:
                c.create_oval(px + pw // 2 - 39, py_img - 39,
                              px + pw // 2 + 39, py_img + 39,
                              fill=C["bg"], outline=accent, width=1)
                c.create_image(px + pw // 2, py_img, image=portrait)
            else:
                c.create_oval(px + pw // 2 - 28, py_img - 28,
                              px + pw // 2 + 28, py_img + 28,
                              fill=accent, outline="")
            # Stats
            sy = ny + 115
            stat_labels = [
                ("HP", stats["hp"], C["hp_bar"]),
                ("ATK", stats["attack"], C["red"]),
                ("DEF", stats["defense"], C["blue"]),
                ("FOC", stats["focus"], C["focus_bar"]),
            ]
            for j, (label, val, clr) in enumerate(stat_labels):
                row_y = sy + j * 22
                c.create_text(px + 15, row_y, text=label, anchor=tk.W,
                               fill=C["text_dim"], font=("Consolas", 9))
                # Bar
                bar_x = px + 55
                bar_w = 110
                c.create_rectangle(bar_x, row_y - 7, bar_x + bar_w, row_y + 7,
                                   fill=C["bg"], outline=C["panel_edge"])
                fill_w = int(bar_w * min(val / 60, 1.0))
                if fill_w > 0:
                    c.create_rectangle(bar_x, row_y - 7, bar_x + fill_w, row_y + 7,
                                       fill=clr, outline="")
                c.create_text(bar_x + bar_w + 12, row_y, text=str(val),
                               fill=C["text"], font=("Consolas", 9, "bold"))
            # Ability
            ay = sy + 95
            c.create_text(px + pw // 2, ay, text=f"⚔ {stats['ability']}",
                           fill=accent, font=("Consolas", 10, "bold"))
            c.create_text(px + pw // 2, ay + 16, text=stats["ability_desc"],
                           fill=C["text_dim"], font=("Consolas", 8), width=pw - 20)
            # Passive
            psy = ay + 42
            c.create_text(px + pw // 2, psy, text=f"◈ {stats['passive']}",
                           fill=C["gold"], font=("Consolas", 9, "bold"))
            c.create_text(px + pw // 2, psy + 15, text=stats["passive_desc"],
                           fill=C["text_dim"], font=("Consolas", 8), width=pw - 20)
        # Instructions
        c.create_text(cw // 2, ch - 30,
                       text="← →  or  1 · 2 · 3  to select   ·   Enter to confirm",
                       fill=C["text_dim"], font=("Consolas", 10))
        # Sidebar — game info
        self._render_sidebar_title_screen()
    def _render_sidebar_title_screen(self):
        s = self.sidebar
        s.delete("all")
        sw = max(SIDEBAR_W, s.winfo_width())
        s.create_text(sw // 2, 42, text="ETHEREA",
                      fill=C["gold"], font=("Georgia", 21, "bold"))
        s.create_text(sw // 2, 68, text="Ashes of the Saints - Pocket Roguelike",
                      fill=C["text_dim"], font=("Georgia", 8, "italic"))
        s.create_line(22, 88, sw - 22, 88, fill=C["panel_edge"])
        s.create_text(sw // 2, 120, text="LATE-GAME PROTOTYPE / DEMO AREA",
                      fill=C["gold"], font=("Consolas", 9, "bold"))
        s.create_text(sw // 2, 150, text="Temple of the Sleepers: Blood Wing",
                      fill=C["text_bright"], font=("Georgia", 13, "bold"))
        s.create_text(sw // 2, 184,
                      text="The current playable dungeon belongs near the end of Etherea's full canon route.",
                      fill=C["text_dim"], font=("Georgia", 9, "italic"), width=sw - 40)
        s.create_text(sw // 2, 246, text="Campaign Foundation",
                      fill=C["text"], font=("Georgia", 12, "bold"))
        s.create_text(sw // 2, 275,
                      text="The Estate Intro, Foundries, Deeper Well, and later areas are registered as planned content.",
                      fill=C["text_dim"], font=("Consolas", 8), width=sw - 42)
        s.create_text(sw // 2, 355, text=CAMPAIGN_VERSION,
                      fill=C["text_dim"], font=("Consolas", 8))
        s.create_text(sw // 2, 500, text="F11: Fullscreen",
                      fill=C["text_dim"], font=("Consolas", 8))
        return
        s.create_text(sw // 2, 30, text="⛧", fill=C["gold"], font=("Georgia", 28))
        s.create_text(sw // 2, 70, text="Blood Wing", fill=C["gold"],
                       font=("Georgia", 16, "bold"))
        s.create_text(sw // 2, 95, text="A Dungeon of the First Seal",
                       fill=C["text_dim"], font=("Georgia", 9, "italic"))
        y = 140
        lore = [
            "Four rooms stand between",
            "the pilgrim and the seal.",
            "",
            "Three False Pilgrims guard",
            "the entrance. An Overseer",
            "watches the sleeping chains.",
            "A Knight waits in ritual",
            "silence. And behind them all—",
            "",
            "Vaelrith, Herald of the",
            "First Seal, patient and",
            "unyielding.",
            "",
            "Choose your class.",
            "Begin the descent.",
        ]
        for line in lore:
            s.create_text(sw // 2, y, text=line, fill=C["text_dim"],
                           font=("Georgia", 9))
            y += 18
    # ─── Difficulty Selection ────────────────────────────────
    def _render_difficulty_select(self):
        c = self.canvas
        c.delete("all")
        self.menu_hitboxes = []
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        c.create_text(cw // 2, 50, text="CHOOSE YOUR PATH",
                       fill=C["gold"], font=("Georgia", 22, "bold"))
        c.create_line(cw // 2 - 140, 72, cw // 2 + 140, 72,
                       fill=C["panel_edge"])
        diffs = [Difficulty.PILGRIM, Difficulty.WARDEN, Difficulty.MARTYR]
        diff_accents = [C["green"], C["gold"], C["red"]]
        pw = 200
        gap = 20
        total = pw * 3 + gap * 2
        sx = (cw - total) // 2
        for i, diff in enumerate(diffs):
            ds = DIFFICULTY_STATS[diff]
            px = sx + i * (pw + gap)
            py = 100
            ph = 280
            accent = diff_accents[i]
            selected = (i == self.selected_diff_index)
            border = accent if selected else C["panel_edge"]
            bw = 2 if selected else 1
            c.create_rectangle(px, py, px + pw, py + ph,
                               fill=C["panel"], outline=border, width=bw)
            if selected:
                c.create_rectangle(px + 2, py + 2, px + pw - 2, py + 22,
                                   fill=accent, outline="")
                c.create_text(px + pw // 2, py + 12, text=f"▸ {i + 1} ◂",
                               fill=C["bg"], font=("Consolas", 9, "bold"))
            c.create_text(px + pw // 2, py + 42, text=ds["name"],
                           fill=C["text_bright"], font=("Georgia", 16, "bold"))
            c.create_text(px + pw // 2, py + 68, text=ds["desc"],
                           fill=C["text_dim"], font=("Georgia", 9, "italic"),
                           width=pw - 20)
            # Modifier details
            my = py + 110
            mods = [
                f"Enemy HP: ×{ds['hp_mult']:.1f}",
                f"Enemy ATK: {'+' if ds['atk_bonus'] >= 0 else ''}{ds['atk_bonus']}",
                f"Start Vials: {ds['vials']}",
                f"Shard Mult: ×{ds['shard_mult']:.2f}",
            ]
            for j, txt in enumerate(mods):
                c.create_text(px + pw // 2, my + j * 22, text=txt,
                               fill=C["text"], font=("Consolas", 9))
        c.create_text(cw // 2, ch - 30,
                       text="← →  or  1 · 2 · 3  to select   ·   Enter to confirm",
                       fill=C["text_dim"], font=("Consolas", 10))
        # Sidebar stays
        self._render_sidebar_title_screen()
    # ─── Game Rendering ──────────────────────────────────────
    def _render_game(self):
        self._render_grid()
        self._render_sidebar_game()
        self._flush_canvas_effects()
    def _render_grid(self):
        c = self.canvas
        c.delete("all")
        room_clear = self._is_room_clear()
        for gy in range(GRID_H):
            for gx in range(GRID_W):
                ch = self.grid[gy][gx] if gy < len(self.grid) and gx < len(self.grid[gy]) else "#"
                x1 = gx * TILE
                y1 = gy * TILE
                x2 = x1 + TILE
                y2 = y1 + TILE
                # Base tile colour
                if ch == "#":
                    fill = C["wall"] if (gx + gy) % 2 == 0 else C["wall_hi"]
                    c.create_rectangle(x1, y1, x2, y2, fill=fill, outline=C["bg"], width=1)
                elif ch == "~":
                    c.create_rectangle(x1, y1, x2, y2, fill=C["trap"], outline=C["bg"], width=1)
                    c.create_text(x1 + TILE // 2, y1 + TILE // 2, text="~",
                                   fill=C["trap_glow"], font=("Consolas", 16))
                elif ch == "!":
                    c.create_rectangle(x1, y1, x2, y2, fill=C["reliq"], outline=C["bg"], width=1)
                    c.create_text(x1 + TILE // 2, y1 + TILE // 2, text="✦",
                                   fill=C["reliq_icon"], font=("Consolas", 14))
                elif ch == "†":
                    c.create_rectangle(x1, y1, x2, y2, fill=C["shrine"], outline=C["bg"], width=1)
                    c.create_text(x1 + TILE // 2, y1 + TILE // 2, text="†",
                                   fill=C["shrine_icon"], font=("Georgia", 18))
                elif ch == ">":
                    if room_clear:
                        glow = C["exit_glow"] if self.exit_pulse_on else C["exit_open"]
                        c.create_rectangle(x1, y1, x2, y2, fill=glow, outline=C["gold"], width=2)
                        if not self._draw_sprite(c, "exit_rune", x1 + TILE // 2, y1 + TILE // 2):
                            c.create_text(x1 + TILE // 2, y1 + TILE // 2, text="▶",
                                          fill=C["bg"], font=("Consolas", 16, "bold"))
                    else:
                        c.create_rectangle(x1, y1, x2, y2, fill=C["exit_locked"],
                                           outline=C["bg"], width=1)
                        c.create_text(x1 + TILE // 2, y1 + TILE // 2, text="▷",
                                       fill=C["text_dim"], font=("Consolas", 14))
                elif ch in ("e", "l", "i", "b", "h"):
                    fill = C["floor"] if (gx + gy) % 2 == 0 else C["floor_alt"]
                    c.create_rectangle(x1, y1, x2, y2, fill=fill, outline="", width=0)
                    glyphs = {"e": "E", "l": "L", "i": "I", "b": "B", "h": "*"}
                    colors = {"e": C["gold"], "l": C["purple"], "i": C["text_bright"], "b": C["green"], "h": "#d46a32"}
                    if not self._draw_sprite(c, TAVERN_TILE_SPRITES[ch], x1 + TILE // 2, y1 + TILE // 2):
                        c.create_text(x1 + TILE // 2, y1 + TILE // 2, text=glyphs[ch],
                                      fill=colors[ch], font=("Consolas", 14, "bold"))
                else:
                    # Floor (chequered)
                    fill = C["floor"] if (gx + gy) % 2 == 0 else C["floor_alt"]
                    c.create_rectangle(x1, y1, x2, y2, fill=fill, outline="", width=0)
                    if self.area_id == "tavern":
                        self._draw_sprite(c, "tavern_floor", x1 + TILE // 2, y1 + TILE // 2)
        # Enemies
        bob = -2 if self.exit_pulse_on else 0
        for en in self.enemies:
            if not en.is_alive:
                continue
            cx = en.x * TILE + TILE // 2
            cy = en.y * TILE + TILE // 2 + bob
            ex1 = en.x * TILE + 4
            ey1 = en.y * TILE + 4 + bob
            ex2 = ex1 + TILE - 8
            ey2 = ey1 + TILE - 8
            clr = ENEMY_CLR.get(en.enemy_type, C["red"])
            if en.is_boss:
                # Vaelrith gets a larger ring and sprite so the boss reads clearly.
                c.create_oval(cx - 25, cy - 25, cx + 25, cy + 25,
                              fill="", outline=C["boss_bar"], width=2)
                drew = self._draw_sprite(c, self._entity_sprite_key(en.enemy_type), cx, cy, boss=True)
            else:
                c.create_oval(cx - 17, cy - 17, cx + 17, cy + 17,
                              fill=C["bg"], outline=clr, width=1)
                drew = self._draw_sprite(c, self._entity_sprite_key(en.enemy_type), cx, cy)
            if not drew:
                c.create_oval(ex1, ey1, ex2, ey2, fill=clr, outline="")
                letter = en.name[0]
                c.create_text(cx, cy, text=letter, fill=C["text_bright"],
                              font=("Consolas", 12, "bold"))
            # HP pip
            if en.hp < en.max_hp:
                bar_w = TILE - 8
                bar_x = en.x * TILE + 4
                bar_y = en.y * TILE + 2
                ratio = max(0, en.hp / en.max_hp)
                c.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + 3,
                                   fill=C["hp_bg"], outline="")
                c.create_rectangle(bar_x, bar_y, bar_x + int(bar_w * ratio), bar_y + 3,
                                   fill=C["hp_bar"], outline="")
            # Status glyphs
            glyphs = []
            if en.has_status(StatusType.STUN):
                glyphs.append(("✦", C["gold"]))
            if en.has_status(StatusType.BLEED):
                glyphs.append(("♦", C["bleed"]))
            for gi, (g, gc) in enumerate(glyphs):
                c.create_text(en.x * TILE + TILE - 6, en.y * TILE + 6 + gi * 10,
                               text=g, fill=gc, font=("Consolas", 7))
        if self.area_id == "tavern":
            for npc in TAVERN_NPCS:
                cx = npc.position[0] * TILE + TILE // 2
                cy = npc.position[1] * TILE + TILE // 2
                key = TAVERN_NPC_SPRITES.get(npc.name, "")
                if not self._draw_sprite(c, key, cx, cy):
                    c.create_oval(cx - 14, cy - 14, cx + 14, cy + 14, fill=C["panel"], outline=C["gold"], width=1)
                    c.create_text(cx, cy, text=npc.name[0], fill=C["text_bright"], font=("Consolas", 11, "bold"))
                c.create_text(cx, cy - 22, text=npc.name.split()[0], fill=C["gold"], font=("Consolas", 6, "bold"))
        # Player
        if self.player and self.player.is_alive:
            pcx = self.player.x * TILE + TILE // 2
            pcy = self.player.y * TILE + TILE // 2 + (-2 if self.exit_pulse_on else 0)
            accent = CLASS_ACCENT.get(self.player.player_class, C["player_out"])
            c.create_oval(pcx - 19, pcy - 19, pcx + 19, pcy + 19,
                          fill=C["bg"], outline=accent, width=2)
            drew = self._draw_sprite(c, self._class_sprite_key(self.player.player_class), pcx, pcy)
            if not drew:
                c.create_oval(pcx - 17, pcy - 17, pcx + 17, pcy + 17,
                              fill=C["player"], outline=C["player_out"], width=2)
                c.create_text(pcx, pcy, text="@", fill=C["text_bright"],
                              font=("Consolas", 14, "bold"))
        # Boss health bar (top of canvas)
        boss = self._get_boss()
        if boss and boss.is_alive:
            self._render_boss_bar(boss)
        # Shrine / Shop overlays
        if self.state == GameState.SHRINE_PROMPT:
            self._render_prompt_overlay("Saint Shrine", [
                "1 › Restore 16 HP",
                "2 › Restore 6 focus, gain +1 Blood Vial",
            ])
        elif self.state == GameState.SHOP_PROMPT:
            opts = ["1 › Spend 30 shards for +1 Blood Vial"]
            if self.relic_pool:
                r = self.relic_pool[0]
                opts.append(f"2 › Spend 40 shards for relic: {r.name}")
                opts.append("3 › Keep shards and continue")
            else:
                opts.append("2 › Keep shards and continue")
            self._render_prompt_overlay("Reliquary Merchant", opts)
    def _render_boss_bar(self, boss: Enemy):
        c = self.canvas
        bw = CANVAS_W - 60
        bx = 30
        by = 8
        bh = 18
        # Background
        c.create_rectangle(bx - 2, by - 2, bx + bw + 2, by + bh + 2,
                           fill=C["bg"], outline=C["panel_edge"])
        c.create_rectangle(bx, by, bx + bw, by + bh, fill=C["boss_bg"], outline="")
        # Fill
        ratio = max(0, boss.hp / boss.max_hp)
        fill_w = int(bw * ratio)
        if fill_w > 0:
            bar_clr = C["boss_bar"]
            if boss.boss_phase == 3:
                bar_clr = "#e02050"
            elif boss.boss_phase == 2:
                bar_clr = "#d04060"
            c.create_rectangle(bx, by, bx + fill_w, by + bh, fill=bar_clr, outline="")
        # Phase markers at 50% and 25%
        for pct in (0.5, 0.25):
            mx = bx + int(bw * pct)
            c.create_line(mx, by, mx, by + bh, fill=C["text_dim"], width=1)
        # Name and HP
        c.create_text(bx + bw // 2, by + bh // 2,
                       text=f"Vaelrith  —  {boss.hp}/{boss.max_hp}  (Phase {boss.boss_phase})",
                       fill=C["text_bright"], font=("Consolas", 9, "bold"))
    def _render_prompt_overlay(self, title: str, options: list):
        c = self.canvas
        ow = 380
        oh = 40 + len(options) * 30 + 20
        ox = (CANVAS_W - ow) // 2
        oy = (CANVAS_H - oh) // 2
        # Shadow
        c.create_rectangle(ox + 4, oy + 4, ox + ow + 4, oy + oh + 4,
                           fill="#000000", outline="", stipple="gray25")
        # Panel
        c.create_rectangle(ox, oy, ox + ow, oy + oh,
                           fill=C["panel"], outline=C["gold"], width=2)
        # Title
        c.create_text(ox + ow // 2, oy + 20, text=title,
                       fill=C["gold"], font=("Georgia", 13, "bold"))
        # Options
        for i, opt in enumerate(options):
            c.create_text(ox + ow // 2, oy + 50 + i * 30, text=opt,
                           fill=C["text"], font=("Consolas", 10))
    # ─── Sidebar (Gameplay) ──────────────────────────────────
    def _render_sidebar_game(self):
        s = self.sidebar
        s.delete("all")
        sw = max(SIDEBAR_W, s.winfo_width())
        p = self.player
        if not p:
            return
        y = 10
        # Room name
        content = AREA_CONTENT.get(self.area_id, AREA_CONTENT["blood_wing"])
        meta = content["meta"][self.room_index]
        s.create_text(sw // 2, y + 8, text=meta["name"],
                       fill=C["gold"], font=("Georgia", 14, "bold"))
        y += 26
        # Subtitle
        s.create_text(sw // 2, y + 4, text=meta["subtitle"],
                       fill=C["text_dim"], font=("Georgia", 8, "italic"),
                       width=sw - 30)
        y += 38
        # Room modifier
        if self.room_modifier:
            s.create_text(sw // 2, y, text=f"⚑ {self.room_modifier.name}",
                           fill="#8a6a4a", font=("Consolas", 9, "bold"))
            s.create_text(sw // 2, y + 14, text=self.room_modifier.description,
                           fill=C["text_dim"], font=("Consolas", 7), width=sw - 30)
            y += 30
        # Separator
        s.create_line(15, y, sw - 15, y, fill=C["panel_edge"])
        y += 8
        # Objective
        s.create_text(sw // 2, y + 4, text=meta["objective"],
                       fill=C["text_dim"], font=("Consolas", 9), width=sw - 30)
        y += 22
        # Separator
        s.create_line(15, y, sw - 15, y, fill=C["panel_edge"])
        y += 10
        # Player class and portrait
        accent = CLASS_ACCENT[p.player_class]
        portrait = self.images.get(self._class_sprite_key(p.player_class) + "_p")
        if portrait:
            s.create_oval(20, y - 8, 84, y + 56, fill=C["bg"], outline=accent, width=1)
            s.create_image(52, y + 24, image=portrait)
            s.create_text(96, y + 10, anchor=tk.W, text=f"☩ {p.name}",
                          fill=accent, font=("Georgia", 12, "bold"))
            s.create_text(96, y + 30, anchor=tk.W, text=p.player_class.value,
                          fill=C["text_dim"], font=("Consolas", 8))
            y += 64
        else:
            s.create_text(sw // 2, y, text=f"☩ {p.name}",
                          fill=accent, font=("Georgia", 12, "bold"))
            y += 22
        # HP Bar
        self._draw_bar(s, 20, y, sw - 40, 16,
                       p.hp, p.max_hp, C["hp_bar"], C["hp_bg"],
                       f"HP  {p.hp}/{p.max_hp}")
        y += 24
        # Focus Bar
        self._draw_bar(s, 20, y, sw - 40, 16,
                       p.focus, p.max_focus, C["focus_bar"], C["focus_bg"],
                       f"FOC {p.focus}/{p.max_focus}")
        y += 24
        # Stats row
        stats_text = f"ATK {p.attack}    DEF {p.defense}"
        s.create_text(sw // 2, y, text=stats_text,
                       fill=C["text"], font=("Consolas", 10))
        y += 20
        # Blood Vials & Shards
        s.create_text(20, y, anchor=tk.W,
                       text=f"♥ Blood Vials: {p.blood_vials}",
                       fill=C["red"], font=("Consolas", 10))
        y += 18
        s.create_text(20, y, anchor=tk.W,
                       text=f"◆ Relic Shards: {p.relic_shards}",
                       fill=C["gold"], font=("Consolas", 10))
        y += 18
        # Difficulty
        s.create_text(20, y, anchor=tk.W,
                       text=f"Path: {self.difficulty.value}",
                       fill=C["text_dim"], font=("Consolas", 9))
        y += 16
        # Separator
        s.create_line(15, y, sw - 15, y, fill=C["panel_edge"])
        y += 8
        # Relics
        if p.relics:
            s.create_text(20, y, anchor=tk.W, text="Relics:",
                           fill=C["gold"], font=("Consolas", 9, "bold"))
            y += 16
            for rid in p.relics:
                relic = self._relic_by_id(rid)
                if relic:
                    s.create_text(28, y, anchor=tk.W,
                                   text=f"{relic.icon} {relic.name}",
                                   fill=C["text"], font=("Consolas", 8))
                    y += 14
            y += 4
        # Status effects
        if p.status_effects:
            s.create_text(20, y, anchor=tk.W, text="Status:",
                           fill=C["purple"], font=("Consolas", 9, "bold"))
            y += 16
            for eff in p.status_effects:
                icon = "♦" if eff.type == StatusType.BLEED else "✦" if eff.type == StatusType.STUN else "⚡"
                s.create_text(28, y, anchor=tk.W,
                               text=f"{icon} {eff.type.value} ({eff.duration}t)",
                               fill=C["bleed"] if eff.type == StatusType.BLEED else C["gold"],
                               font=("Consolas", 8))
                y += 14
            y += 4
        # Separator
        s.create_line(15, y, sw - 15, y, fill=C["panel_edge"])
        y += 6
        # Event log (last N entries)
        s.create_text(20, y, anchor=tk.W, text="Event Log",
                       fill=C["text_dim"], font=("Consolas", 9, "bold"))
        y += 14
        log_max = 6 if self.area_id == "tavern" else 12
        display_log = self.event_log[-log_max:]
        for entry in display_log:
            # Colour code
            clr = C["text_dim"]
            if "damage" in entry.lower() or "hit" in entry.lower():
                clr = C["red"]
            elif "heal" in entry.lower() or "restore" in entry.lower():
                clr = C["heal"]
            elif "defeated" in entry.lower() or "shard" in entry.lower():
                clr = C["gold"]
            elif "bleed" in entry.lower() or "blood" in entry.lower():
                clr = C["bleed"]
            elif "stun" in entry.lower():
                clr = C["blue"]
            line_width = max(38, (sw - 40) // 6)
            wrapped = []
            for paragraph in entry.splitlines() or [""]:
                wrapped.extend(textwrap.wrap(paragraph, width=line_width) or [""])
            for line in wrapped:
                s.create_text(20, y, anchor=tk.W, text=line,
                              fill=clr, font=("Consolas", 8))
                y += 12
        # Controls (at bottom)
        y = max(y + 10, 520)
        s.create_line(15, y, sw - 15, y, fill=C["panel_edge"])
        y += 8
        controls = [
            "WASD/Arrows: Move    Space: Attack",
            "Q: Ability   E: Vial   R: Focus",
            "B: Save   L: Load   F: Interact",
            "F11: Fullscreen",
        ]
        for line in controls:
            s.create_text(sw // 2, y, text=line,
                           fill=C["text_dim"], font=("Consolas", 7))
            y += 12
    def _draw_bar(self, canvas, x, y, w, h, val, max_val, fill_clr, bg_clr, label):
        canvas.create_rectangle(x, y, x + w, y + h, fill=bg_clr, outline=C["panel_edge"])
        ratio = max(0, min(1, val / max_val)) if max_val > 0 else 0
        fw = int(w * ratio)
        if fw > 0:
            # Gradient effect — slightly lighter at top
            canvas.create_rectangle(x, y, x + fw, y + h, fill=fill_clr, outline="")
            lighter = self._lighten(fill_clr, 30)
            canvas.create_rectangle(x, y, x + fw, y + h // 2, fill=lighter, outline="")
        canvas.create_text(x + w // 2, y + h // 2, text=label,
                           fill=C["text_bright"], font=("Consolas", 8, "bold"))
    @staticmethod
    def _lighten(hex_clr: str, amount: int) -> str:
        hex_clr = hex_clr.lstrip("#")
        r = min(255, int(hex_clr[0:2], 16) + amount)
        g = min(255, int(hex_clr[2:4], 16) + amount)
        b = min(255, int(hex_clr[4:6], 16) + amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    # ─── Victory / Defeat ────────────────────────────────────
    def _render_victory(self):
        c = self.canvas
        c.delete("all")
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill=C["bg"], outline="")
        c.create_text(cw // 2, 40, text="THE SEAL IS BROKEN",
                       fill=C["gold"], font=("Georgia", 24, "bold"))
        c.create_text(cw // 2, 72, text="Vaelrith has fallen. The Blood Wing is silent.",
                       fill=C["text_dim"], font=("Georgia", 10, "italic"))
        # Score summary
        rs = self.run_stats
        y = 110
        rank = self._calc_rank()
        summary = [
            ("Class", self.player.name if self.player else "?"),
            ("Difficulty", self.difficulty.value),
            ("Turns", str(rs.turns)),
            ("Enemies Defeated", str(rs.enemies_defeated)),
            ("Shards Collected", str(rs.shards_collected)),
            ("Potions Used", str(rs.potions_used)),
            ("Relics Found", str(rs.relics_found)),
            ("Shrines Visited", str(rs.shrines_visited)),
            ("Damage Dealt", str(rs.damage_dealt)),
            ("Damage Taken", str(rs.damage_taken)),
        ]
        for label, val in summary:
            c.create_text(cw // 2 - 80, y, anchor=tk.E, text=label,
                           fill=C["text_dim"], font=("Consolas", 10))
            c.create_text(cw // 2 - 60, y, anchor=tk.W, text=val,
                           fill=C["text"], font=("Consolas", 10, "bold"))
            y += 22
        # Rank
        y += 10
        rank_clr = {
            "S": "#f0d040", "A": "#60c060", "B": "#40a0c0",
            "C": "#a0a0a0", "D": "#6a5a5a",
        }.get(rank, C["text"])
        c.create_text(cw // 2, y, text=f"RANK: {rank}",
                       fill=rank_clr, font=("Georgia", 28, "bold"))
        c.create_text(cw // 2, ch - 25,
                       text="Press  N  for New Game",
                       fill=C["text_dim"], font=("Consolas", 10))
        # Sidebar
        self._render_sidebar_title_screen()
    def _render_defeat(self):
        c = self.canvas
        c.delete("all")
        cw = max(CANVAS_W, c.winfo_width())
        ch = max(CANVAS_H, c.winfo_height())
        c.create_rectangle(0, 0, cw, ch, fill="#0a0508", outline="")
        c.create_text(cw // 2, ch // 2 - 40, text="YOU HAVE FALLEN",
                       fill=C["red"], font=("Georgia", 26, "bold"))
        c.create_text(cw // 2, ch // 2,
                       text="The Blood Wing claims another pilgrim.",
                       fill=C["text_dim"], font=("Georgia", 10, "italic"))
        c.create_text(cw // 2, ch // 2 + 50,
                       text="Press  N  for New Game   ·   L  to Load",
                       fill=C["text_dim"], font=("Consolas", 10))
        self._render_sidebar_title_screen()
    def _calc_rank(self) -> str:
        rs = self.run_stats
        score = 0
        # Fewer turns → better
        if rs.turns < 60:
            score += 4
        elif rs.turns < 90:
            score += 3
        elif rs.turns < 130:
            score += 2
        elif rs.turns < 180:
            score += 1
        # Potions used (fewer → better)
        if rs.potions_used <= 2:
            score += 2
        elif rs.potions_used <= 4:
            score += 1
        # Relics found
        score += min(rs.relics_found, 2)
        # Difficulty bonus
        if self.difficulty == Difficulty.MARTYR:
            score += 3
        elif self.difficulty == Difficulty.WARDEN:
            score += 1
        if score >= 10:
            return "S"
        elif score >= 7:
            return "A"
        elif score >= 5:
            return "B"
        elif score >= 3:
            return "C"
        return "D"
    # ═══════════════════════════════════════════════════════════
    # INPUT HANDLING
    # ═══════════════════════════════════════════════════════════
    def _on_key(self, event):
        if self.headless:
            return
        key = event.keysym.lower()
        if self.state == GameState.TAVERN:
            self._handle_tavern_key(key)
        elif self.state == GameState.EXPEDITION_BOARD:
            self._handle_expedition_key(key)
        elif self.state == GameState.TUTORIAL:
            self._handle_simple_back_key(key)
        elif self.state == GameState.LORE_BOOK:
            self._handle_lore_key(key)
        elif self.state == GameState.SETTINGS:
            self._handle_settings_key(key)
        elif self.state == GameState.INHERITANCE_BOARD:
            self._handle_inheritance_key(key)
        elif self.state == GameState.AREA_SELECT:
            self._handle_area_select_key(key)
        elif self.state == GameState.WORLD_PROGRESSION:
            self._handle_world_progression_key(key)
        elif self.state == GameState.CLASS_SELECT:
            self._handle_class_select_key(key)
        elif self.state == GameState.DIFFICULTY_SELECT:
            self._handle_difficulty_key(key)
        elif self.state == GameState.PLAYING:
            self._handle_playing_key(key)
        elif self.state == GameState.SHRINE_PROMPT:
            self._handle_shrine_key(key)
        elif self.state == GameState.SHOP_PROMPT:
            self._handle_shop_key(key)
        elif self.state in (GameState.VICTORY, GameState.DEFEAT):
            if key == "n":
                self._new_game()
            elif key == "l" and self.state == GameState.DEFEAT:
                self._load_game()
    def _on_canvas_click(self, event):
        """Handle mouse clicks on the class selection panels."""
        for x1, y1, x2, y2, action in self.menu_hitboxes:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self._activate_menu_action(action)
                return
        if self.state == GameState.CLASS_SELECT:
            cw = max(CANVAS_W, self.canvas.winfo_width())
            pw = 215
            gap = 15
            total = pw * 3 + gap * 2
            sx = (cw - total) // 2
            for i in range(3):
                px = sx + i * (pw + gap)
                if px <= event.x <= px + pw and 105 <= event.y <= 440:
                    self.selected_class_index = i
                    self._render()
                    return

    def _activate_menu_action(self, action: str):
        self.audio.play("click")
        if action.startswith("area:"):
            self._begin_expedition(action.split(":", 1)[1])
        elif action == "new_game":
            self.state = GameState.CLASS_SELECT
            self._render()
        elif action == "continue":
            if os.path.exists(self.save_path):
                self._load_game()
            else:
                self.state = GameState.CLASS_SELECT
                self._render()
        elif action == "expedition":
            self.state = GameState.EXPEDITION_BOARD
            self._render()
        elif action == "blood_wing":
            self.area_id = "blood_wing"
            self.area_status = AREA_REGISTRY[self.area_id]["status"]
            self.state = GameState.CLASS_SELECT
            self._render()
        elif action == "tutorial":
            self.state = GameState.TUTORIAL
            self._render()
        elif action == "lore":
            self.state = GameState.LORE_BOOK
            self.lore_page = 0
            self._render()
        elif action == "inheritance":
            self.state = GameState.INHERITANCE_BOARD
            self.inheritance_page = 0
            self._render()
        elif action == "world":
            self.state = GameState.WORLD_PROGRESSION
            self._render()
        elif action == "settings":
            self.state = GameState.SETTINGS
            self._render()
        elif action == "music":
            self.audio.toggle()
            self._render()
        elif action == "tavern":
            self.state = GameState.TAVERN
            self._render()
        elif action == "return_hub":
            self.state = GameState.PLAYING
            self._render()
        elif action == "quit":
            self.root.destroy()

    def _handle_tavern_key(self, key):
        actions = ("new_game", "continue", "tutorial", "lore", "world", "settings", "quit")
        if key in ("up", "w"):
            self.tavern_index = (self.tavern_index - 1) % len(TAVERN_MENU)
        elif key in ("down", "s"):
            self.tavern_index = (self.tavern_index + 1) % len(TAVERN_MENU)
        elif key in ("1", "2", "3", "4", "5", "6", "7"):
            self.tavern_index = int(key) - 1
            self._activate_menu_action(actions[self.tavern_index])
            return
        elif key == "return":
            self._activate_menu_action(actions[self.tavern_index])
            return
        else:
            return
        self._render()

    def _handle_expedition_key(self, key):
        playable_ids = ("tutorial_estate", "foundries_and_forges", "blood_wing")
        if key in ("up", "w"):
            self.expedition_index = (self.expedition_index - 1) % len(playable_ids)
            self._render()
        elif key in ("down", "s"):
            self.expedition_index = (self.expedition_index + 1) % len(playable_ids)
            self._render()
        elif key in ("return", "1", "2", "3"):
            if key in ("1", "2", "3"):
                self.expedition_index = int(key) - 1
            self._begin_expedition(playable_ids[self.expedition_index])
        elif key in ("escape", "backspace"):
            if self.player and self.area_id == "tavern":
                self.state = GameState.PLAYING
                self._render()
            else:
                self._activate_menu_action("tavern")

    def _handle_simple_back_key(self, key):
        if key in ("escape", "backspace", "return"):
            self._activate_menu_action("tavern")

    def _handle_lore_key(self, key):
        if key in ("left", "a"):
            self.lore_page = (self.lore_page - 1) % len(LORE_PAGES)
            self._render()
        elif key in ("right", "d"):
            self.lore_page = (self.lore_page + 1) % len(LORE_PAGES)
            self._render()
        elif key in ("escape", "backspace"):
            self._activate_menu_action("tavern")

    def _handle_settings_key(self, key):
        if key in ("m", "return"):
            self._activate_menu_action("music")
        elif key in ("escape", "backspace"):
            self._activate_menu_action("tavern")

    def _handle_inheritance_key(self, key):
        if key in ("left", "a", "right", "d"):
            self.inheritance_page = 1 - self.inheritance_page
            self._render()
        elif key in ("escape", "backspace"):
            self._activate_menu_action("return_hub")

    def _handle_area_select_key(self, key):
        if key in ("return", "1"):
            self.state = GameState.EXPEDITION_BOARD
        elif key in ("2", "w"):
            self.state = GameState.WORLD_PROGRESSION
        else:
            return
        self._render()

    def _handle_world_progression_key(self, key):
        if key in ("backspace", "escape", "return", "w"):
            self.state = GameState.TAVERN
            self._render()
    def _handle_class_select_key(self, key):
        if key in ("1", "2", "3"):
            self.selected_class_index = int(key) - 1
        elif key in ("left", "a"):
            self.selected_class_index = (self.selected_class_index - 1) % 3
        elif key in ("right", "d"):
            self.selected_class_index = (self.selected_class_index + 1) % 3
        elif key == "return":
            self.state = GameState.DIFFICULTY_SELECT
        elif key in ("backspace", "escape"):
            self.state = GameState.EXPEDITION_BOARD
        else:
            return
        self._render()
    def _handle_difficulty_key(self, key):
        if key in ("1", "2", "3"):
            self.selected_diff_index = int(key) - 1
        elif key in ("left", "a"):
            self.selected_diff_index = (self.selected_diff_index - 1) % 3
        elif key in ("right", "d"):
            self.selected_diff_index = (self.selected_diff_index + 1) % 3
        elif key == "return":
            self._start_game()
            return
        elif key in ("backspace", "escape"):
            self.state = GameState.CLASS_SELECT
        else:
            return
        self._render()
    def _handle_playing_key(self, key):
        if key in ("w", "up"):
            self._move_player(0, -1)
        elif key in ("s", "down"):
            self._move_player(0, 1)
        elif key in ("a", "left"):
            self._move_player(-1, 0)
        elif key in ("d", "right"):
            self._move_player(1, 0)
        elif key == "space":
            self._player_attack()
        elif key == "q":
            self._use_ability()
        elif key == "e":
            self._use_vial()
        elif key == "r":
            self._recover_focus()
        elif key == "b":
            self._save_game()
        elif key == "l":
            self._load_game()
        elif key == "f":
            if self.area_id == "tavern":
                self._interact_tavern()
            elif self.player and self.grid[self.player.y][self.player.x] == ">":
                self._exit_interact()
    def _handle_shrine_key(self, key):
        if key == "1":
            self._shrine_choose(1)
        elif key == "2":
            self._shrine_choose(2)
    def _handle_shop_key(self, key):
        if key == "1":
            self._shop_choose(1)
        elif key == "2":
            if self.relic_pool:
                self._shop_choose(2)
            else:
                self._shop_choose(0)  # continue
        elif key == "3" and self.relic_pool:
            self._shop_choose(0)  # continue
    # ═══════════════════════════════════════════════════════════
    # GAME FLOW
    # ═══════════════════════════════════════════════════════════
    def _start_game(self):
        classes = [PlayerClass.WARDEN, PlayerClass.ASHEN_BLADE, PlayerClass.DREAMSEER]
        diffs = [Difficulty.PILGRIM, Difficulty.WARDEN, Difficulty.MARTYR]
        self.selected_class = classes[self.selected_class_index]
        self.difficulty = diffs[self.selected_diff_index]
        self.area_id = "tavern"
        self.area_status = AREA_REGISTRY[self.area_id]["status"]
        self.player = create_player(self.selected_class, self.difficulty)
        self.run_stats = RunStats()
        self.relic_pool = list(ALL_RELICS)
        random.shuffle(self.relic_pool)
        self.room_index = 0
        self.cleared_areas = set()
        self.turn_count = 0
        self.event_log = []
        self._log(f"{self.player.name} enters the Hollow Hearth Tavern.")
        self._log(f"Difficulty: {self.difficulty.value}")
        self._load_room(0)
        self.state = GameState.PLAYING
        self.audio.play("tavern")
        self._start_exit_pulse()
        self._render()

    def _begin_expedition(self, area_id: str):
        if not self.player:
            self.state = GameState.CLASS_SELECT
            self._render()
            return
        if area_id not in AREA_CONTENT:
            return
        self.area_id = area_id
        self.area_status = AREA_REGISTRY[area_id]["status"]
        self.room_index = 0
        self._log(f"Expedition begun: {AREA_REGISTRY[area_id]['name']}.")
        self._load_room(0)
        self.state = GameState.PLAYING
        if area_id == "tavern":
            self.audio.play("tavern")
        else:
            self.audio.stop()
        self._render()

    def _return_to_tavern(self, message: str):
        self.cleared_areas.add(self.area_id)
        self.area_id = "tavern"
        self.area_status = AREA_REGISTRY[self.area_id]["status"]
        self.room_index = 0
        self._load_room(0)
        self.state = GameState.PLAYING
        self._log(message)
        self.audio.play("tavern")
        self._render()
    def _new_game(self):
        self.audio.stop()
        self.state = GameState.TAVERN
        self.selected_class_index = 0
        self.selected_diff_index = 1
        self.player = None
        self.enemies = []
        self.grid = []
        self.event_log = []
        self._stop_exit_pulse()
        self._render()
    # ─── Room Loading ────────────────────────────────────────
    def _load_room(self, index: int):
        self.room_index = index
        content = AREA_CONTENT.get(self.area_id, AREA_CONTENT["blood_wing"])
        layout = content["rooms"][index]
        self.grid = []
        self.enemies = []
        for gy, row in enumerate(layout):
            grid_row = []
            for gx, ch in enumerate(row):
                if ch == "@":
                    if self.player:
                        self.player.x = gx
                        self.player.y = gy
                    grid_row.append(".")
                elif ch in ENEMY_MARKERS:
                    etype = ENEMY_MARKERS[ch]
                    enemy = create_enemy(etype, self.difficulty, gx, gy)
                    self.enemies.append(enemy)
                    grid_row.append(".")
                else:
                    grid_row.append(ch)
            self.grid.append(grid_row)
        # Room modifier (not for boss room)
        if self.area_id == "blood_wing" and index < 3:
            self.room_modifier = random.choice(ROOM_MODIFIERS)
            self._log(f"Modifier: {self.room_modifier.name}")
        else:
            self.room_modifier = None
        # Reset per-room passive tracking
        if self.player:
            self.player.first_hit_this_room = True
            self.player.first_attack_this_room = True
        meta = content["meta"][index]
        self._log(f"— {meta['name']} —")
        self.turn_count = 0
    # ═══════════════════════════════════════════════════════════
    # PLAYER ACTIONS
    # ═══════════════════════════════════════════════════════════
    def _move_player(self, dx: int, dy: int):
        if not self.player or not self.player.is_alive:
            return
        nx = self.player.x + dx
        ny = self.player.y + dy
        if not self._in_bounds(nx, ny):
            return
        # Check for enemy at target
        target_enemy = self._enemy_at(nx, ny)
        if target_enemy:
            self._attack_enemy(target_enemy)
            self._end_turn()
            return
        tile = self.grid[ny][nx]
        if tile == "#":
            return
        self.player.x = nx
        self.player.y = ny
        self._on_tile_enter(nx, ny)
        self._end_turn()
    def _player_attack(self):
        """Attack nearest adjacent enemy."""
        if not self.player or not self.player.is_alive:
            return
        adj = self._adjacent_enemies()
        if not adj:
            self._log("No adjacent enemy to attack.")
            self._render()
            return
        target = min(adj, key=lambda e: e.hp)
        self._attack_enemy(target)
        self._end_turn()
    def _attack_enemy(self, enemy: Enemy):
        """Perform a basic attack on an enemy."""
        p = self.player
        if not p:
            return
        atk = p.attack
        # Saint's Ember relic — first attack each room +3
        if p.has_relic("saints_ember") and p.first_attack_this_room:
            atk += 3
            self._log("Saint's Ember flares! +3 damage")
        p.first_attack_this_room = False
        # Ashen Blade passive — bleeding enemies take +1
        if p.player_class == PlayerClass.ASHEN_BLADE and enemy.has_status(StatusType.BLEED):
            atk += 1
        # Chain Psalm relic — stunned enemies take +2
        if p.has_relic("chain_psalm") and enemy.has_status(StatusType.STUN):
            atk += 2
        dmg, crit = self._calc_damage(atk, enemy.defense)
        enemy.hp -= dmg
        self.run_stats.damage_dealt += dmg
        crit_txt = " CRITICAL!" if crit else ""
        self._log(f"You hit {enemy.name} for {dmg} damage.{crit_txt}")
        self._float_text(enemy.x, enemy.y, f"-{dmg}", C["crit"] if crit else C["red"])
        if enemy.hp <= 0:
            self._enemy_defeated(enemy)
    def _use_ability(self):
        """Use class ability."""
        p = self.player
        if not p or not p.is_alive:
            return
        stats = CLASS_STATS[p.player_class]
        cost = stats["ability_cost"]
        # Ember Gauntlet relic — ability costs 1 less
        if p.has_relic("ember_gauntlet"):
            cost = max(1, cost - 1)
        if p.focus < cost:
            self._log(f"Not enough focus for {stats['ability']}! ({p.focus}/{cost})")
            self._render()
            return
        if p.player_class == PlayerClass.WARDEN:
            self._ability_shield_bash(cost)
        elif p.player_class == PlayerClass.ASHEN_BLADE:
            self._ability_cinder_arc(cost)
        elif p.player_class == PlayerClass.DREAMSEER:
            self._ability_dream_lance(cost)
    def _ability_shield_bash(self, cost: int):
        p = self.player
        adj = self._adjacent_enemies()
        if not adj:
            self._log("Shield Bash: No adjacent enemy.")
            self._render()
            return
        target = min(adj, key=lambda e: e.hp)
        p.focus -= cost
        atk = int(p.attack * 1.3) + 4
        if p.has_relic("chain_psalm") and target.has_status(StatusType.STUN):
            atk += 2
        dmg, crit = self._calc_damage(atk, target.defense)
        target.hp -= dmg
        self.run_stats.damage_dealt += dmg
        # Stun
        target.add_status(StatusEffect(StatusType.STUN, 2))
        self._log(f"Shield Bash hits {target.name} for {dmg}! Stunned!")
        self._float_text(target.x, target.y, f"-{dmg}⚡", C["gold"])
        # Dreamseer passive wouldn't apply, but Warden passive: no focus gain
        # Psychic Resonance is Dreamseer only — no action here
        if target.hp <= 0:
            self._enemy_defeated(target)
        self._end_turn()
    def _ability_cinder_arc(self, cost: int):
        p = self.player
        adj = self._adjacent_enemies()
        if not adj:
            self._log("Cinder Arc: No adjacent enemies.")
            self._render()
            return
        p.focus -= cost
        for target in adj:
            atk = int(p.attack * 0.8)
            if p.player_class == PlayerClass.ASHEN_BLADE and target.has_status(StatusType.BLEED):
                atk += 1
            if p.has_relic("chain_psalm") and target.has_status(StatusType.STUN):
                atk += 2
            dmg, crit = self._calc_damage(atk, target.defense)
            target.hp -= dmg
            self.run_stats.damage_dealt += dmg
            target.add_status(StatusEffect(StatusType.BLEED, 3, 3))
            self._log(f"Cinder Arc hits {target.name} for {dmg}! Bleeding!")
            self._float_text(target.x, target.y, f"-{dmg}♦", C["bleed"])
        # Check deaths
        for target in list(adj):
            if target.hp <= 0:
                self._enemy_defeated(target)
        self._end_turn()
    def _ability_dream_lance(self, cost: int):
        p = self.player
        # Find nearest enemy within range 4
        targets = [e for e in self.enemies if e.is_alive
                   and self._dist(p.x, p.y, e.x, e.y) <= 4]
        if not targets:
            self._log("Dream Lance: No enemy in range (4 tiles).")
            self._render()
            return
        target = min(targets, key=lambda e: self._dist(p.x, p.y, e.x, e.y))
        p.focus -= cost
        atk = int(p.attack * 1.2) + 3
        if p.has_relic("chain_psalm") and target.has_status(StatusType.STUN):
            atk += 2
        dmg, crit = self._calc_damage(atk, target.defense)
        target.hp -= dmg
        self.run_stats.damage_dealt += dmg
        target.add_status(StatusEffect(StatusType.STUN, 2))
        self._log(f"Dream Lance strikes {target.name} for {dmg}! Stunned!")
        self._float_text(target.x, target.y, f"-{dmg}⚡", C["blue"])
        # Dreamseer passive — regain 1 focus on stun
        if p.player_class == PlayerClass.DREAMSEER:
            p.focus = min(p.max_focus, p.focus + 1)
            self._log("Psychic Resonance: +1 focus.")
        if target.hp <= 0:
            self._enemy_defeated(target)
        self._end_turn()
    def _use_vial(self):
        p = self.player
        if not p or not p.is_alive:
            return
        if self.area_id == "tavern":
            self._log("You do not need a Blood Vial inside the Hollow Hearth. Rest at the bed instead.")
            self._render()
            return
        if p.blood_vials <= 0:
            self._log("No Blood Vials remaining.")
            self._render()
            return
        p.blood_vials -= 1
        heal = 20
        old_hp = p.hp
        p.hp = min(p.max_hp, p.hp + heal)
        actual = p.hp - old_hp
        self.run_stats.potions_used += 1
        self._log(f"Used Blood Vial. Restored {actual} HP.")
        self._float_text(p.x, p.y, f"+{actual}", C["heal"])
        # Bloodglass Ring — also restore 2 focus
        if p.has_relic("bloodglass_ring"):
            p.focus = min(p.max_focus, p.focus + 2)
            self._log("Bloodglass Ring: +2 focus.")
        # Pale Wing Fragment — +2 defense for 1 turn
        if p.has_relic("pale_wing"):
            p.defense += 2
            self._log("Pale Wing Fragment: +2 defense this turn.")
            # We'll remove this at end of turn
        self._end_turn()
        # Remove pale wing defense bonus after turn
        if p.has_relic("pale_wing"):
            p.defense = max(0, p.defense - 2)
    def _recover_focus(self):
        p = self.player
        if not p or not p.is_alive:
            return
        old = p.focus
        p.focus = min(p.max_focus, p.focus + 3)
        gained = p.focus - old
        if gained > 0:
            self._log(f"Resting... Recovered {gained} focus.")
            self._float_text(p.x, p.y, f"+{gained} foc", C["focus_bar"])
        else:
            self._log("Focus is already full.")
            self._render()
            return
        self._end_turn()
    # ═══════════════════════════════════════════════════════════
    # COMBAT HELPERS
    # ═══════════════════════════════════════════════════════════
    def _calc_damage(self, atk: int, defense: int) -> Tuple[int, bool]:
        """Calculate damage with variation and crit. Returns (damage, is_crit)."""
        base = atk - defense
        variation = random.randint(-2, 2)
        dmg = base + variation
        crit = False
        crit_chance = 0.10
        # Rusted Halo — +15% crit below 40% HP
        if self.player and self.player.has_relic("rusted_halo"):
            if self.player.hp < self.player.max_hp * 0.4:
                crit_chance += 0.15
        if random.random() < crit_chance:
            dmg = int(dmg * 1.5)
            crit = True
        return max(1, dmg), crit
    def _enemy_defeated(self, enemy: Enemy):
        shards = enemy.shard_reward
        # Room modifier shard bonus
        if self.room_modifier and self.room_modifier.shard_bonus > 0:
            shards += self.room_modifier.shard_bonus
        if self.player:
            self.player.relic_shards += shards
        self.run_stats.shards_collected += shards
        self.run_stats.enemies_defeated += 1
        self._log(f"{enemy.name} defeated! +{shards} shards.")
        # Remove from list
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        # Check victory condition
        if enemy.is_boss and enemy.enemy_type == "vaelrith":
            self.state = GameState.VICTORY
            self._log("Vaelrith has fallen!")
            self._stop_exit_pulse()
            self._render()
    def _adjacent_enemies(self) -> List[Enemy]:
        if not self.player:
            return []
        px, py = self.player.x, self.player.y
        return [e for e in self.enemies if e.is_alive
                and abs(e.x - px) + abs(e.y - py) == 1]
    def _enemy_at(self, x: int, y: int) -> Optional[Enemy]:
        for e in self.enemies:
            if e.is_alive and e.x == x and e.y == y:
                return e
        return None
    def _get_boss(self) -> Optional[Enemy]:
        for e in self.enemies:
            if e.is_boss and e.is_alive:
                return e
        return None
    # ═══════════════════════════════════════════════════════════
    # TURN PROCESSING
    # ═══════════════════════════════════════════════════════════
    def _end_turn(self):
        if not self.player or not self.player.is_alive:
            return
        self.turn_count += 1
        self.run_stats.turns += 1
        # Process player status effects
        self._process_player_status()
        if not self.player.is_alive:
            self._player_died()
            return
        # Enemy turns
        self._enemy_turns()
        if not self.player or not self.player.is_alive:
            self._player_died()
            return
        # Process enemy status effects
        self._process_enemy_status()
        self._render()
    def _process_player_status(self):
        p = self.player
        if not p:
            return
        expired = []
        for eff in p.status_effects:
            if eff.type == StatusType.BLEED and eff.damage > 0:
                p.hp -= eff.damage
                self.run_stats.damage_taken += eff.damage
                self._log(f"Bleed: You take {eff.damage} damage.")
                self._float_text(p.x, p.y, f"-{eff.damage}", C["bleed"])
            if eff.tick():
                expired.append(eff.type)
        for t in expired:
            p.remove_status(t)
            self._log(f"{t.value} wore off.")
    def _process_enemy_status(self):
        for enemy in list(self.enemies):
            if not enemy.is_alive:
                continue
            expired = []
            for eff in enemy.status_effects:
                if eff.type == StatusType.BLEED and eff.damage > 0:
                    enemy.hp -= eff.damage
                    self._log(f"{enemy.name} bleeds for {eff.damage}.")
                    self._float_text(enemy.x, enemy.y, f"-{eff.damage}", C["bleed"])
                if eff.tick():
                    expired.append(eff.type)
            for t in expired:
                enemy.remove_status(t)
            if enemy.hp <= 0:
                self._enemy_defeated(enemy)
    def _player_died(self):
        self.state = GameState.DEFEAT
        self._log("You have fallen.")
        self._stop_exit_pulse()
        self._render()
    # ═══════════════════════════════════════════════════════════
    # ENEMY AI
    # ═══════════════════════════════════════════════════════════
    def _enemy_turns(self):
        if not self.player:
            return
        # Ashen Silence modifier — enemies skip every other turn
        if self.room_modifier and self.room_modifier.enemy_move_interval == 2:
            if self.turn_count % 2 == 0:
                return
        for enemy in list(self.enemies):
            if not enemy.is_alive or not self.player.is_alive:
                continue
            self._single_enemy_turn(enemy)
    def _single_enemy_turn(self, enemy: Enemy):
        # Stunned — skip
        if enemy.has_status(StatusType.STUN):
            self._log(f"{enemy.name} is stunned!")
            return
        p = self.player
        if not p:
            return
        dist = abs(enemy.x - p.x) + abs(enemy.y - p.y)
        # Boss AI
        if enemy.is_boss and enemy.enemy_type == "vaelrith":
            self._vaelrith_turn(enemy)
            return
        # Type-specific AI
        if enemy.enemy_type == "overseer":
            self._overseer_turn(enemy, dist)
        elif enemy.enemy_type == "false_pilgrim":
            self._false_pilgrim_turn(enemy, dist)
        elif enemy.enemy_type == "sealbound_knight":
            self._sealbound_knight_turn(enemy, dist)
        else:
            self._default_enemy_turn(enemy, dist)
    def _default_enemy_turn(self, enemy: Enemy, dist: int):
        p = self.player
        if dist == 1:
            self._enemy_attacks_player(enemy)
        else:
            self._move_toward_player(enemy)
    def _false_pilgrim_turn(self, enemy: Enemy, dist: int):
        """False Pilgrims try to flank the player."""
        p = self.player
        if dist == 1:
            self._enemy_attacks_player(enemy)
            # 25% chance to apply bleed
            if random.random() < 0.25 and p.is_alive:
                p.add_status(StatusEffect(StatusType.BLEED, 3, 2))
                self._log(f"{enemy.name} inflicts Bleed!")
        else:
            # Try to move to opposite side of player
            if not self._try_flank(enemy):
                self._move_toward_player(enemy)
    def _overseer_turn(self, enemy: Enemy, dist: int):
        """Overseers keep distance and drain focus."""
        p = self.player
        if dist == 1:
            self._enemy_attacks_player(enemy)
            # Drain 2 focus
            if p.is_alive:
                drain = min(2, p.focus)
                if drain > 0:
                    p.focus -= drain
                    self._log(f"{enemy.name} drains {drain} focus!")
        elif dist == 2:
            # Comfortable distance — stay put or attack if possible
            pass  # Hold position
        else:
            # Move closer but try to keep distance of 2
            self._move_toward_player(enemy, min_dist=2)
    def _sealbound_knight_turn(self, enemy: Enemy, dist: int):
        """Sealbound Knights guard the exit."""
        p = self.player
        if dist == 1:
            self._enemy_attacks_player(enemy)
        else:
            # Try to position near exit
            exit_pos = self._find_exit()
            if exit_pos and self._dist(enemy.x, enemy.y, exit_pos[0], exit_pos[1]) > 2:
                self._move_toward(enemy, exit_pos[0], exit_pos[1])
            else:
                self._move_toward_player(enemy)
    def _vaelrith_turn(self, enemy: Enemy):
        """Vaelrith boss AI with phases."""
        p = self.player
        if not p:
            return
        # Update phase
        hp_pct = enemy.hp / enemy.max_hp
        if hp_pct <= 0.25:
            if enemy.boss_phase != 3:
                enemy.boss_phase = 3
                enemy.attack = ENEMY_DEFS["vaelrith"]["attack"] + 5
                if self.difficulty == Difficulty.MARTYR:
                    enemy.attack += 2
                elif self.difficulty == Difficulty.PILGRIM:
                    enemy.attack -= 2
                self._log("Vaelrith enters Phase 3! All-out fury!")
        elif hp_pct <= 0.5:
            if enemy.boss_phase != 2:
                enemy.boss_phase = 2
                enemy.attack = ENEMY_DEFS["vaelrith"]["attack"] + 3
                if self.difficulty == Difficulty.MARTYR:
                    enemy.attack += 2
                elif self.difficulty == Difficulty.PILGRIM:
                    enemy.attack -= 2
                self._log("Vaelrith enters Phase 2! The seal pulses!")
        dist = abs(enemy.x - p.x) + abs(enemy.y - p.y)
        # Phase 2 — may summon or Blood Pulse
        if enemy.boss_phase >= 2 and not enemy.has_summoned:
            if random.random() < 0.4:
                self._vaelrith_summon(enemy)
                enemy.has_summoned = True
                return
        if enemy.boss_phase >= 2 and random.random() < 0.3:
            # Blood Pulse — apply bleed
            p.add_status(StatusEffect(StatusType.BLEED, 3, 2))
            self._log("Vaelrith unleashes Blood Pulse! You are bleeding!")
            self._float_text(p.x, p.y, "Blood Pulse!", C["boss_bar"])
        # Attack or move
        if dist == 1:
            self._enemy_attacks_player(enemy)
        else:
            self._move_toward_player(enemy)
    def _vaelrith_summon(self, boss: Enemy):
        """Vaelrith summons two False Pilgrims."""
        spawned = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]:
            sx, sy = boss.x + dx, boss.y + dy
            if not self._in_bounds(sx, sy):
                continue
            if self.grid[sy][sx] == "#":
                continue
            if self._enemy_at(sx, sy):
                continue
            if self.player and self.player.x == sx and self.player.y == sy:
                continue
            fp = create_enemy("false_pilgrim", self.difficulty, sx, sy)
            self.enemies.append(fp)
            spawned += 1
            if spawned >= 2:
                break
        if spawned > 0:
            self._log(f"Vaelrith summons {spawned} False Pilgrim{'s' if spawned > 1 else ''}!")
    def _enemy_attacks_player(self, enemy: Enemy):
        p = self.player
        if not p:
            return
        dmg, crit = self._calc_enemy_damage(enemy.attack, p.defense)
        # Warden passive — Iron Resolve: first hit each room reduced by 50%
        if p.player_class == PlayerClass.WARDEN and p.first_hit_this_room:
            dmg = max(1, dmg // 2)
            p.first_hit_this_room = False
            self._log("Iron Resolve absorbs the blow!")
        p.hp -= dmg
        self.run_stats.damage_taken += dmg
        crit_txt = " Critical!" if crit else ""
        self._log(f"{enemy.name} hits you for {dmg}.{crit_txt}")
        self._float_text(p.x, p.y, f"-{dmg}", C["red"])
        # Thorn-Crowned Charm — reflect 1 damage
        if p.has_relic("thorn_charm") and enemy.is_alive:
            enemy.hp -= 1
            self._log(f"Thorn-Crowned Charm reflects 1 damage!")
            if enemy.hp <= 0:
                self._enemy_defeated(enemy)
    def _calc_enemy_damage(self, atk: int, defense: int) -> Tuple[int, bool]:
        base = atk - defense
        variation = random.randint(-1, 2)
        dmg = base + variation
        crit = random.random() < 0.08
        if crit:
            dmg = int(dmg * 1.4)
        return max(1, dmg), crit
    # ─── Movement Helpers ────────────────────────────────────
    def _move_toward_player(self, enemy: Enemy, min_dist: int = 0):
        if not self.player:
            return
        self._move_toward(enemy, self.player.x, self.player.y, min_dist)
    def _move_toward(self, enemy: Enemy, tx: int, ty: int, min_dist: int = 0):
        dx = 0
        dy = 0
        if enemy.x < tx:
            dx = 1
        elif enemy.x > tx:
            dx = -1
        if enemy.y < ty:
            dy = 1
        elif enemy.y > ty:
            dy = -1
        # Prefer the axis with greater distance
        adx = abs(tx - enemy.x)
        ady = abs(ty - enemy.y)
        moves = []
        if adx >= ady:
            if dx != 0:
                moves.append((dx, 0))
            if dy != 0:
                moves.append((0, dy))
        else:
            if dy != 0:
                moves.append((0, dy))
            if dx != 0:
                moves.append((dx, 0))
        for mdx, mdy in moves:
            nx, ny = enemy.x + mdx, enemy.y + mdy
            if not self._in_bounds(nx, ny):
                continue
            if self.grid[ny][nx] == "#":
                continue
            if self._enemy_at(nx, ny):
                continue
            if self.player and self.player.x == nx and self.player.y == ny:
                continue
            # Check min_dist
            if min_dist > 0:
                new_dist = abs(nx - tx) + abs(ny - ty)
                if new_dist < min_dist:
                    continue
            enemy.x = nx
            enemy.y = ny
            return
    def _try_flank(self, enemy: Enemy) -> bool:
        """Try to move to the opposite side of the player."""
        p = self.player
        if not p:
            return False
        # Target: opposite side
        dx = p.x - enemy.x
        dy = p.y - enemy.y
        fx = p.x + (1 if dx > 0 else -1 if dx < 0 else 0)
        fy = p.y + (1 if dy > 0 else -1 if dy < 0 else 0)
        if self._in_bounds(fx, fy) and self.grid[fy][fx] != "#" and not self._enemy_at(fx, fy):
            if not (self.player and self.player.x == fx and self.player.y == fy):
                # Move one step toward flank position
                self._move_toward(enemy, fx, fy)
                return True
        return False
    def _find_exit(self) -> Optional[Tuple[int, int]]:
        for gy in range(GRID_H):
            for gx in range(GRID_W):
                if gy < len(self.grid) and gx < len(self.grid[gy]):
                    if self.grid[gy][gx] == ">":
                        return (gx, gy)
        return None
    # ═══════════════════════════════════════════════════════════
    # TILE INTERACTIONS
    # ═══════════════════════════════════════════════════════════
    def _on_tile_enter(self, x: int, y: int):
        tile = self.grid[y][x]
        if self.area_id == "tavern" and tile in ("e", "l", "i", "b"):
            names = {"e": "Expedition Board", "l": "Lore Book", "i": "Hollow Quill Notice", "b": "Tavern Bed"}
            self._log(f"{names[tile]}: press F to interact.")
        elif tile == "~":
            self._trap_trigger(x, y)
        elif tile == "!":
            self._reliquary_pickup(x, y)
        elif tile == "†":
            self._shrine_interact(x, y)
        elif tile == ">":
            self._exit_interact()

    def _interact_tavern_tile(self, tile: str):
        actions = {
            "e": "expedition",
            "l": "lore",
            "i": "inheritance",
        }
        action = actions.get(tile)
        if action:
            self._activate_menu_action(action)
        elif tile == "b":
            self._rest_at_tavern_bed()

    def _interact_tavern(self):
        if self.area_id != "tavern" or not self.player:
            self._log("There is nothing here to interact with.")
            self._render()
            return
        for npc in TAVERN_NPCS:
            if max(abs(self.player.x - npc.position[0]), abs(self.player.y - npc.position[1])) <= 1:
                self.event_log.clear()
                self._log(f"{npc.name}, {npc.title}:")
                for line in npc.dialogue:
                    self._log(f"  {line}")
                self._render()
                return
        positions = sorted(
            (
                (self.player.x + dx, self.player.y + dy)
                for dy in range(-1, 2)
                for dx in range(-1, 2)
            ),
            key=lambda point: abs(point[0] - self.player.x) + abs(point[1] - self.player.y),
        )
        for x, y in positions:
            if self._in_bounds(x, y) and self.grid[y][x] in ("e", "l", "i", "b"):
                self._interact_tavern_tile(self.grid[y][x])
                return
        self._log("The hearth crackles. The tavern waits.")
        self._render()

    def _rest_at_tavern_bed(self):
        if not self.player:
            return
        self.player.hp = self.player.max_hp
        self.player.focus = self.player.max_focus
        self.player.blood_vials = 2
        self._log("You rest beneath the low firelight. HP, focus, and Blood Vials are restored.")
        self._render()
    def _trap_trigger(self, x: int, y: int):
        dmg = 3
        if self.room_modifier:
            dmg += self.room_modifier.trap_damage_bonus
        if self.player:
            self.player.hp -= dmg
            self.run_stats.damage_taken += dmg
            self._log(f"Blood trap! You take {dmg} damage.")
            self._float_text(x, y, f"-{dmg}", C["trap_glow"])
            # Trap remains
    def _reliquary_pickup(self, x: int, y: int):
        p = self.player
        if not p:
            return
        p.blood_vials += 1
        shards = random.randint(8, 14)
        if self.room_modifier:
            shards += self.room_modifier.shard_bonus
        p.relic_shards += shards
        self.run_stats.shards_collected += shards
        self._log(f"Reliquary! +1 Blood Vial, +{shards} shards.")
        self._float_text(x, y, f"+{shards}◆", C["gold"])
        # Chance to find a relic (40%)
        if self.relic_pool and random.random() < 0.40:
            self._grant_relic()
        # Remove reliquary
        self.grid[y][x] = "."
    def _shrine_interact(self, x: int, y: int):
        self.state = GameState.SHRINE_PROMPT
        self.run_stats.shrines_visited += 1
        self._render()
    def _shrine_choose(self, choice: int):
        p = self.player
        if not p:
            return
        if choice == 1:
            heal = 16
            # Hollow Saint Medallion — +4 extra HP
            if p.has_relic("hollow_medallion"):
                heal += 4
            # Saintless Dark modifier
            if self.room_modifier and self.room_modifier.shrine_hp_bonus != 0:
                heal = max(1, heal + self.room_modifier.shrine_hp_bonus)
            old = p.hp
            p.hp = min(p.max_hp, p.hp + heal)
            actual = p.hp - old
            self._log(f"Shrine: Restored {actual} HP.")
            self._float_text(p.x, p.y, f"+{actual} HP", C["heal"])
        elif choice == 2:
            p.focus = min(p.max_focus, p.focus + 6)
            p.blood_vials += 1
            self._log("Shrine: +6 focus, +1 Blood Vial.")
            self._float_text(p.x, p.y, "+6 foc +1♥", C["focus_bar"])
        # Clear shrine tile
        self.grid[p.y][p.x] = "."
        self.state = GameState.PLAYING
        self._end_turn()
    def _exit_interact(self):
        if not self._is_room_clear():
            self._log("The exit is sealed. Defeat all enemies first.")
            self._render()
            return
        content = AREA_CONTENT.get(self.area_id, AREA_CONTENT["blood_wing"])
        if self.area_id in ("tutorial_estate", "foundries_and_forges"):
            self._advance_room()
            return
        if self.room_index >= len(content["rooms"]) - 1:
            # Last room — shouldn't have exit
            return
        # Show shop prompt
        self.state = GameState.SHOP_PROMPT
        self._render()
    def _shop_choose(self, choice: int):
        p = self.player
        if not p:
            return
        if choice == 1:
            # Buy Blood Vial for 30 shards
            if p.relic_shards >= 30:
                p.relic_shards -= 30
                p.blood_vials += 1
                self._log("Merchant: Bought Blood Vial for 30 shards.")
            else:
                self._log("Merchant: Not enough shards. (Need 30)")
                self._render()
                return
        elif choice == 2 and self.relic_pool:
            # Buy relic for 40 shards
            if p.relic_shards >= 40:
                p.relic_shards -= 40
                self._grant_relic()
                self._log("Merchant: Purchased a relic.")
            else:
                self._log("Merchant: Not enough shards. (Need 40)")
                self._render()
                return
        # Advance to next room
        self.state = GameState.PLAYING
        self._advance_room()
    def _advance_room(self):
        next_idx = self.room_index + 1
        content = AREA_CONTENT.get(self.area_id, AREA_CONTENT["blood_wing"])
        if next_idx < len(content["rooms"]):
            self._load_room(next_idx)
            self._render()
        else:
            if self.area_id == "blood_wing":
                self.state = GameState.VICTORY
                self._render()
            elif self.area_id == "tutorial_estate":
                self._return_to_tavern("You return to the Hollow Hearth with ash on your boots and the road ahead marked in blood.")
            else:
                self._return_to_tavern("The last furnace coughs once, then falls silent. Somewhere below, water answers.")
    # ═══════════════════════════════════════════════════════════
    # RELIC SYSTEM
    # ═══════════════════════════════════════════════════════════
    def _grant_relic(self):
        if not self.relic_pool or not self.player:
            return
        relic = self.relic_pool.pop(0)
        self.player.relics.append(relic.id)
        self.run_stats.relics_found += 1
        self._log(f"Found relic: {relic.icon} {relic.name}!")
        self._log(f"  → {relic.description}")
    def _relic_by_id(self, rid: str) -> Optional[Relic]:
        for r in ALL_RELICS:
            if r.id == rid:
                return r
        return None
    # ═══════════════════════════════════════════════════════════
    # SAVE / LOAD
    # ═══════════════════════════════════════════════════════════
    def _save_game(self):
        if not self.player:
            return
        data = {
            "player": self.player.to_dict(),
            "area_id": self.area_id,
            "area_status": self.area_status,
            "cleared_areas": sorted(self.cleared_areas),
            "room_index": self.room_index,
            "difficulty": self.difficulty.value,
            "grid": ["".join(row) for row in self.grid],
            "enemies": [e.to_dict() for e in self.enemies if e.is_alive],
            "run_stats": self.run_stats.to_dict(),
            "turn_count": self.turn_count,
            "relic_pool": [r.id for r in self.relic_pool],
            "event_log": self.event_log[-50:],
        }
        try:
            with open(self.save_path, "w") as f:
                json.dump(data, f, indent=2)
            self._log("Game saved.")
        except Exception as e:
            self._log(f"Save failed: {e}")
        self._render()
    def _load_game(self):
        if not os.path.exists(self.save_path):
            self._log("No save file found.")
            self._render()
            return
        try:
            with open(self.save_path, "r") as f:
                data = json.load(f)
            self.player = Player.from_dict(data["player"])
            area_id = data.get("area_id", "blood_wing")
            if area_id not in AREA_CONTENT:
                area_id = "tavern"
            self.area_id = area_id
            self.area_status = data.get("area_status", AREA_REGISTRY[area_id]["status"])
            self.cleared_areas = set(data.get("cleared_areas", []))
            self.room_index = int(data.get("room_index", 0))
            self.difficulty = Difficulty(data["difficulty"])
            self.grid = [list(row) for row in data["grid"]]
            self.enemies = [Enemy.from_dict(e) for e in data["enemies"]]
            self.run_stats = RunStats.from_dict(data["run_stats"])
            self.turn_count = data.get("turn_count", 0)
            # Restore relic pool
            pool_ids = data.get("relic_pool", [])
            self.relic_pool = [r for r in ALL_RELICS if r.id in pool_ids]
            self.event_log = data.get("event_log", [])
            self.state = GameState.PLAYING
            self._log("Game loaded.")
            self._start_exit_pulse()
            self._render()
        except Exception as e:
            self._log(f"Load failed: {e}")
            self._render()
    # ═══════════════════════════════════════════════════════════
    # ANIMATIONS & EFFECTS
    # ═══════════════════════════════════════════════════════════
    def _float_text(self, gx: int, gy: int, text: str, colour: str):
        """Queue floating text and a quick tile flash.

        Most gameplay actions call _render() immediately after resolving, which
        used to delete the text before it could animate.  Queueing the effect and
        flushing it after the next render keeps the feedback visible.
        """
        if self.headless:
            return
        self._pending_float_texts.append((gx, gy, text, colour))
        self._pending_tile_flashes.append((gx, gy, colour))

    def _flush_canvas_effects(self):
        if self.headless:
            return
        # Draw tile flashes below floating numbers, then let them fade quickly.
        flashes = self._pending_tile_flashes[-12:]
        self._pending_tile_flashes.clear()
        for gx, gy, colour in flashes:
            x1 = gx * TILE + 3
            y1 = gy * TILE + 3
            item = self.canvas.create_rectangle(
                x1, y1, x1 + TILE - 6, y1 + TILE - 6,
                fill=colour, outline=colour, stipple="gray50", width=2,
            )
            job = self.root.after(140, self._safe_canvas_delete, item)
            self._anim_jobs.append(job)

        floats = self._pending_float_texts[-16:]
        self._pending_float_texts.clear()
        for gx, gy, text, colour in floats:
            px = gx * TILE + TILE // 2 + random.randint(-5, 5)
            py = gy * TILE + TILE // 4 + random.randint(-3, 3)
            item = self.canvas.create_text(
                px, py, text=text, fill=colour,
                font=("Consolas", 11, "bold"),
            )
            self._animate_float(item, 0)

    def _safe_canvas_delete(self, item):
        try:
            self.canvas.delete(item)
        except Exception:
            pass

    def _animate_float(self, item, step):
        if self.headless:
            return
        if step >= 14:
            self._safe_canvas_delete(item)
            return
        try:
            self.canvas.move(item, 0, -2)
        except Exception:
            return
        job = self.root.after(55, self._animate_float, item, step + 1)
        self._anim_jobs.append(job)

    def _start_exit_pulse(self):
        if self.headless:
            return
        self._stop_exit_pulse()
        self._pulse_exit()
    def _pulse_exit(self):
        self.exit_pulse_on = not self.exit_pulse_on
        if self.state == GameState.PLAYING:
            self._render()
        self._pulse_job = self.root.after(800, self._pulse_exit)
    def _stop_exit_pulse(self):
        if self._pulse_job and not self.headless:
            try:
                self.root.after_cancel(self._pulse_job)
            except Exception:
                pass
            self._pulse_job = None
        for job in self._anim_jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self._anim_jobs.clear()
    # ═══════════════════════════════════════════════════════════
    # FULLSCREEN
    # ═══════════════════════════════════════════════════════════
    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
    def _leave_fullscreen(self):
        if self.state == GameState.CLASS_SELECT:
            self.state = GameState.EXPEDITION_BOARD
            self._render()
        elif self.state == GameState.DIFFICULTY_SELECT:
            self.state = GameState.CLASS_SELECT
            self._render()
        elif self.state == GameState.INHERITANCE_BOARD:
            self.state = GameState.PLAYING
            self._render()
        elif self.state in (
            GameState.EXPEDITION_BOARD,
            GameState.TUTORIAL,
            GameState.LORE_BOOK,
            GameState.WORLD_PROGRESSION,
            GameState.SETTINGS,
        ):
            self.state = GameState.TAVERN
            self._render()
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
    # ═══════════════════════════════════════════════════════════
    # UTILITY
    # ═══════════════════════════════════════════════════════════
    def _is_room_clear(self) -> bool:
        return all(not e.is_alive for e in self.enemies)
    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < GRID_W and 0 <= y < GRID_H
    @staticmethod
    def _dist(x1, y1, x2, y2) -> int:
        return abs(x1 - x2) + abs(y1 - y2)
    def _log(self, msg: str):
        self.event_log.append(msg)
    # ═══════════════════════════════════════════════════════════
    # PUBLIC API (for testing)
    # ═══════════════════════════════════════════════════════════
    def setup_game(self, player_class: PlayerClass, difficulty: Difficulty):
        """Programmatically start a game (for tests)."""
        self.selected_class = player_class
        self.difficulty = difficulty
        self.player = create_player(player_class, difficulty)
        self.run_stats = RunStats()
        self.relic_pool = list(ALL_RELICS)
        self.room_index = 0
        self.turn_count = 0
        self.event_log = []
        self._load_room(0)
        self.state = GameState.PLAYING
    def get_grid_char(self, x: int, y: int) -> str:
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
            return self.grid[y][x]
        return "#"
