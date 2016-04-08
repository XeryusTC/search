# -*- coding: utf-8 -*-
import unittest
import unittest.mock as mock
import grid

class GridTests(unittest.TestCase):
    def test_grid_ctor_requires_size(self):
        with self.assertRaises(TypeError):
            g = grid.Grid()
        g = grid.Grid(5, 5)

    def test_grid_has_no_obstacles_by_default(self):
        g = grid.Grid(6, 4)
        for x in range(6):
            for y in range(4):
                with self.subTest(pos=(x,y)):
                    self.assertEqual(g.grid[x,y], grid.OPEN)

    def test_can_get_grid_neighbours(self):
        g = grid.Grid(6, 4)
        self.assertCountEqual(g.neighbours(1, 1), [(0,0), (0,1), (0,2), (1,0),
            (1,2), (2,0), (2,1), (2,2)])

    def test_obstacle_has_no_neighbours(self):
        g = grid.Grid(6,4)
        g.grid[1, 1] = grid.OBSTACLE
        self.assertEqual(g.neighbours(1, 1), [])

    def test_edge_cells_dont_have_non_existent_neighbours(self):
        g = grid.Grid(6, 4)
        self.assertCountEqual(g.neighbours(0, 1), [(0,0), (0,2), (1,0), (1,1),
            (1,2)])
        self.assertCountEqual(g.neighbours(1, 0), [(0,0), (2,0), (0,1), (1,1),
            (2,1)])
        self.assertCountEqual(g.neighbours(5, 1), [(4,0), (4,1), (4,2), (5,0),
            (5,2)])
        self.assertCountEqual(g.neighbours(1, 3), [(0,3), (2,3), (0,2), (1,2),
            (2,2)])

    def test_corner_cells_dont_have_non_existent_neighbours(self):
        g = grid.Grid(6, 4)
        self.assertCountEqual(g.neighbours(0, 0), [(1,0), (0,1), (1,1)])
        self.assertCountEqual(g.neighbours(5, 0), [(5,1), (4,0), (4,1)])
        self.assertCountEqual(g.neighbours(0, 3), [(1,3), (0,2), (1,2)])
        self.assertCountEqual(g.neighbours(5, 3), [(4,3), (5,2), (4,2)])

    def test_obstacle_cells_are_not_in_neighbours(self):
        g = grid.Grid(6, 4)
        g.grid[1, 1] = grid.OBSTACLE
        self.assertCountEqual(g.neighbours(0, 1), [(0,0), (0,2), (1,0), (1,2)])
        self.assertCountEqual(g.neighbours(1, 2), [(0,1), (2,1), (0,2), (2,2),
            (0,3), (1,3), (2,3)])

    def test_string_representation(self):
        g = grid.Grid(3, 3)
        self.assertEqual(str(g), "+---+\n|   |\n|   |\n|   |\n+---+")

    def test_string_representation_with_obstacles(self):
        g = grid.Grid(3, 3)
        g.grid[1, 1] = grid.OBSTACLE
        self.assertEqual(str(g), "+---+\n|   |\n| X |\n|   |\n+---+")

    def test_string_representation_complex(self):
        g = grid.Grid(6, 4)
        g.grid[1, 1] = grid.OBSTACLE
        g.grid[2, 3] = grid.OBSTACLE
        g.grid[4, 1] = grid.OBSTACLE
        g.grid[5, 0] = grid.OBSTACLE
        self.assertEqual(str(g), "+------+\n|     X|\n| X  X |\n|      |\n" +
            "|  X   |\n+------+")

    def test_ctor_can_generate_random_obstacles(self):
        g = grid.Grid(10, 10, 0.2)
        obs = sum([1 for x, y in g.grid if g.grid[x, y] == grid.OBSTACLE])
        self.assertAlmostEqual(obs/100, 0.2, delta=0.15)

    def test_ctor_random_obstacles_greater_or_equal_to_zero(self):
        with self.assertRaises(ValueError):
            grid.Grid(10, 10, -0.1)
        with self.assertRaises(ValueError):
            grid.Grid(10, 10, -1)

    def test_ctor_random_obstacles_smaller_than_one(self):
        with self.assertRaises(ValueError):
            grid.Grid(10, 10, 1)

    def test_open_cell_list_contains_all_cells_when_no_obstacles(self):
        g = grid.Grid(10, 10)
        self.assertCountEqual(g.open_cells, g.grid.keys())

    def test_open_cell_list_does_not_contain_obstacle_cells(self):
        g = grid.Grid(10, 10)
        g.grid = {(x, y): grid.OBSTACLE for x in range(10) for y in range(10)}
        self.assertEqual(g.open_cells, [])

    def test_open_cell_list_does_not_contain_obstacle_cells2(self):
        g = grid.Grid(5, 5)
        g.grid[1, 1] = grid.OBSTACLE
        g.grid[2, 3] = grid.OBSTACLE
        g.grid[4, 4] = grid.OBSTACLE
        g.grid[4, 1] = grid.OBSTACLE
        self.assertEqual(len(g.open_cells), 21)
        self.assertNotIn((1, 1), g.open_cells)
        self.assertNotIn((2, 3), g.open_cells)
        self.assertNotIn((4, 4), g.open_cells)
        self.assertNotIn((4, 1), g.open_cells)


class DistanceHeuristicTests(unittest.TestCase):
    def test_cost_is_zero_for_same_start_and_destination(self):
        self.assertEqual(grid.dist((0, 0), (0, 0)), 0)
        self.assertEqual(grid.dist((1, 5), (1, 5)), 0)
        self.assertEqual(grid.dist((7, 2), (7, 2)), 0)

    def test_cost_is_equal_to_number_of_optimal_straight_line_steps(self):
        self.assertEqual(grid.dist((0, 0), (10, 10)), 10)
        self.assertEqual(grid.dist((5, 7), (3, 9)), 2)
        self.assertEqual(grid.dist((31, 8), (78, 2)), 47)
        self.assertEqual(grid.dist((9, 7), (1, 2)), 8)
        self.assertEqual(grid.dist((6, 2), (8, 13)), 11)
