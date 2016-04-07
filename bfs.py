# -*- coding: utf-8 -*-
import draw
import grid
import util

def bfs(g, start, goal):
    closed = set()
    queue = [(start, [start])]

    while queue != []:
        node, path = queue[0]
        if node == goal:
            return path
        queue = queue[1:]

        closed.add(node)
        for n in g.neighbours(*node):
            if n in closed:
                continue # skip already evaluated neighbours
            queue.append((n, path + [n]))

    return None

if __name__ == '__main__':
    g, start, goal = util.generate_problem(32, 32, 0.3)
    print('Start:', start, 'goal:', goal)
    path = bfs(g, start, goal)
    print('Found length vs heuristic:', len(path), grid.dist(start, goal))

    draw.draw_path(draw.draw_grid(g), path).show()
