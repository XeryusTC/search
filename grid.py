# -*- coding: utf-8 -*-

OBSTACLE = 0
OPEN = 1

class Grid:
    def __init__(self, width, height):
        self.grid = {(x,y): OPEN for x in range(width) for y in range(height)}

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
