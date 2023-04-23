from variables import *
import copy
import numpy as np

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
    ghost_constant = 100
    dist_constant = 3
    look_ahead = 5
    
    # if current_path == None:
        # first every node gets assigned a value based on pellet score and distance from ghost
        # they also get assigmed a parent
    h_scores = evaluate_grid(
                        grid, 
                        state,
                        {}, 
                        pellet_constant, 
                        ghost_constant)
    # else:
    #     h_scores = update_heuristic_values(start, last_start,
    #                            pellet_eaten, 
    #                            ghost_nodes_past, 
    #                            ghost_node_current, 
    #                            h_scores, 
    #                            pellet_value, 
    #                            ghost_constant)

    parents, goal = do_a_star(grid, h_scores, start, look_ahead, dist_constant)

    #Search the next x moves for the path with the highest reward
    path = get_path(parents, goal)


    return path #in order to update them the next time around


def evaluate_grid(grid, state, scores:dict, pellet_constant:int, ghost_constant:int):
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

    ghosts = get_ghost_locations(state)

    for x in range(28):
        for y in range(30):
<<<<<<< HEAD
<<<<<<< HEAD
        #set reward 
            if grid[x][y] == I:
=======
            #set reward
            if grid[x][y] == I or grid[x][y] == e or grid[x][y] == n:
>>>>>>> 4456544c5bd95b46f140f0acc0352de8365b5303
=======
            #set reward
            if grid[x][y] == I or grid[x][y] == e or grid[x][y] == n:

>>>>>>> df5812fb4242f7ce0e9c77b51d0f30055c71fada
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

    frontier = [start]
    explored = []
    parents = {}

    #we will have a list of goal states and return the goal state 
    # with the best value from the certain distance
    goal_states = []

    while len(frontier) != 0:
        print("begin",frontier)
        current_node = best_nodes(scores, frontier)
        explored.append(current_node)
        
        
        # b) pop q off the open list
        frontier = frontier[1:]
  
        #c) generate successors and set their parents to q
        neighbours = get_neighbours(grid, current_node)

        for n in neighbours:
            parents[n] = current_node


            # i) if successor is the goal, stop search
            if done_search(grid, explored, start, max_step_amount):
                #pick the best goal state
                best_goal_state = best_nodes(scores, goal_states)
                return parents, best_goal_state
            
            distance = grid_distance(grid, current_node, start)

            #add to goal state if past a certain set of steps from current 
            if (distance == max_step_amount):
                goal_states.append(n)

            # new score is the prev score of the prev node (heuritsic and actual)
            #plus the heuristic score of the current node
            #minus one because its one more distance away
            new_score = scores[n] + scores[current_node] - dist_constant

            #if a node with the same position as successor is
            #  in the OPEN list which has alower f than successor, 
            # skip this successor

            prev_cost = scores[n]
            if (new_score > prev_cost):
                scores[n] = new_score
                frontier.append(n)
                print(frontier)
        
        
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
    path = 0
    for d in distances:
        path += d

    return -constant* (60-d)

# def update_heuristic_values(start, last_start,
#                 pellet_eaten, 
#                 ghost_nodes_past, 
#                 ghost_node_current, 
#                 scores, 
#                 pellet_value, 
#                 ghost_constant):
#     """
#     Inputs:
#         Pellet_eaten Node (x,y) of parent that has been eaten. None if nothing has been eaten
#         ghost_nodes_past, List of ghosts and their location Node, none if ghosts are not on grid
#             If any of the ghosts are None just reevaluate ngl
#         Scores: Dicts of Nodes and corresponding scores
#         Pellet_Value: Value of having a pellet so we can subtract
#     Returns: Updated Scores for each node

#     THESE JUST RETURN THE HEURISTIC VALUE
#     """

#     if pellet_eaten is not None:
#         scores[pellet_eaten] -= 10
#     #figure out where each ghot has gone
        



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
    max_val = np.inf
    max_node = visited[0]
    for node in visited:
        val = scores[node]
        if val < max_val:
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
