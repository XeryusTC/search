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


@mock.patch('draw.ImageDraw', spec=True)
@mock.patch('draw.Image', spec=True)
class DrawPathTests(unittest.TestCase):
    def test_draws_on_surface_parameter(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        draw.draw_path(im, [(0, 0), (0, 1)])
        ImageDrawMock.Draw.assert_called_once_with(im)

    def test_path_drawn_from_centre_of_grid(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 1)])
        d.line.assert_called_once_with([(5, 5), (5, 15)], fill=(255, 0, 0))

    def test_path_must_have_at_least_two_steps(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        with self.assertRaises(ValueError):
            draw.draw_path(im, [])
        with self.assertRaises(ValueError):
            draw.draw_path(im, [(0, 0)])

    def test_line_gets_drawn_between_all_steps(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 1), (1, 1), (1, 0)])
        d.line.assert_called_once_with([(5, 5), (5, 15), (15, 15), (15, 5)],
            fill=(255, 0, 0))

    def test_can_have_scale_parameter(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 1)], scale=50)
        d.line.assert_called_once_with([(25, 25), (25, 75)], fill=(255, 0, 0))

    def test_can_set_path_colour(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 0)], color=(0, 255, 0))
        d.line.assert_called_once_with([(5, 5), (5, 5)], fill=(0, 255, 0))

    def test_path_colour_is_red_by_default(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 0)])
        d.line.assert_called_once_with([(5, 5), (5, 5)], fill=(255, 0, 0))

    def test_returns_original_surface_object(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        self.assertEqual(draw.draw_path(im, [(0, 0), (0, 0)]), im)

    def test_draws_circle_at_path_endpoint(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 0)])
        d.ellipse.assert_called_once_with([(0, 0), (10, 10)],
            outline=(255, 0, 0))

    def test_draws_circle_at_path_endpoint2(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (1, 0)])
        d.ellipse.assert_called_once_with([(10, 0), (20, 10)],
            outline=(255, 0, 0))

    def test_endpoint_circle_has_same_colour_as_path(self, ImageMock,
            ImageDrawMock):
        im = ImageMock.new()
        d = ImageDrawMock.Draw.return_value
        draw.draw_path(im, [(0, 0), (0, 0)], color=(0, 0, 255))
        d.ellipse.assert_called_once_with([(0, 0), (10, 10)],
            outline=(0, 0, 255))


@mock.patch('draw.ImageDraw')
@mock.patch('draw.Image')
class DrawTreeTests(unittest.TestCase):
    def test_draws_on_surface_parameter(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        draw.draw_tree(im, [((0, 0), (1, 1))])
        ImageDrawMock.Draw.assert_called_once_with(im)

    def test_returns_original_surface_object(self, ImageMock, ImageDrawMock):
        im = ImageMock.new()
        self.assertEqual(draw.draw_tree(im, []), im)

    def test_branch_drawn_from_centre_of_grid(self, ImageMock, ImageDrawMock):
        d = ImageDrawMock.Draw.return_value
        draw.draw_tree(None, [((0, 0), (0, 1))])
        d.line.assert_called_once_with([(5, 5), (5, 15)], fill=(0, 0, 255))

    def test_line_gets_drawn_for_each_edge(self, ImageMock, ImageDrawMock):
        d = ImageDrawMock.Draw.return_value
        draw.draw_tree(None, [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((5, 5), (6, 6))])
        self.assertEqual(d.line.call_count, 3)

    def test_can_have_scale_parameter(self, ImageMock, ImageDrawMock):
        d = ImageDrawMock.Draw.return_value
        draw.draw_tree(None, [((0, 0), (0, 1))], scale=20)
        d.line.assert_called_once_with([(10, 10), (10, 30)], fill=(0, 0, 255))

    def test_can_set_tree_colour(self, ImageMock, ImageDrawMock):
        d = ImageDrawMock.Draw.return_value
        draw.draw_tree(None, [((0, 0), (0, 1))], color=(255, 255, 0))
        d.line.assert_called_once_with([(5, 5), (5, 15)], fill=(255, 255, 0))

    def test_path_colour_is_blue_by_default(self, ImageMock, ImageDrawMock):
        d = ImageDrawMock.Draw.return_value
        draw.draw_tree(None, [((0, 0), (0, 1))])
        d.line.assert_called_once_with([(5, 5), (5, 15)], fill=(0, 0, 255))
