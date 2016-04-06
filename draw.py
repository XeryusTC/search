# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

import grid

def draw_grid(g, scale=10):
    if scale <= 0:
        raise ValueError('Scale must be positive')
    im = Image.new('RGB', (g.width*scale, g.height*scale), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for x, y in g.grid:
        if g.grid[x, y] == grid.OBSTACLE:
            draw.rectangle((x*scale, y*scale, (x+1)*scale, (y+1)*scale),
                fill=(0, 0, 0))

    return im
