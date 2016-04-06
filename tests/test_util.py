# -*- coding: utf-8 -*-
import unittest
from unittest import mock

import grid
import util

class ProblemGenerateTests(unittest.TestCase):
    @mock.patch('util.grid.Grid')
    def test_generates_a_grid(self, GridMock):
        GridMock.return_value.open_cells = [(0,0), (0, 1), (1, 0)]
        util.generate_problem(10, 10, 0.1)
        GridMock.assert_called_once_with(10, 10, 0.1)

    def test_generates_a_grid_with_correct_width(self):
        g, _, _ = util.generate_problem(32, 16, 0)
        self.assertEqual(g.width, 32)

    def test_generates_a_grid_with_correct_height(self):
        g, _, _ = util.generate_problem(32, 16, 0)
        self.assertEqual(g.height, 16)

    def test_generates_a_grid_with_obstacles(self):
        g, _, _ = util.generate_problem(10, 10, 0.2)
        obs = sum([1 for x, y in g.grid if g.grid[x, y] == grid.OBSTACLE])
        self.assertAlmostEqual(obs/100, 0.2, delta=0.1)

    def test_start_and_goal_positions_are_not_the_same(self):
        for i in range(100):
            with self.subTest(i=i):
                g, start, end = util.generate_problem(5, 5, 0.2)
                self.assertNotEqual(start, end)
