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

def draw_path(im, path, scale=10, color=(255, 0, 0)):
    if len(path) < 2:
        raise ValueError('The path has to consist of at least one move')

    endpos = path[-1]
    path = [((x+.5)*scale, (y+.5)*scale) for x, y in path]

    draw = ImageDraw.Draw(im)
    draw.line(path, fill=color)

    draw.ellipse([(endpos[0]*scale, endpos[1]*scale), ((endpos[0]+1)*scale,
        (endpos[1]+1)*scale)], outline=color)

    return im

def draw_tree(im, edges, scale=10, color=(0, 0, 255)):
    draw = ImageDraw.Draw(im)

    for e in edges:
        p1 = ((e[0][0]+.5)*scale, (e[0][1]+.5)*scale)
        p2 = ((e[1][0]+.5)*scale, (e[1][1]+.5)*scale)
        draw.line([p1, p2], fill=color)
    return im
