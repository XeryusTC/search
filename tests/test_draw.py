# -*- coding: utf-8 -*-
import unittest
from unittest import mock

import grid
import draw

@mock.patch('draw.ImageDraw', spec=True)
@mock.patch('draw.Image', spec=True)
class GridDrawTests(unittest.TestCase):
    """Tests for the Grid.draw() method"""
    def setUp(self):
        self.g = grid.Grid(16, 16)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def test_grid_draw_function_has_scale_parameter(self, ImageMock,
            ImageDrawMock):
        draw.draw_grid(self.g, scale=1)

    def test_grid_draw_function_creates_new_white_surface(self, ImageMock,
            ImageDrawMock):
        draw.draw_grid(self.g)
        ImageMock.new.assert_called_once_with('RGB', (160, 160), self.white)

    def test_surface_size_depends_on_scale(self, ImageMock, ImageDrawMock):
        draw.draw_grid(self.g, 1)
        ImageMock.new.assert_called_with('RGB', (16, 16), self.white)
        draw.draw_grid(self.g, 25)
        ImageMock.new.assert_called_with('RGB', (400, 400), self.white)

    def test_draws_on_surface(self, ImageMock, ImageDrawMock):
        im = ImageMock.new.return_value
        draw.draw_grid(self.g)
        ImageDrawMock.Draw.assert_called_once_with(im)

    def test_does_not_draw_open_cells(self, ImageMock, ImageDrawMock):
        draw = ImageDrawMock.Draw.return_value
        draw.draw_grid(self.g)
        draw.rectangle.assert_not_called()

    def test_draws_obstacles_as_black(self, ImageMock, ImageDrawMock):
        d = ImageDrawMock.Draw.return_value
        self.g.grid[0, 0] = grid.OBSTACLE
        draw.draw_grid(self.g)
        d.rectangle.assert_called_once_with((0, 0, 10, 10), fill=self.black)

    def test_draws_obstacles_in_correct_position(self, ImageMock,
            ImageDrawMock):
        self.g.grid[1, 1] = grid.OBSTACLE
        self.g.grid[9, 6] = grid.OBSTACLE
        d = ImageDrawMock.Draw.return_value
        draw.draw_grid(self.g)

        d.rectangle.assert_any_call((10, 10, 20, 20), fill=self.black)
        d.rectangle.assert_any_call((90, 60, 100, 70), fill=self.black)
        self.assertEqual(d.rectangle.call_count, 2)

    def test_draws_obstacles_in_correct_position_when_scaled(self, ImageMock,
            ImageDrawMock):
        self.g.grid[1, 1] = grid.OBSTACLE
        self.g.grid[9, 6] = grid.OBSTACLE
        d = ImageDrawMock.Draw.return_value

        draw.draw_grid(self.g, 5)

        d.rectangle.assert_any_call((5, 5, 10, 10), fill=self.black)
        d.rectangle.assert_any_call((45, 30, 50, 35), fill=self.black)
        self.assertEqual(d.rectangle.call_count, 2)

    def test_raises_assert_when_scale_is_too_small(self, ImageMock,
            ImageDrawMock):
        with self.assertRaises(ValueError):
            draw.draw_grid(self.g, 0)
        with self.assertRaises(ValueError):
            draw.draw_grid(self.g, -1)

    def test_returns_surface_object(self, ImageMock, ImageDrawMock):
        self.assertEqual(draw.draw_grid(self.g), ImageMock.new.return_value)
