# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

OBSTACLE = 0
OPEN = 1

class Grid:
    def __init__(self, width, height):
        self.grid = {(x,y): OPEN for x in range(width) for y in range(height)}
        self.width = width
        self.height = height

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

    def draw(self, scale=10):
        if scale <= 0:
            raise ValueError('Scale must be positive')

        im = Image.new('RGB', (self.width*scale, self.height*scale),
            (255, 255, 255))
        draw = ImageDraw.Draw(im)

        for x, y in self.grid:
            if self.grid[x, y] == OBSTACLE:
                draw.rectangle((x*scale, y*scale, (x+1)*scale, (y+1)*scale),
                    fill=(0, 0, 0))
        return im
