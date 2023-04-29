from search import bfs
from grid import grid
from variables import *

def isWalkable(node, start_position):
    if grid[node[0]][node[1]] == I or grid[node[0]][node[1]] == n:
        return False
    
    return bfs(grid, start_position, node) is not None

def findWalkableTiles(start_position):
    walkableTiles = []
    for x in range(28):
        for y in range(30):
            if isWalkable((x, y), start_position):
                walkableTiles.append((x, y))
    
    return walkableTiles