# -*- coding: utf-8 -*-
import draw
import grid
import util

def iddfs(g, start, goal):
    for i in range(40):
        path = iddfs_rec(g, start, goal, [start], i)
        if path != None:
            return path
    return None

def iddfs_rec(g, pos, goal, path, max_depth):
    if len(path) > max_depth:
        return None
    if pos == goal:
        return path

    for n in g.neighbours(*pos):
        if n in path:
            continue # don't follow loops
        p = iddfs_rec(g, n, goal, path + [n], max_depth)
        if p != None:
            return p
    return None

if __name__ == '__main__':
    g, start, goal = util.generate_problem(16, 16, 0.2)
    print('Start:', start, 'goal:', goal)
    path = iddfs(g, start, goal)
    print('Found length vs heuristic:', len(path), grid.dist(start, goal))

    draw.draw_path(draw.draw_grid(g), path).show()
