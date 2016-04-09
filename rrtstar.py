# -*- coding: utf-8 -*-
import random

import draw
import grid
import util

def rrtstar(g, start, goal, max_iter=10000):
    nodes = {start: 0}
    edges = []
    for i in range(max_iter):
        q = (random.randrange(g.width), random.randrange(g.height))
        # Find closest node to the sample
        closest = start
        dist = grid.dist(closest, q)
        for n in nodes:
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

        # find the neighbour with the lowest cost
        cost = nodes[closest]
        for n in g.neighbours(*c):
            if n in nodes and nodes[n] < cost:
                cost = nodes[n]
                closest = n

        nodes[c] = nodes[closest] + grid.cost(closest, c)
        edges.append((closest, c))

        # Update edges from other nodes
        for n in g.neighbours(*c):
            if n in nodes:
                update_shortest_path(grid, nodes, edges, n)

        if c == goal:
            print('arrived at goal')
            return (reconstruct(edges, start, goal), edges)
    print('No path found')
    return None, edges

def update_shortest_path(grid, nodes, edges, node):
    for n in g.neighbours(*node):
        if n in nodes and nodes[n] + grid.cost(n, node) < nodes[node]:
            # remove current edge
            for parent in nodes:
                if (parent, node) in edges:
                    edges.remove((parent, node))
                    break
            # set new edge
            edges.append((n, node))
            nodes[node] = nodes[n] + grid.cost(n, node)
    # update all children
    update_costs(grid, nodes, edges, node)

def update_costs(grid, nodes, edges, node):
    update = []
    for s, e in edges:
        if e == node:
            nodes[node] = nodes[s] + grid.cost(s, node)
        if s == node:
            update.append(e)
    for n in update:
        update_costs(grid, nodes, edges, n)

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
    path, edges = rrtstar(g, start, goal)
    if path != None:
        print('Found length vs heuristic:', len(path), grid.dist(start, goal))

    im = draw.draw_tree(draw.draw_grid(g), edges)
    if path != None:
        draw.draw_path(im, path)
    im.show()
