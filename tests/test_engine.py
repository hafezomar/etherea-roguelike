from __future__ import annotations

import os
import random
import tempfile
import unittest
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from game.engine import GameEngine
from game.map_data import ROOMS
from game.areas import AREA_REGISTRY, campaign_areas
from game.audio import AudioManager
from game.lore import LORE_PAGES, TAVERN_MENU, TAVERN_NAME
from game.models import Difficulty, GameState, PlayerClass, StatusType, create_enemy, create_player


class EthereaGeneratedAttemptTests(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(7)

    def new_game(self, class_index: int = 0, diff_index: int = 1) -> GameEngine:
        game = GameEngine(headless=True)
        game.selected_class_index = class_index
        game.selected_diff_index = diff_index
        game._start_game()
        return game

    def test_rooms_are_rectangular_18_by_12(self) -> None:
        self.assertEqual(len(ROOMS), 4)
        for room in ROOMS:
            self.assertEqual(len(room), 12)
            self.assertTrue(all(len(row) == 18 for row in room))

    def test_campaign_registry_marks_blood_wing_as_late_game_prototype(self) -> None:
        blood_wing = AREA_REGISTRY["blood_wing"]
        self.assertEqual(blood_wing["status"], "playable_prototype")
        self.assertEqual(blood_wing["order"], 14)
        self.assertEqual(AREA_REGISTRY["tutorial_estate"]["order"], 1)
        self.assertEqual(AREA_REGISTRY["deeper_well"]["order"], 3)
        orders = [area["order"] for _, area in campaign_areas()]
        self.assertEqual(orders, list(range(1, 17)))

    def test_tavern_and_lore_data_exist(self) -> None:
        game = GameEngine(headless=True)
        self.assertEqual(game.state, GameState.TAVERN)
        self.assertEqual(TAVERN_NAME, "The Hollow Hearth Tavern")
        self.assertIn("Choose Expedition", TAVERN_MENU)
        self.assertGreaterEqual(len(LORE_PAGES), 4)
        self.assertTrue(any(page["title"] == "TEMPLE OF THE SLEEPERS" for page in LORE_PAGES))

    def test_future_early_game_enemies_scale_with_difficulty(self) -> None:
        zombie = create_enemy("zombie", Difficulty.WARDEN)
        skeleton = create_enemy("skeleton", Difficulty.WARDEN)
        martyr_zombie = create_enemy("zombie", Difficulty.MARTYR)
        self.assertGreater(zombie.hp, skeleton.hp)
        self.assertGreater(skeleton.attack, zombie.attack)
        self.assertGreater(martyr_zombie.hp, zombie.hp)

    def test_optional_audio_is_safe_without_assets(self) -> None:
        audio = AudioManager(os.path.join(tempfile.gettempdir(), "missing_etherea_audio"))
        self.assertFalse(audio.play("tavern"))
        self.assertFalse(audio.toggle())
        self.assertTrue(audio.toggle())

    def test_all_starting_classes_create_valid_players(self) -> None:
        classes = [PlayerClass.WARDEN, PlayerClass.ASHEN_BLADE, PlayerClass.DREAMSEER]
        for idx, player_class in enumerate(classes):
            game = self.new_game(idx)
            self.assertEqual(game.player.player_class, player_class)
            self.assertEqual(game.player.hp, game.player.max_hp)
            self.assertGreater(game.player.focus, 0)
            self.assertEqual(game.state.value, "playing")

    def test_adjacent_attack_damages_enemy(self) -> None:
        game = self.new_game(1)
        enemy = game.enemies[0]
        game.player.x = enemy.x - 1
        game.player.y = enemy.y
        before = enemy.hp
        game._player_attack()
        self.assertTrue(enemy.hp < before or enemy not in game.enemies)

    def test_save_and_load_preserve_progress(self) -> None:
        game = self.new_game(2)
        game.player.relic_shards = 44
        game.player.hp -= 5
        game.room_index = 1
        with tempfile.TemporaryDirectory() as tmp:
            save_path = os.path.join(tmp, "blood_wing_save.json")
            game.save_path = save_path
            game._save_game()
            loaded = GameEngine(headless=True)
            loaded.save_path = save_path
            loaded._load_game()
        self.assertEqual(loaded.player.player_class, PlayerClass.DREAMSEER)
        self.assertEqual(loaded.room_index, 1)
        self.assertEqual(loaded.player.relic_shards, 44)
        self.assertEqual(loaded.player.hp, game.player.hp)

    def test_legacy_save_defaults_to_blood_wing_area(self) -> None:
        game = self.new_game()
        with tempfile.TemporaryDirectory() as tmp:
            save_path = os.path.join(tmp, "blood_wing_save.json")
            game.save_path = save_path
            game._save_game()
            with open(save_path, "r") as handle:
                data = json.load(handle)
            data.pop("area_id", None)
            data.pop("area_status", None)
            with open(save_path, "w") as handle:
                json.dump(data, handle)
            loaded = GameEngine(headless=True)
            loaded.save_path = save_path
            loaded._load_game()
        self.assertEqual(loaded.area_id, "blood_wing")
        self.assertEqual(loaded.area_status, "playable_prototype")

    def test_final_room_contains_vaelrith(self) -> None:
        game = self.new_game()
        game._load_room(3)
        self.assertTrue(any(enemy.enemy_type == "vaelrith" for enemy in game.enemies))

    def test_shrine_focus_choice_grants_vial_and_clears_tile(self) -> None:
        game = self.new_game(2)
        game.player.x = 13
        game.player.y = 3
        game.grid[3][13] = "†"
        before = game.player.blood_vials
        game._shrine_choose(2)
        self.assertEqual(game.player.blood_vials, before + 1)
        self.assertEqual(game.grid[3][13], ".")

    def test_shop_trades_shards_for_vial_and_advances_room(self) -> None:
        game = self.new_game()
        game.enemies.clear()
        game.player.relic_shards = 30
        before = game.player.blood_vials
        game._shop_choose(1)
        self.assertEqual(game.player.blood_vials, before + 1)
        self.assertEqual(game.player.relic_shards, 0)
        self.assertEqual(game.room_index, 1)

    def test_vaelrith_summons_two_false_pilgrims_when_space_allows(self) -> None:
        game = self.new_game()
        game._load_room(3)
        boss = next(enemy for enemy in game.enemies if enemy.enemy_type == "vaelrith")
        game._vaelrith_summon(boss)
        pilgrims = [enemy for enemy in game.enemies if enemy.enemy_type == "false_pilgrim"]
        self.assertEqual(len(pilgrims), 2)

    def test_relic_and_difficulty_features_work(self) -> None:
        pilgrim = create_enemy("false_pilgrim", Difficulty.PILGRIM)
        martyr = create_enemy("false_pilgrim", Difficulty.MARTYR)
        self.assertLess(pilgrim.hp, martyr.hp)
        self.assertLess(pilgrim.attack, martyr.attack)
        game = self.new_game()
        game.player.relics.append("bloodglass_ring")
        game.player.focus = 0
        game.player.hp -= 20
        game.player.blood_vials = 1
        game._use_vial()
        self.assertGreaterEqual(game.player.focus, 2)


if __name__ == "__main__":
    unittest.main()
