# -*- coding: utf-8 -*-
import random
import draw
import grid
import util

def rrtstar(g, start, goal, max_iter=10000):
    nodes = {start: {'cost': 0, 'parent': None}}
    for i in range(max_iter):
        # Pick a random point in the grid
        q = (random.randrange(g.width), random.randrange(g.height))
        # Find the cell in the tree closest to random point
        closest_tree_node = start
        dist = grid.dist(q, closest_tree_node)
        for cell in nodes.keys():
            if dist > grid.dist(q, cell):
                closest_tree_node = cell
                dist = grid.dist(q, cell)
        # Find a neighbour of closest that is even closer to q
        best_new_node = closest_tree_node
        for n in g.neighbours(*closest_tree_node):
            if dist > grid.dist(q, n):
                best_new_node = n
                dist = grid.dist(q, n)
        if best_new_node in nodes:
            continue # skip nodes if they are already in the tree
        # Find the neighbour of the best cell with the lowest cost
        best_parent = start
        cost = 10000
        for n in g.neighbours(*best_new_node):
            if n not in nodes:
                continue
            if nodes[n]['cost'] + grid.cost(best_new_node, n) < cost:
                best_parent = n
                cost = nodes[n]['cost'] + grid.cost(best_new_node, n)
        # Add new node
        cost = nodes[best_parent]['cost'] + grid.cost(best_parent, best_new_node)
        nodes[best_new_node] = {'cost': cost, 'parent': best_parent}
        if best_new_node == goal:
            return _reconstruct_path(goal, nodes), _build_edge_list(nodes)
        # Check the neighbours if their cost can be decreased by connecting to the new node
        for n in g.neighbours(*best_new_node):
            if n not in nodes:
                continue
            if nodes[n]['cost'] > cost + grid.cost(best_new_node, n):
                nodes[n]['parent'] = best_new_node
                nodes[n]['cost'] = cost + grid.cost(best_new_node, n)
                _update_child_cost(nodes, n)
    print('no path')
    return None, _build_edge_list(nodes)

def _update_child_cost(nodes, parent):
    for node in nodes:
        if nodes[node]['parent'] == parent:
            nodes[node]['cost'] = nodes[parent]['cost'] + grid.cost(parent, node)
            _update_child_cost(nodes, node)

def _reconstruct_path(goal, nodes):
    path = []
    last = goal
    while last != None:
        path.append(last)
        last = nodes[last]['parent']
    path.reverse()
    return path

def _build_edge_list(nodes):
    return [(nodes[node]['parent'], node) for node in nodes if nodes[node]['parent'] != None]

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
