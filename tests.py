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


@mock.patch('grid.ImageDraw', spec=True)
@mock.patch('grid.Image', spec=True)
class GridDrawTests(unittest.TestCase):
    """Tests for the Grid.draw() method"""
    def setUp(self):
        self.g = grid.Grid(16, 16)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def test_grid_draw_function_has_scale_parameter(self, ImageMock,
            ImageDrawMock):
        self.g.draw(scale=10)

    def test_grid_draw_function_creates_new_white_surface(self, ImageMock,
            ImageDrawMock):
        self.g.draw()
        ImageMock.new.assert_called_once_with('RGB', (160, 160), self.white)

    def test_surface_size_depends_on_scale(self, ImageMock, ImageDrawMock):
        self.g.draw(1)
        ImageMock.new.assert_called_with('RGB', (16, 16), self.white)
        self.g.draw(25)
        ImageMock.new.assert_called_with('RGB', (400, 400), self.white)

    def test_draws_on_surface(self, ImageMock, ImageDrawMock):
        im = ImageMock.new.return_value
        self.g.draw()
        ImageDrawMock.Draw.assert_called_once_with(im)

    def test_does_not_draw_open_cells(self, ImageMock, ImageDrawMock):
        draw = ImageDrawMock.Draw.return_value
        self.g.draw()
        draw.rectangle.assert_not_called()

    def test_draws_obstacles_as_black(self, ImageMock, ImageDrawMock):
        draw = ImageDrawMock.Draw.return_value
        self.g.grid[0, 0] = grid.OBSTACLE
        self.g.draw()
        draw.rectangle.assert_called_once_with((0, 0, 10, 10), fill=self.black)

    def test_draws_obstacles_in_correct_position(self, ImageMock,
            ImageDrawMock):
        self.g.grid[1, 1] = grid.OBSTACLE
        self.g.grid[9, 6] = grid.OBSTACLE
        draw = ImageDrawMock.Draw.return_value
        self.g.draw()
        draw.rectangle.assert_any_call((10, 10, 20, 20), fill=self.black)
        draw.rectangle.assert_any_call((90, 60, 100, 70), fill=self.black)
        self.assertEqual(draw.rectangle.call_count, 2)

    def test_draws_obstacles_in_correct_position_when_scaled(self, ImageMock,
            ImageDrawMock):
        self.g.grid[1, 1] = grid.OBSTACLE
        self.g.grid[9, 6] = grid.OBSTACLE
        draw = ImageDrawMock.Draw.return_value
        self.g.draw(5)
        draw.rectangle.assert_any_call((5, 5, 10, 10), fill=self.black)
        draw.rectangle.assert_any_call((45, 30, 50, 35), fill=self.black)
        self.assertEqual(draw.rectangle.call_count, 2)

    def test_raises_assert_when_scale_is_too_small(self, ImageMock,
            ImageDrawMock):
        with self.assertRaises(ValueError):
            self.g.draw(0)
        with self.assertRaises(ValueError):
            self.g.draw(-1)

    def test_returns_surface_object(self, ImageMock, ImageDrawMock):
        self.assertEqual(self.g.draw(), ImageMock.new.return_value)


if __name__ == '__main__':
    unittest.main()
