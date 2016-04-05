# -*- coding: utf-8 -*-
import unittest
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
        self.assertCountEqual(g.neighbours(1, 1), [(0,1), (1,0), (1,2), (2,1)])

    def test_obstacle_has_no_neighbours(self):
        g = grid.Grid(6,4)
        g.grid[1, 1] = grid.OBSTACLE
        self.assertEqual(g.neighbours(1, 1), [])

    def test_edge_cells_dont_have_non_existent_neighbours(self):
        g = grid.Grid(6, 4)
        self.assertCountEqual(g.neighbours(0, 1), [(0,0), (1,1), (0,2)])
        self.assertCountEqual(g.neighbours(1, 0), [(0,0), (2,0), (1,1)])
        self.assertCountEqual(g.neighbours(5, 1), [(4,1), (5,0), (5,2)])
        self.assertCountEqual(g.neighbours(1, 3), [(0,3), (2,3), (1,2)])

    def test_corner_cells_dont_have_non_existent_neighbours(self):
        g = grid.Grid(6, 4)
        self.assertCountEqual(g.neighbours(0, 0), [(1,0), (0,1)])
        self.assertCountEqual(g.neighbours(5, 0), [(5,1), (4,0)])
        self.assertCountEqual(g.neighbours(0, 3), [(1,3), (0,2)])
        self.assertCountEqual(g.neighbours(5, 3), [(4,3), (5,2)])

    def test_obstacle_cells_are_not_in_neighbours(self):
        g = grid.Grid(6, 4)
        g.grid[1, 1] = grid.OBSTACLE
        self.assertCountEqual(g.neighbours(0, 1), [(0,0), (0,2)])
        self.assertCountEqual(g.neighbours(1, 2), [(0,2), (2,2), (1,3)])

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


if __name__ == '__main__':
    unittest.main()
