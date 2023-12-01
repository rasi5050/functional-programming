"""
Author: Rasi
10/28/2023
A* algorithm using functional programming in Python

Refferences
python functional programming: https://docs.python.org/3/howto/functional.html
A* algorithm: https://en.wikipedia.org/wiki/A*_search_algorithm
"""

from heapq import heappop, heappush, heapify
from math import inf

def reconstruct_path(cameFrom, current):
    if current is None: return []       
    #reconstructing path; prepending to list
    return reconstruct_path(cameFrom, cameFrom.get(current)) + [current]

def aStar(start, goal, h, nodes, edge):

    #best score from start node till any node, default infinity
    gScore = {node: inf for node in nodes}

    #fScore[n] = gScore[n] + h(n)
    fScore = {node: inf for node in nodes}

    #starting node states
    gScore[start] = 0
    fScore[start] = h(start)
    state = ([[fScore[start], start]], {start: None}, gScore, fScore)

    result = aStarRecurse(state, goal, h, edge)
    if result:
        cameFrom, current = result
        return reconstruct_path(cameFrom, current)
    else:
        return 'failed'

def aStarRecurse(state, goal, h, edge):
    #openSet = set of discovered nodes, 
    #cameFrom = node immediately preceding it on the cheapest path from the start to n currently known.
    openSet, cameFrom, gScore, fScore = state

    if not openSet: return None
    
    current_score, current = heappop(openSet)
    if current == goal: return (cameFrom, current)

    #find neighbors
    neighbors = {*{neighbor for (a, neighbor) in edges if a == current}, *{a for (neighbor, a) in edges if neighbor == current}}

    newOpenSet = list(openSet)
    newCameFrom = dict(cameFrom)
    newGScore = dict(gScore)
    newFScore = dict(fScore)

    #update the scores.
    for neighbor in neighbors:
        tentative_gScore = gScore[current] + edge(current, neighbor)
        if tentative_gScore < newGScore.get(neighbor, inf):
            newCameFrom[neighbor] = current
            newGScore[neighbor] = tentative_gScore
            newFScore[neighbor] = tentative_gScore + h(neighbor)
            heappush(newOpenSet, (newFScore[neighbor], neighbor))
    #recurse with new state
    return aStarRecurse((newOpenSet, newCameFrom, newGScore, newFScore), goal, h, edge)

def edge(a, b):
    return edges.get((a, b), edges.get((b, a), inf))


#test cases
#1
def h(node):
    heuristic = {'A': 2, 'B': 2, 'C': 1, 'D': 4, 'E': 1}
    return heuristic[node]

nodes = ['A', 'B', 'C', 'D', 'E']
edges = {
    ('A', 'B'): 2, 
    ('B', 'C'): 3, 
    ('A', 'D'): 4, 
    ('D', 'E'): 4, 
    ('C', 'E'): 1
}

path = aStar('A', 'E', h, nodes, edge)
assert path == ['A', 'B', 'C', 'E'], f"path should be ['A', 'B', 'C', 'E'], but got {path}"

print(f"1. for nodes {nodes} \n connected via edges {edges} \n with h(n) as 'A': 2, 'B': 2, 'C': 1, 'D': 4, 'E': 1")
print(f'the resultng path by A* algorithm is {path} \n \n ')

#2
# Test Case 1: Straightforward path with no alternative routes.
nodes1 = ['A', 'B', 'C', 'D', 'E']
edges = {
    ('A', 'B'): 1,
    ('B', 'C'): 1,
    ('C', 'D'): 1,
    ('D', 'E'): 1
}
def h1(node):
    heuristic1 = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    return heuristic1[node]
def edge1(a, b):
    return edges.get((a, b), edges.get((b, a), inf))
path1 = aStar('A', 'E', h1, nodes1, edge1)
assert path1 == ['A', 'B', 'C', 'D', 'E'], f"Expected ['A', 'B', 'C', 'D', 'E'], but got {path1}"

print(f"2. for nodes {nodes1} \n connected via edges {edges} \n with h(n) as 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0")
print(f'the resultng path by A* algorithm is {path1} \n \n ')

#3
# Test Case 2: Heuristic leads the wrong way.
nodes2 = ['A', 'B', 'C', 'D', 'E']
edges = {
    ('A', 'B'): 1,
    ('B', 'C'): 5,
    ('A', 'D'): 2,
    ('D', 'E'): 1,
    ('E', 'C'): 1
}
def h2(node):
    heuristic2 = {'A': 3, 'B': 2, 'C': 0, 'D': 2, 'E': 1}
    return heuristic2[node]
path2 = aStar('A', 'C', h2, nodes2, edge1)
assert path2 == ['A', 'D', 'E', 'C'], f"Expected ['A', 'D', 'E', 'C'], but got {path2}"

print(f"3. for nodes {nodes2} \n connected via edges {edges} \n with h(n) as 'A': 3, 'B': 2, 'C': 0, 'D': 2, 'E': 1")
print(f'the resultng path by A* algorithm is {path2} \n \n ')

#4
# Test Case 3: No valid path to the goal.
nodes3 = ['A', 'B', 'C', 'D', 'E']
edges = {
    ('A', 'B'): 1,
    ('B', 'D'): 1,
    ('D', 'E'): 1
}
def h3(node):
    heuristic3 = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    return heuristic3[node]
path3 = aStar('A', 'C', h3, nodes3, edge1)
assert path3 == 'failed', f"Expected 'failed', but got {path3}"

print(f"4. for nodes {nodes3} \n connected via edges {edges} \n with h(n) as 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0")
print(f'the resultng path by A* algorithm is {path3} \n \n ')


#4
nodes4 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
edges = {
    ('A', 'B'): 2, 
    ('A', 'C'): 1, 
    ('C', 'D'): 1,
    ('D', 'E'): 5,
    ('B', 'F'): 3,
    ('F', 'G'): 2,
    ('G', 'E'): 2
}

def h4(node):
    heuristic = {'A': 6, 'B': 7, 'C': 5, 'D': 5, 'E': 0, 'F': 5, 'G': 2}
    return heuristic[node]

path = aStar('A', 'E', h4, nodes4, edge)
assert path == ['A', 'C', 'D', 'E'], f"Expected '['A', 'C', 'D', 'E']', but got {path}"

print(f"5. for nodes {nodes4} \n connected via edges {edges} \n with h(n) as 'A': 6, 'B': 7, 'C': 5, 'D': 5, 'E': 0, 'F': 5, 'G': 2")
print(f'the resultng path by A* algorithm is {path}')



