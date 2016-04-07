# -*- coding: utf-8 -*-
import draw
import grid
import util

def dfs(g, start, goal):
    return dfs_rec(g, start, goal, [start])

def dfs_rec(g, pos, goal, path):
    if pos == goal:
        return path
    if len(path) > 50:
        return None

    for n in g.neighbours(*pos):
        if n in path:
            continue # skip already visited neighbours
        p = dfs_rec(g, n, goal, path + [n])
        if p != None:
            return p
    return None

if __name__ == '__main__':
    g, start, goal = util.generate_problem(16, 16, 0.2)
    print('Start:', start, 'goal:', goal)
    path = dfs(g, start, goal)
    print('Found length vs heuristic:', len(path), grid.dist(start, goal))

    draw.draw_path(draw.draw_grid(g), path).show()
