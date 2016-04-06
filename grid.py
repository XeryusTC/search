# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import random

OBSTACLE = 0
OPEN = 1

class Grid:
    def __init__(self, width, height, obstacles=0):
        if not 0 <= obstacles < 1:
            raise ValueError('Chance of obstacles should be 0 <= P < 1')
        self.width = width
        self.height = height

        self.grid = {}
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < obstacles:
                    self.grid[x, y] = OBSTACLE
                else:
                    self.grid[x, y] = OPEN

    def neighbours(self, x, y):
        if self.grid[x, y] == OBSTACLE:
            return []
        ret = []
        for p in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            try:
                if self.grid[x+p[0], y+p[1]] == OPEN:
                    ret.append((x+p[0], y+p[1]))
            except KeyError:
                pass
        return ret

    def __str__(self):
        ret = '+' + '-' * self.width + '+\n'
        for y in range(self.height):
            ret += '|'
            for x in range(self.width):
                if self.grid[x, y] == OPEN:
                    ret += ' '
                elif self.grid[x, y] == OBSTACLE:
                    ret += 'X'
            ret += '|\n'
        ret += '+' + '-' * self.width + '+'
        return ret

    @property
    def open_cells(self):
        return [k for k in self.grid if self.grid[k] == OPEN]


def dist(s, d):
    return abs(s[0] - d[0]) + abs(s[1] - d[1])
