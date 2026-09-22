"""
Comprehensive Unit Tests for Conway's Game of Life (GameOfLifeEngine)
"""

import unittest
from GameOfLife import GameOfLifeEngine


class TestGameOfLifeEngine(unittest.TestCase):

    def test_initialization(self):
        engine = GameOfLifeEngine(rows=10, cols=15, wrap=True)
        self.assertEqual(engine.rows, 10)
        self.assertEqual(engine.cols, 15)
        self.assertTrue(engine.wrap)
        self.assertEqual(engine.generation, 0)
        self.assertEqual(engine.get_alive_count(), 0)

    def test_clear_and_random_seed(self):
        engine = GameOfLifeEngine(rows=10, cols=10)
        engine.seed_random(density=0.5)
        self.assertGreater(engine.get_alive_count(), 0)

        engine.clear()
        self.assertEqual(engine.get_alive_count(), 0)
        self.assertEqual(engine.generation, 0)

    def test_still_life_block(self):
        # 2x2 Block should remain completely static forever
        engine = GameOfLifeEngine(rows=6, cols=6, wrap=False)
        engine.grid[2][2] = True
        engine.grid[2][3] = True
        engine.grid[3][2] = True
        engine.grid[3][3] = True
        self.assertEqual(engine.get_alive_count(), 4)

        for _ in range(5):
            gen, alive = engine.step()
            self.assertEqual(alive, 4)
            self.assertTrue(engine.grid[2][2])
            self.assertTrue(engine.grid[2][3])
            self.assertTrue(engine.grid[3][2])
            self.assertTrue(engine.grid[3][3])

    def test_blinker_oscillator_period_2(self):
        # Horizontal blinker of 3 cells centered at (2, 2)
        engine = GameOfLifeEngine(rows=5, cols=5, wrap=False)
        engine.grid[2][1] = True
        engine.grid[2][2] = True
        engine.grid[2][3] = True

        # Generation 1: Becomes vertical
        engine.step()
        self.assertEqual(engine.get_alive_count(), 3)
        self.assertTrue(engine.grid[1][2])
        self.assertTrue(engine.grid[2][2])
        self.assertTrue(engine.grid[3][2])
        self.assertFalse(engine.grid[2][1])
        self.assertFalse(engine.grid[2][3])

        # Generation 2: Back to horizontal
        engine.step()
        self.assertEqual(engine.get_alive_count(), 3)
        self.assertTrue(engine.grid[2][1])
        self.assertTrue(engine.grid[2][2])
        self.assertTrue(engine.grid[2][3])

    def test_toad_oscillator_period_2(self):
        # Toad oscillator loaded via preset
        engine = GameOfLifeEngine(rows=10, cols=10, wrap=False)
        self.assertTrue(engine.load_preset("toad"))
        initial_state = [row[:] for row in engine.grid]

        engine.step()  # Gen 1 (transformed)
        self.assertNotEqual(engine.grid, initial_state)

        engine.step()  # Gen 2 (restored to initial)
        self.assertEqual(engine.grid, initial_state)

    def test_beacon_oscillator_period_2(self):
        # Beacon oscillator loaded via preset
        engine = GameOfLifeEngine(rows=10, cols=10, wrap=False)
        self.assertTrue(engine.load_preset("beacon"))
        initial_state = [row[:] for row in engine.grid]

        engine.step()  # Gen 1
        self.assertNotEqual(engine.grid, initial_state)

        engine.step()  # Gen 2
        self.assertEqual(engine.grid, initial_state)

    def test_pulsar_oscillator_period_3(self):
        # Pulsar oscillator has period 3
        engine = GameOfLifeEngine(rows=25, cols=25, wrap=False)
        self.assertTrue(engine.load_preset("pulsar"))
        initial_state = [row[:] for row in engine.grid]

        engine.step()  # Gen 1
        self.assertNotEqual(engine.grid, initial_state)
        engine.step()  # Gen 2
        self.assertNotEqual(engine.grid, initial_state)
        engine.step()  # Gen 3 (restored)
        self.assertEqual(engine.grid, initial_state)

    def test_glider_translation_period_4(self):
        # A glider translates 1 cell down and 1 cell right every 4 generations
        engine = GameOfLifeEngine(rows=15, cols=15, wrap=False)
        # Load glider at top-left corner
        glider_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for r, c in glider_cells:
            engine.grid[r][c] = True

        for _ in range(4):
            engine.step()

        # After 4 steps, pattern shape must be identical but shifted by (+1, +1)
        for r, c in glider_cells:
            self.assertTrue(engine.grid[r + 1][c + 1], f"Glider cell missing at ({r+1}, {c+1})")
        self.assertEqual(engine.get_alive_count(), 5)

    def test_underpopulation_and_overpopulation(self):
        engine = GameOfLifeEngine(rows=5, cols=5, wrap=False)
        # Single isolated cell dies (underpopulation)
        engine.grid[2][2] = True
        engine.step()
        self.assertEqual(engine.get_alive_count(), 0)

        # 4 neighbors on center cell causes overpopulation death
        engine.clear()
        engine.grid[2][2] = True
        engine.grid[1][2] = True
        engine.grid[3][2] = True
        engine.grid[2][1] = True
        engine.grid[2][3] = True
        engine.step()
        self.assertFalse(engine.grid[2][2])

    def test_reproduction(self):
        # Dead cell with exactly 3 live neighbors becomes alive
        engine = GameOfLifeEngine(rows=5, cols=5, wrap=False)
        engine.grid[1][2] = True
        engine.grid[2][1] = True
        engine.grid[3][2] = True
        self.assertFalse(engine.grid[2][2])
        engine.step()
        self.assertTrue(engine.grid[2][2])

    def test_presets_loading(self):
        engine = GameOfLifeEngine(rows=40, cols=60)
        expected_presets = [
            "blinker", "toad", "beacon", "glider", "pulsar",
            "gosper_gun", "lwss", "pentadecathlon", "diehard", "acorn"
        ]
        for preset_name in expected_presets:
            success = engine.load_preset(preset_name)
            self.assertTrue(success, f"Failed to load preset '{preset_name}'")
            self.assertGreater(engine.get_alive_count(), 0)

        self.assertFalse(engine.load_preset("non_existent_preset"))

    def test_toroidal_wrapping(self):
        engine = GameOfLifeEngine(rows=5, cols=5, wrap=True)
        engine.grid[0][0] = True
        # Count neighbors of (0, 0) includes wrapped cells
        engine.grid[4][4] = True
        engine.grid[4][0] = True
        self.assertEqual(engine.count_neighbors(0, 0), 2)

    def test_resize(self):
        engine = GameOfLifeEngine(rows=5, cols=5)
        engine.grid[1][1] = True
        engine.resize(10, 12)
        self.assertEqual(engine.rows, 10)
        self.assertEqual(engine.cols, 12)
        self.assertTrue(engine.grid[1][1])

    def test_resize_shrink_preservation(self):
        engine = GameOfLifeEngine(rows=10, cols=10)
        engine.grid[2][2] = True
        engine.grid[8][8] = True  # outside shrunk area
        engine.resize(5, 5)
        self.assertEqual(engine.rows, 5)
        self.assertEqual(engine.cols, 5)
        self.assertTrue(engine.grid[2][2])
        self.assertEqual(engine.get_alive_count(), 1)

    def test_cycle_detection(self):
        # Test extinction detection
        engine = GameOfLifeEngine(rows=6, cols=6)
        status, period = engine.detect_status()
        self.assertEqual(status, "extinct")
        self.assertIsNone(period)

        # Test still life detection
        engine.grid[2][2] = True
        engine.grid[2][3] = True
        engine.grid[3][2] = True
        engine.grid[3][3] = True
        engine.sync_history()
        engine.step()
        status, period = engine.detect_status()
        self.assertEqual(status, "stable")
        self.assertEqual(period, 1)

        # Test oscillator detection
        engine.clear()
        engine.load_preset("blinker")
        engine.step()  # Gen 1
        engine.step()  # Gen 2 (matches Gen 0)
        status, period = engine.detect_status()
        self.assertEqual(status, "oscillator")
        self.assertEqual(period, 2)

    def test_toggle_and_set_cell(self):
        engine = GameOfLifeEngine(rows=5, cols=5)
        # Toggle alive
        result = engine.toggle_cell(2, 2)
        self.assertTrue(result)
        self.assertTrue(engine.grid[2][2])

        # Toggle dead
        result = engine.toggle_cell(2, 2)
        self.assertFalse(result)
        self.assertFalse(engine.grid[2][2])

        # Out of bounds toggle
        self.assertFalse(engine.toggle_cell(-1, 0))
        self.assertFalse(engine.toggle_cell(10, 10))

        # Explicit set_cell
        engine.set_cell(1, 3, True)
        self.assertTrue(engine.grid[1][3])
        engine.set_cell(1, 3, False)
        self.assertFalse(engine.grid[1][3])

    def test_rle_parser_and_exporter(self):
        engine = GameOfLifeEngine(rows=15, cols=15)
        # Glider in RLE format
        rle_glider = "#N Glider\nx = 3, y = 3, rule = B3/S23\nbob$2bo$3o!"
        success = engine.load_rle(rle_glider)
        self.assertTrue(success)
        self.assertEqual(engine.get_alive_count(), 5)

        # Export to RLE and re-import
        exported = engine.export_rle(name="TestExport")
        self.assertIn("x = ", exported)
        self.assertIn("rule = B3/S23", exported)

        new_engine = GameOfLifeEngine(rows=15, cols=15)
        success = new_engine.load_rle(exported)
        self.assertTrue(success)
        self.assertEqual(new_engine.get_alive_count(), 5)

    def test_plaintext_parser(self):
        engine = GameOfLifeEngine(rows=10, cols=10)
        cells_data = """!Name: Blinker
!Comment: Period 2 oscillator
...
.OOO.
...
"""
        success = engine.load_plaintext(cells_data)
        self.assertTrue(success)
        self.assertEqual(engine.get_alive_count(), 3)


if __name__ == "__main__":
    unittest.main()
