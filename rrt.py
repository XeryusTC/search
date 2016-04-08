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
        dx = closest[0] - q[0]
        dy = closest[1] - q[1]
        x = max(-1, min(round(dx/dy), 1)) if dy != 0 else 1
        y = max(-1, min(round(dy/dx), 1)) if dx != 0 else 1
        c = (closest[0]-x, closest[1]-y)
        if c not in g.neighbours(*closest) or c in nodes:
            continue # skip inaccessible and already visited cells
        nodes.append(c)
        edges.append((closest, c))
        if c == goal:
            print('arrived at goal')
            return reconstruct(edges, start, goal)
    print('No path found')

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
            print(path)
            return path
    raise Exception('Could not reconstruct the path')

if __name__ == '__main__':
    g, start, goal = util.generate_problem(16, 16, 0.2)
    print('Start:', start, 'goal:', goal)
    path = rrt(g, start, goal)
    print('Found length vs heuristic:', len(path), grid.dist(start, goal))

    draw.draw_path(draw.draw_grid(g), path).show()
