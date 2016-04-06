# -*- coding: utf-8 -*-
import random
import grid

def generate_problem(width, height, obstacles):
    g = grid.Grid(width, height, obstacles)
    start = random.choice(g.open_cells)
    goal = random.choice(g.open_cells)
    while start == goal:
        goal = random.choice(g.open_cells)
    return g, start, goal
