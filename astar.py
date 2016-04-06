# -*- coding: utf-8 -*-
import heapq
import random
import grid

def generate_problem(width, height, obstacles):
    g = grid.Grid(width, height, obstacles)
    start = random.choice(g.open_cells)
    goal = random.choice(g.open_cells)
    while start == goal:
        goal = random.choice(g.open_cells)
    return g, start, goal

def astar(g, start, goal):
    closed = set()
    open_list = []
    heapq.heappush(open_list, (0, start))
    g_scores = {start: 0}
    came_from = {}

    while open_list != []:
        prio, current = heapq.heappop(open_list)
        if current == goal:
            return reconstruct(came_from, goal)

        closed.add(current)
        for n in g.neighbours(*current):
            if n in closed:
                continue # skip already evaluated neighbours

            g_score = g_scores[current] + 1
            if n in g_scores and g_score > g_scores[n]:
                continue # This is not a better path

            # Add the neighbour on the heap
            came_from[n] = current
            g_scores[n] = g_score
            heapq.heappush(open_list, (g_score + grid.dist(n, goal), n))
    print(came_from)
    return None

def reconstruct(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

if __name__ == '__main__':
    g, start, goal = generate_problem(32, 32, 0.2)
    print(start, goal)
    print(g)
    path = astar(g, start, goal)
    print(len(path), grid.dist(start, goal))
    print(path)
