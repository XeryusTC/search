# -*- coding: utf-8 -*-
import random

import draw
import grid
import util

def rrt(g, start, goal, max_iter=10000):
    nodes = [start]
    edges = []
    for i in range(max_iter):
        q = (random.randrange(g.width), random.randrange(g.height))
        # Find closest node
        closest = nodes[0]
        dist = grid.dist(closest, q)
        for n in nodes[1:]:
            if grid.dist(n, q) < dist:
                closest = n
                dist = grid.dist(n, q)
        # Find grid cell that is most in direction of sample
        c = g.neighbours(*closest)[0]
        dist = grid.dist(c, q)
        for n in g.neighbours(*closest):
            if grid.dist(n, q) < dist:
                c = n
                dist = grid.dist(n, q)
        if c in nodes:
            continue # skip already visited cells
        nodes.append(c)
        edges.append((closest, c))
        if c == goal:
            print('arrived at goal')
            return (reconstruct(edges, start, goal), edges)
    print('No path found')
    return None, edges

def reconstruct(edges, start, goal):
    path = [goal]
    current = goal
    for i in range(len(edges)*100):
        for s, e in edges:
            if e == current:
                path.append(s)
                current = s
        if current == start:
            path.reverse()
            return path
    raise Exception('Could not reconstruct the path')

if __name__ == '__main__':
    g, start, goal = util.generate_problem(32, 32, 0.2)
    print('Start:', start, 'goal:', goal)
    path, edges = rrt(g, start, goal)
    if path != None:
        print('Found length vs heuristic:', len(path), grid.dist(start, goal))

    im = draw.draw_tree(draw.draw_grid(g), edges)
    if path != None:
        draw.draw_path(im, path)
    im.show()
