"""
Unit tests for Conway's Game of Life (GameOfLifeEngine)
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
        engine = GameOfLifeEngine(rows=30, cols=50)
        for preset_name in ["blinker", "toad", "beacon", "glider", "pulsar", "gosper_gun"]:
            success = engine.load_preset(preset_name)
            self.assertTrue(success, f"Failed to load preset '{preset_name}'")
            self.assertGreater(engine.get_alive_count(), 0)

        self.assertFalse(engine.load_preset("non_existent_preset"))

    def test_toroidal_wrapping(self):
        # Glider hitting right-bottom edge wraps around with wrap=True
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


if __name__ == "__main__":
    unittest.main()
