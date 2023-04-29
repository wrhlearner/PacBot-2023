from variables import *
import copy
import numpy as np
import time

WALKABLE_TILES = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 7), (1, 8), (1, 9), (1, 10), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (2, 1), (2, 4), (2, 7), (2, 10), (2, 22), (2, 25), (2, 29), (3, 1), (3, 4), (3, 5), (3, 6), (3, 7), (3, 10), (3, 22), (3, 25), (3, 29), (4, 1), (4, 4), (4, 10), (4, 22), (4, 25), (4, 29), (5, 1), (5, 4), (5, 10), (5, 22), (5, 25), (5, 29), (6, 1), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22), (6, 23), (6, 24), (6, 25), (6, 26), (6, 27), (6, 28), (6, 29), (7, 1), (7, 7), (7, 10), (7, 16), (7, 25), (7, 29), (8, 1), (8, 7), (8, 10), (8, 16), (8, 25), (8, 29), (9, 1), (9, 4), (9, 5), (9, 6), (9, 7), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 19), (9, 22), (9, 23), (9, 24), (9, 25), (9, 29), (10, 1), (10, 4), (10, 7), (10, 10), (10, 13), (10, 19), (10, 22), (10, 25), (10, 29), (11, 1), (11, 4), (11, 7), (11, 10), (11, 13), (11, 19), (11, 22), (11, 25), (11, 29), (12, 1), (12, 2), (12, 3), (12, 4), (12, 7), (12, 8), (12, 9), (12, 10), (12, 13), (12, 19), (12, 20), (12, 21), (12, 22), (12, 25), (12, 26), (12, 27), (12, 28), (12, 29), (13, 1), (13, 7), (13, 13), (13, 19), (13, 25), (14, 1), (14, 7), (14, 13), (14, 19), (14, 25), (15, 1), (15, 2), (15, 3), (15, 4), (15, 7), (15, 8), (15, 9), (15, 10), (15, 13), (15, 19), (15, 20), (15, 21), (15, 22), (15, 25), (15, 26), (15, 27), (15, 28), (15, 29), (16, 1), (16, 4), (16, 7), (16, 10), (16, 13), (16, 19), (16, 22), (16, 25), (16, 29), (17, 1), (17, 4), (17, 7), (17, 10), (17, 13), (17, 19), (17, 22), (17, 25), (17, 29), (18, 1), (18, 4), (18, 5), (18, 6), (18, 7), (18, 10), (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (18, 19), (18, 22), (18, 23), (18, 24), (18, 25), (18, 29), (19, 1), (19, 7), (19, 10), (19, 16), (19, 25), (19, 29), (20, 1), (20, 7), (20, 10), (20, 16), (20, 25), (20, 29), (21, 1), (21, 4), (21, 5), (21, 6), (21, 7), (21, 8), (21, 9), (21, 10), (21, 11), (21, 12), (21, 13), (21, 14), (21, 15), (21, 16), (21, 17), (21, 18), (21, 19), (21, 20), (21, 21), (21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27), (21, 28), (21, 29), (22, 1), (22, 4), (22, 10), (22, 22), (22, 25), (22, 29), (23, 1), (23, 4), (23, 10), (23, 22), (23, 25), (23, 29), (24, 1), (24, 4), (24, 5), (24, 6), (24, 7), (24, 10), (24, 22), (24, 25), (24, 29), (25, 1), (25, 4), (25, 7), (25, 10), (25, 22), (25, 25), (25, 29), (26, 1), (26, 2), (26, 3), (26, 4), (26, 7), (26, 8), (26, 9), (26, 10), (26, 22), (26, 23), (26, 24), (26, 25), (26, 26), (26, 27), (26, 28), (26, 29)]

def bfs(grid, start, target, max_dist=float("inf")):
    visited = []
    queue = [(start, [])]

    while len(queue) > 0:
        nxt = queue.pop(0)
        visited.append(nxt[0])
        new_path = copy.deepcopy(nxt[1])
        new_path.append(nxt[0])
        loc = nxt[0]
        if type(target) is tuple:
            if target == loc:
                return new_path
        elif grid[loc[0]][loc[1]] in target:
            return new_path

        if grid[loc[0] + 1][loc[1]] in [o, e, O] and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0] + 1, loc[1]),new_path))
        if grid[loc[0] - 1][loc[1]] in [o, e, O] and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0] - 1, loc[1]),new_path))
        if grid[loc[0]][loc[1] + 1] in [o, e, O] and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0], loc[1] + 1),new_path))
        if grid[loc[0]][loc[1] - 1] in [o, e, O] and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0], loc[1] - 1),new_path))

    return None

def a_star(state,
           grid, 
           start, 
           current_path, pellet_eaten,
           max_dist=float("inf"),
           max_duration=1000):
    """
    Inputs
        State: the state
        Grid: grid
        Start: Node with (x, y) value

    Output:
        Path: list of nodes [(x,y), (x,y)]
    """

    pellet_constant = 10
    ghost_constant = 0.1
    dist_constant = 3
    look_ahead = 5

    ghost_locations  = get_ghost_locations(state)

    if (package is not None):
        last_start, ghost_nodes_past = package
    else:
        last_start = start
        ghost_nodes_past = ghost_locations
    
    # if current_path == None:
        # first every node gets assigned a value based on pellet score and distance from ghost
        # they also get assigmed a parent
    h_scores = evaluate_grid(
                        grid, 
                        ghost_locations,
                        {}, 
                        pellet_constant, 
                        ghost_constant)
    # else:
    #     h_scores = update_heuristic_values(start, last_start,
    #                 pellet_eaten, ghost_nodes_past, 
    #                 ghost_locations, h_scores, 
    #                 pellet_constant, ghost_constant)


    time_before_a_star = time.time()
    parents, goal = do_a_star(grid, h_scores, start, look_ahead, dist_constant)
    print("A star time: ", time.time() - time_before_a_star)
    #print("Goal: ", goal)   
    #print(parents)

    #Search the next x moves for the path with the highest reward
    path = get_path(parents, goal)


    package = (start, ghost_locations)


    return path, package #in order to update them the next time around


def evaluate_grid(grid, ghost_locations, scores:dict, pellet_constant:int, ghost_constant:int):
    """
    Give every node a heuristic value, not including distance from the goal
    Inputs:
        grid: the grid and current state
        state: the state
        scores: at this point an empty dictionary
        pellet_constant: int pellet value
        ghost_constant: int ghost value
    returns:
        Scores: dictionary mapping scores to nodes {(x,y):int}
    """ 

    ghosts = ghost_locations

    for x in range(28):
        for y in range(30):

            if (x,y) not in WALKABLE_TILES:
                reward = 0
            else:
                reward = reward_between_points(grid, (x,y), ghost_constant,
                                           pellet_constant, ghosts)
            
            scores[(x,y)] = reward

    #evaluate parents

    return scores


def do_a_star(grid, scores:dict, start:tuple, max_step_amount:int, dist_constant:int):
    """
    Inputs:
        grid:
        Scores: Dictionary mapping scores to their values
        Start: Node (x,y) start node
        max_step_amount: integer looking at the nodes you are looking at 
        dist_constant: constant subtrated for the distance

    returns:
        Parents: dictionary mapping a parent node to its child (x,y):(a,b)
        Goal: Goal Node 
    """

    frontier = [start] #open list
    explored = [] #closed list
    parents = {}

    distance_incl_scores = {}
    distance_incl_scores[start] = scores[start]

    #we will have a list of goal states and return the goal state 
    # with the best value from the certain distance
    goal_states = []

    while len(frontier) != 0:
        # Set current node to the node in the unvisited list with the best f-score 
        current_node = best_nodes(scores, frontier)

        if done_search(grid, explored, start, max_step_amount):
                #pick the best goal state
                best_goal_state = best_nodes(scores, goal_states)
                explored.append(current_node)

                '''print("parents", parents)
                print("best goal",  best_goal_state)
                print("h_scores", scores)
                print("actual scores", distance_incl_scores)
                print(distance_incl_scores)'''
                return parents, best_goal_state
        
        #remove current node from frontier 
        frontier.remove(current_node)

        #add to closed list (explored)
        explored.append(current_node)
        
                #c) generate successors and set their parents to q
        neighbours = get_neighbours(grid, current_node)

        for n in neighbours:

            # i) if successor is the goal, stop search
            distance = grid_distance(grid, current_node, start)

            #add to goal state if past a certain set of steps from current 
            if (distance == max_step_amount):
                goal_states.append(n)

            # new score is the prev score of the prev node (heuritsic and actual)
            #plus the heuristic score of the current node
            #minus one because its one more distance away
            new_score =  distance_incl_scores[current_node] + scores[n] - dist_constant


            prev_cost = distance_incl_scores.get(n, -np.inf)

            if (n not in frontier and n not in explored):
                distance_incl_scores[n] = new_score
                frontier.append(n)
                parents[n] = current_node

            
            
    #print("parents", parents)
    #print("GOALS",  goal_states)
    #print(distance_incl_scores)
    return parents, best_nodes(scores, goal_states)

def done_search(grid, goal_nodes, start, max_step_amount):
    """
    returns True if all the nodes of a certain distance have been explored 
    goal_nodes is a list of explored nodes in (x, y) format. 
    start is the starting node in (x, y) format

    Input:
        goal_nodes: list of nodes [(x, y), (x1, y1)]
        start: node (x,y)
    returns True if all the nodes of a certain distance have been explored from the start position

    """
    if len(goal_nodes) == 0:
        return False

    # Perform BFS to walk through all nodes at distance `max_step_amount` from start
    queue = [(start, 0)] # (node, distance) 
    bfs_explored_nodes = [] # list of nodes that have been explored by the BFS algorithm used to check if all nodes have been explored

    while len(queue) > 0:
        node, node_distance = queue.pop(0)
        if node not in goal_nodes:
            return False # we have not explored this node
        
        if node_distance < max_step_amount:
            neighbours = get_neighbours(grid, node)
            for n in neighbours:
                if n not in bfs_explored_nodes:
                    queue.append((n, node_distance + 1))

        bfs_explored_nodes.append(node)

    return True


def get_neighbours(grid, current_node):
    """
    Input:
        grid - grid
        current node (x,y) current ndoe
    output:
        List of neighbouring nodes that are not a wall

    """
    neighbours = []
    x = current_node[0]
    y = current_node[1]
    
    #up
    if y-1 >= 0:
        if grid[x][y-1] != I:
            neighbours.append((x, y-1))
    if y+1 <= 29:
        if grid[x][y+1] != I:
            neighbours.append((x, y+1))
    if x-1 >= 0:
        if grid[x-1][y] != I:
            neighbours.append((x-1, y))
    if x+1 <= 29:
        if grid[x+1][y] != I:
            neighbours.append((x+1, y))
    
    return neighbours


def ghost_value(distances, constant):
    """
    Returns the heuristic updated value from the distance of the ghost from the node we want to get
    Input:
        Distance: List of distances from all 4 ghosts. Infinity of the ghosts are not on the grid 
        Constant: Positive constant that multiplies how close our node is to the ghost.
    Output: 
        int: Sum of all ghost values 
    NOTE: Edit this if we are having issues with heuristic, because it should be explonential probably
    """
    

    return -constant*(np.power(np.e, (60-distances[0])) + np.power(np.e, (60-distances[1])) + 
                      np.power(np.e, (60-distances[2])) + np.power(np.e, (60-distances[3])))

def update_heuristic_values(start, last_start,
                pellet_eaten, 
                ghost_nodes_past, 
                ghost_node_current, 
                scores, 
                pellet_constant, 
                ghost_constant):
    """
    Inputs:
        Pellet_eaten Node (x,y) of parent that has been eaten. None if nothing has been eaten
        ghost_nodes_past, List of ghosts and their location Node, none if ghosts are not on grid
            If any of the ghosts are None just reevaluate ngl
        Scores: Dicts of Nodes and corresponding scores6
        Pellet_Value: Value of having a pellet so we can subtract
    Returns: Updated Scores for each node

    THESE JUST RETURN THE HEURISTIC VALUE
    """

    if pellet_eaten is not None:
        scores[pellet_eaten] -= pellet_constant
    #figure out where each ghot has gone
    for i in range(4):
        #find the change between old and new ghost
        ghost_old = ghost_nodes_past[i]
        ghost_current = ghost_node_current[i]

        x_diff = ghost_old[0]-ghost_current[0]
        y_diff = ghost_old[1]-ghost_current[1]
        



def reward_between_points(grid, a:tuple, ghost_constant:int,
                           pellet_constant:int, ghosts:list):
    """
    Inputs:
        grid: the grid's current state
        a: Node with (x, y) value
        ghost constant: integer what we multiply by ghost values
        pellet_constant: integer what we multiply by ghost values
        ghosts: list of ghost locations [(x,y), (x1,y1)]
        
    Output:
        Value: int reward value for path between nodes
    """
    ghost_distances = []
    for g in ghosts:
        if g[0] == None or grid[g[0]][g[1]] == n:
            distance = 60
        else:
            distance = grid_distance(grid, a, g)
        ghost_distances.append(distance)
    val = ghost_value(ghost_distances, ghost_constant)

    if has_pellet(grid, a):
        val += pellet_constant

    return val 




def get_path(parents, current):
    """
    Inputs: 
        Parents: dictionary mapping a parent node to its child (x,y):(a,b)
        Current: the current node we are at (x,y)
    Output: 
        Path:
            list of nodes [(x,y), (a,b)]
    """
    total_path = [current]
    while current in parents.keys():
        current = parents[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def best_nodes(scores, visited):
    """
    Inputs: 
        Scores: dictionary mapping scores to nodes {(x,y):int}
        Visited: list of nodes that have been visited
    Output:
        max_node: node (x,y) that has biggest value in the visited
    
    """
    max_val = -np.inf
    max_node = visited[0]
    for node in visited:
        val = scores[node]
        if val > max_val:
            max_node = node
            max_val = val
    return max_node


def grid_distance(grid,a:int,b:list):
    """
    Input:
        Grid: 30x30 grid
        a: node (x,y)
        b: list of nodes [(x,y), (x1,y1)] of which we the num of the distances 
    Returns:
        int: lenght of shortest path between nodes

    """

    return len(bfs(grid, a, b))


def get_ghost_locations(state):
    """
    input:
        state from messgae
    output:
        list of nodes (x,y) for each ghost:
        location of 4 ghosts in (x,y) coords.
        If ghost doesn't exist return (None, None)
    """
    
    return [(ghost.x, ghost.y) for ghost in [state.red_ghost, state.blue_ghost, state.orange_ghost, state.pink_ghost]]

def has_pellet(grid, node):
    """
    Inputr
        Grid
        Node: (x,y)
    Output:
        True is has pellet False otherwise
    
    """
    x= node[0]
    y= node[1]
    if grid[x][y] == o or grid[x][y] == O:
        return True
    return False