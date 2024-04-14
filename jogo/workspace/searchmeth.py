from collections import deque
import heapq
import copy
from level1 import *
# Define TreeNode classfrom collections import deque
import heapq
import copy
from level1 import *
# Define TreeNode class
class TreeNode:
    def __init__(self, state, parent=None, heuristic=0, cost=0, g=0, h=0):  # Modified the __init__ method
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost  # Added cost attribute
        self.g = g  # Added g attribute
        self.h = h  # Added h attribute
        self.children = []

    def __lt__(self, other):
        return self.cost < other.cost  # Compare using the cost attribute

# Define Algorithm class
class Algorithm:
    def __init__(self, initial_state, goal_state_func, operators_func):
        self.initial_state = initial_state
        self.goal_state_func = goal_state_func
        self.operators_func = operators_func

    @staticmethod
    def cost_func(current_state, successor_state):
        return 1

    @staticmethod
    def manhattan_distance(state):
        distance = 0
        for r, row in enumerate(state):
            for c, val in enumerate(row):
                if val == 2:
                    # Calculate Manhattan distance for the first '2' tile
                    distance += abs(r - 1) + abs(c - 0)
                    # Calculate Manhattan distance for the second '2' tile
                    distance += abs(r - 2) + abs(c - 0)
        return distance


    def breadth_first_search(self):
        root = TreeNode(self.initial_state)
        queue = deque([root])
        
        # Check the type of the initial state
        if not isinstance(self.initial_state, list) or not all(isinstance(row, list) for row in self.initial_state):
            raise ValueError("Initial state must be a list of lists.")
        
        visited = set([tuple(map(tuple, self.initial_state))])  # Convert the initial state to a tuple of tuples

        while queue:
            node = queue.popleft()

            if self.goal_state_func(node.state):
                return node

            for state in self.operators_func(node.state):
                # Ensure state is a list of lists
                if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                    raise ValueError("State must be a list of lists.")
                
                state_tuple = tuple(map(tuple, state))  # Convert the state to a tuple of tuples
                
                if state_tuple not in visited:
                    visited.add(state_tuple)  # Add the state tuple to the visited set
                    child_node = TreeNode(state=state, parent=node)
                    node.children.append(child_node)  # Append the child_node to node's children
                    queue.append(child_node)

        return None

    def depth_first_search(self):
        root = TreeNode(self.initial_state)
        stack = deque([root])
        visited = set([tuple(map(tuple, self.initial_state))])

        while stack:
            node = stack.pop()

            if self.goal_state_func(node.state):
                return node

            for state in self.operators_func(node.state):
                if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                    raise ValueError("State must be a list of lists.")
                
                state_tuple = tuple(map(tuple, state))
                
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node)
                    node.children.append(child_node)
                    stack.append(child_node)
        return None

    def depth_limited_search(self, depth_limit):
        def sub_dls(node, depth, visited):
            if self.goal_state_func(node.state):
                return node
            if depth == depth_limit:
                return None

            for state in self.operators_func(node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node)
                    result = sub_dls(child_node, depth + 1, visited)
                    if result:
                        return result
            return None

        visited = set([tuple(map(tuple, self.initial_state))])
        return sub_dls(TreeNode(self.initial_state), 0, visited)

    def iterative_deepening(self, depth_limit):
        for depth in range(depth_limit):
            result = self.depth_limited_search(depth)
            if result:
                return result
        return None

    def greedy_search(self, heuristic_func):
        open_list = []
        initial_node = TreeNode(self.initial_state, heuristic=heuristic_func(self.initial_state))
        heapq.heappush(open_list, initial_node)
        
        visited = set([tuple(map(tuple, self.initial_state))])

        while open_list:
            current_node = heapq.heappop(open_list)

            if self.goal_state_func(current_node.state):
                return current_node  

            visited.add(tuple(map(tuple, current_node.state)))

            for state in self.operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    successor_node = TreeNode(state, current_node, heuristic_func(state))
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None
    
    def a_star_search(self, goal_state_func, cost_func, successors_func):
        open_list = []
        initial_node = TreeNode(self.initial_state, g=0, h=self.manhattan_distance(self.initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(tuple(map(tuple, current_node.state)))  # Convert list to tuple and add to closed_list

            for successor in successors_func(current_node.state):
                successor_tuple = tuple(map(tuple, successor))  # Convert list to tuple
                if successor_tuple not in closed_list:
                    g_value = current_node.cost + cost_func(current_node.state, successor)
                    h_value = self.manhattan_distance(successor)
                    successor_node = TreeNode(successor, parent=current_node, cost=g_value + h_value)
                    heapq.heappush(open_list, successor_node)

        return None


    def weighted_a_star_search(self, goal_state_func, heuristic_func, cost_func, successors_func, weight):
        open_list = []
        initial_node = TreeNode(self.initial_state, g=0, h=Algorithm.manhattan_distance(self.initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(tuple(map(tuple, current_node.state)))  # Convert list to tuple and add to closed_list

            for successor in successors_func(current_node.state):
                successor_tuple = tuple(map(tuple, successor))  # Convert list to tuple
                if successor_tuple not in closed_list:
                    g_value = current_node.g + cost_func(current_node.state, successor)
                    h_value = weight * heuristic_func(successor)  # Apply weight to the heuristic value
                    successor_node = TreeNode(successor, parent=current_node, g=g_value, h=h_value)
                    heapq.heappush(open_list, successor_node)

        return None




def goal_state_func(state):
    return state[1][0] == 2 and state[2][0] == 2

def move_tile(state, direction, row1, col1, row2, col2):
    new_state = copy.deepcopy(state)
    moved = False

    if direction == 'up':
        # Move tile from (row1, col1) upwards
        while row1 > 0 and new_state[row1 - 1][col1] != 1:
            new_state[row1][col1], new_state[row1 - 1][col1] = new_state[row1 - 1][col1], new_state[row1][col1]
            if (row1 - 1, col1) not in initial_threes:
                new_state[row1][col1] = 0
            row1 -= 1
            moved = True

        # Move tile from (row2, col2) upwards
        while row2 > 0 and new_state[row2 - 1][col2] != 1:
            new_state[row2][col2], new_state[row2 - 1][col2] = new_state[row2 - 1][col2], new_state[row2][col2]
            if (row2 - 1, col2) not in initial_threes:
                new_state[row2][col2] = 0
            row2 -= 1
            moved = True

    elif direction == 'down':
        # Move tile from (row1, col1) downwards
        while row1 < len(state) - 1 and new_state[row1 + 1][col1] != 1:
            new_state[row1][col1], new_state[row1 + 1][col1] = new_state[row1 + 1][col1], new_state[row1][col1]
            if (row1 + 1, col1) not in initial_threes:
                new_state[row1][col1] = 0
            row1 += 1
            moved = True

        # Move tile from (row2, col2) downwards
        while row2 < len(state) - 1 and new_state[row2 + 1][col2] != 1:
            new_state[row2][col2], new_state[row2 + 1][col2] = new_state[row2 + 1][col2], new_state[row2][col2]
            if (row2 + 1, col2) not in initial_threes:
                new_state[row2][col2] = 0
            row2 += 1
            moved = True

    elif direction == 'left':
        # Move tile from (row1, col1) leftwards
        while col1 > 0 and new_state[row1][col1 - 1] != 1:
            new_state[row1][col1], new_state[row1][col1 - 1] = new_state[row1][col1 - 1], new_state[row1][col1]
            if (row1, col1 - 1) not in initial_threes:
                new_state[row1][col1] = 0
            col1 -= 1
            moved = True

        # Move tile from (row2, col2) leftwards
        while col2 > 0 and new_state[row2][col2 - 1] != 1:
            new_state[row2][col2], new_state[row2][col2 - 1] = new_state[row2][col2 - 1], new_state[row2][col2]
            if (row2, col2 - 1) not in initial_threes:
                new_state[row2][col2] = 0
            col2 -= 1
            moved = True

    elif direction == 'right':
        # Move tile from (row1, col1) rightwards
        while col1 < len(state[0]) - 1 and new_state[row1][col1 + 1] != 1:
            new_state[row1][col1], new_state[row1][col1 + 1] = new_state[row1][col1 + 1], new_state[row1][col1]
            if (row1, col1 + 1) not in initial_threes:
                new_state[row1][col1] = 0
            col1 += 1
            moved = True

        # Move tile from (row2, col2) rightwards
        while col2 < len(state[0]) - 1 and new_state[row2][col2 + 1] != 1:
            new_state[row2][col2], new_state[row2][col2 + 1] = new_state[row2][col2 + 1], new_state[row2][col2]
            if (row2, col2 + 1) not in initial_threes:
                new_state[row2][col2] = 0
            col2 += 1
            moved = True

    if moved:
        for r, c in initial_threes:
            if new_state[r][c] != 2:  # If '2' is not over '3', make '3' appear
                new_state[r][c] = 3
        for r, c in [(r, c) for r in range(len(state)) for c in range(len(state[0])) if (r, c) not in initial_threes and new_state[r][c] == 3]:
            new_state[r][c] = 0

    return new_state



def operators_func(state):
    successors = []  # List to store successor states

    # Find the position of the '2' tiles
    for row1 in range(len(state)):
        for col1 in range(len(state[0])):
            if state[row1][col1] == 2:
                for row2 in range(row1, len(state)):
                    for col2 in range(len(state[0])):
                        if state[row2][col2] == 2 and (row1 != row2 or col1 != col2):

                            # Try moving the tile in each direction and add the resulting state to the successors list
                            new_state_up = move_tile(state, 'up', row1, col1, row2, col2)
                            new_state_down = move_tile(state, 'down', row1, col1, row2, col2)
                            new_state_left = move_tile(state, 'left', row1, col1, row2, col2)
                            new_state_right = move_tile(state, 'right', row1, col1, row2, col2)

                            # Add only the valid new states to the successors list
                            if new_state_up and new_state_up not in successors:
                                successors.append(new_state_up)

                            if new_state_down and new_state_down not in successors:
                                successors.append(new_state_down)

                            if new_state_left and new_state_left not in successors:
                                successors.append(new_state_left)

                            if new_state_right and new_state_right not in successors:
                                successors.append(new_state_right)
                                

    return successors


def trace_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return reversed(path)


# Create an instance of the Algorithm class and test the search methods
algorithm = Algorithm(initial_state, goal_state_func, operators_func)

result_node = algorithm.breadth_first_search()
#result_node = algorithm.depth_first_search()
#result_node = algorithm.depth_limited_search(depth_limit=10)
#result_node = algorithm.iterative_deepening(depth_limit=10)
#result_node = algorithm.greedy_search(heuristic_func=Algorithm.manhattan_distance)
#result_node = algorithm.a_star_search(goal_state_func=goal_state_func, cost_func=Algorithm.cost_func, successors_func=operators_func)
#result_node = algorithm.weighted_a_star_search(goal_state_func=goal_state_func,heuristic_func=Algorithm.manhattan_distance,cost_func=Algorithm.cost_func,successors_func=operators_func,weight=1.5)


if result_node:
    path = trace_path(result_node)
    for idx, state in enumerate(path):
        print(f"Step {idx + 1}:")
        for row in state:
            print(row)
else:
    print("No solution found.")
class TreeNode:
    def __init__(self, state, parent=None, heuristic=0, cost=0, g=0, h=0):  # Modified the __init__ method
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost  # Added cost attribute
        self.g = g  # Added g attribute
        self.h = h  # Added h attribute
        self.children = []

    def __lt__(self, other):
        return self.cost < other.cost  # Compare using the cost attribute

# Define Algorithm class
class Algorithm:
    def __init__(self, initial_state, goal_state_func, operators_func):
        self.initial_state = initial_state
        self.goal_state_func = goal_state_func
        self.operators_func = operators_func

    @staticmethod
    def cost_func(current_state, successor_state):
        return 1

    @staticmethod
    def manhattan_distance(state):
        distance = 0
        for r, row in enumerate(state):
            for c, val in enumerate(row):
                if val == 2:
                    # Calculate Manhattan distance for the first '2' tile
                    distance += abs(r - 1) + abs(c - 0)
                    # Calculate Manhattan distance for the second '2' tile
                    distance += abs(r - 2) + abs(c - 0)
        return distance


    def breadth_first_search(self):
        root = TreeNode(self.initial_state)
        queue = deque([root])
        
        # Check the type of the initial state
        if not isinstance(self.initial_state, list) or not all(isinstance(row, list) for row in self.initial_state):
            raise ValueError("Initial state must be a list of lists.")
        
        visited = set([tuple(map(tuple, self.initial_state))])  # Convert the initial state to a tuple of tuples

        while queue:
            node = queue.popleft()

            if self.goal_state_func(node.state):
                return node

            for state in self.operators_func(node.state):
                # Ensure state is a list of lists
                if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                    raise ValueError("State must be a list of lists.")
                
                state_tuple = tuple(map(tuple, state))  # Convert the state to a tuple of tuples
                
                if state_tuple not in visited:
                    visited.add(state_tuple)  # Add the state tuple to the visited set
                    child_node = TreeNode(state=state, parent=node)
                    node.children.append(child_node)  # Append the child_node to node's children
                    queue.append(child_node)

        return None

    def depth_first_search(self):
        root = TreeNode(self.initial_state)
        stack = deque([root])
        visited = set([tuple(map(tuple, self.initial_state))])

        while stack:
            node = stack.pop()

            if self.goal_state_func(node.state):
                return node

            for state in self.operators_func(node.state):
                if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                    raise ValueError("State must be a list of lists.")
                
                state_tuple = tuple(map(tuple, state))
                
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node)
                    node.children.append(child_node)
                    stack.append(child_node)
        return None

    def depth_limited_search(self, depth_limit):
        def sub_dls(node, depth, visited):
            if self.goal_state_func(node.state):
                return node
            if depth == depth_limit:
                return None

            for state in self.operators_func(node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node)
                    result = sub_dls(child_node, depth + 1, visited)
                    if result:
                        return result
            return None

        visited = set([tuple(map(tuple, self.initial_state))])
        return sub_dls(TreeNode(self.initial_state), 0, visited)

    def iterative_deepening(self, depth_limit):
        for depth in range(depth_limit):
            result = self.depth_limited_search(depth)
            if result:
                return result
        return None

    def greedy_search(self, heuristic_func):
        open_list = []
        initial_node = TreeNode(self.initial_state, heuristic=heuristic_func(self.initial_state))
        heapq.heappush(open_list, initial_node)
        
        visited = set([tuple(map(tuple, self.initial_state))])

        while open_list:
            current_node = heapq.heappop(open_list)

            if self.goal_state_func(current_node.state):
                return current_node  

            visited.add(tuple(map(tuple, current_node.state)))

            for state in self.operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    successor_node = TreeNode(state, current_node, heuristic_func(state))
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None
    
    def a_star_search(self, goal_state_func, cost_func, successors_func):
        open_list = []
        initial_node = TreeNode(self.initial_state, g=0, h=self.manhattan_distance(self.initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(tuple(map(tuple, current_node.state)))  # Convert list to tuple and add to closed_list

            for successor in successors_func(current_node.state):
                successor_tuple = tuple(map(tuple, successor))  # Convert list to tuple
                if successor_tuple not in closed_list:
                    g_value = current_node.cost + cost_func(current_node.state, successor)
                    h_value = self.manhattan_distance(successor)
                    successor_node = TreeNode(successor, parent=current_node, cost=g_value + h_value)
                    heapq.heappush(open_list, successor_node)

        return None


    def weighted_a_star_search(self, goal_state_func, heuristic_func, cost_func, successors_func, weight):
        open_list = []
        initial_node = TreeNode(self.initial_state, g=0, h=Algorithm.manhattan_distance(self.initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(tuple(map(tuple, current_node.state)))  # Convert list to tuple and add to closed_list

            for successor in successors_func(current_node.state):
                successor_tuple = tuple(map(tuple, successor))  # Convert list to tuple
                if successor_tuple not in closed_list:
                    g_value = current_node.g + cost_func(current_node.state, successor)
                    h_value = weight * heuristic_func(successor)  # Apply weight to the heuristic value
                    successor_node = TreeNode(successor, parent=current_node, g=g_value, h=h_value)
                    heapq.heappush(open_list, successor_node)

        return None




def goal_state_func(state):
    return state[1][0] == 2 and state[2][0] == 2

def move_tile(state, direction, row1, col1, row2, col2):
    new_state = copy.deepcopy(state)
    moved = False

    if direction == 'up':
        # Move tile from (row1, col1) upwards
        while row1 > 0 and new_state[row1 - 1][col1] != 1:
            new_state[row1][col1], new_state[row1 - 1][col1] = new_state[row1 - 1][col1], new_state[row1][col1]
            if (row1 - 1, col1) not in initial_threes:
                new_state[row1][col1] = 0
            row1 -= 1
            moved = True

        # Move tile from (row2, col2) upwards
        while row2 > 0 and new_state[row2 - 1][col2] != 1:
            new_state[row2][col2], new_state[row2 - 1][col2] = new_state[row2 - 1][col2], new_state[row2][col2]
            if (row2 - 1, col2) not in initial_threes:
                new_state[row2][col2] = 0
            row2 -= 1
            moved = True

    elif direction == 'down':
        # Move tile from (row1, col1) downwards
        while row1 < len(state) - 1 and new_state[row1 + 1][col1] != 1:
            new_state[row1][col1], new_state[row1 + 1][col1] = new_state[row1 + 1][col1], new_state[row1][col1]
            if (row1 + 1, col1) not in initial_threes:
                new_state[row1][col1] = 0
            row1 += 1
            moved = True

        # Move tile from (row2, col2) downwards
        while row2 < len(state) - 1 and new_state[row2 + 1][col2] != 1:
            new_state[row2][col2], new_state[row2 + 1][col2] = new_state[row2 + 1][col2], new_state[row2][col2]
            if (row2 + 1, col2) not in initial_threes:
                new_state[row2][col2] = 0
            row2 += 1
            moved = True

    elif direction == 'left':
        # Move tile from (row1, col1) leftwards
        while col1 > 0 and new_state[row1][col1 - 1] != 1:
            new_state[row1][col1], new_state[row1][col1 - 1] = new_state[row1][col1 - 1], new_state[row1][col1]
            if (row1, col1 - 1) not in initial_threes:
                new_state[row1][col1] = 0
            col1 -= 1
            moved = True

        # Move tile from (row2, col2) leftwards
        while col2 > 0 and new_state[row2][col2 - 1] != 1:
            new_state[row2][col2], new_state[row2][col2 - 1] = new_state[row2][col2 - 1], new_state[row2][col2]
            if (row2, col2 - 1) not in initial_threes:
                new_state[row2][col2] = 0
            col2 -= 1
            moved = True

    elif direction == 'right':
        # Move tile from (row1, col1) rightwards
        while col1 < len(state[0]) - 1 and new_state[row1][col1 + 1] != 1:
            new_state[row1][col1], new_state[row1][col1 + 1] = new_state[row1][col1 + 1], new_state[row1][col1]
            if (row1, col1 + 1) not in initial_threes:
                new_state[row1][col1] = 0
            col1 += 1
            moved = True

        # Move tile from (row2, col2) rightwards
        while col2 < len(state[0]) - 1 and new_state[row2][col2 + 1] != 1:
            new_state[row2][col2], new_state[row2][col2 + 1] = new_state[row2][col2 + 1], new_state[row2][col2]
            if (row2, col2 + 1) not in initial_threes:
                new_state[row2][col2] = 0
            col2 += 1
            moved = True

    if moved:
        for r, c in initial_threes:
            if new_state[r][c] != 2:  # If '2' is not over '3', make '3' appear
                new_state[r][c] = 3
        for r, c in [(r, c) for r in range(len(state)) for c in range(len(state[0])) if (r, c) not in initial_threes and new_state[r][c] == 3]:
            new_state[r][c] = 0

    return new_state



def operators_func(state):
    successors = []  # List to store successor states

    # Find the position of the '2' tiles
    for row1 in range(len(state)):
        for col1 in range(len(state[0])):
            if state[row1][col1] == 2:
                for row2 in range(row1, len(state)):
                    for col2 in range(len(state[0])):
                        if state[row2][col2] == 2 and (row1 != row2 or col1 != col2):

                            # Try moving the tile in each direction and add the resulting state to the successors list
                            new_state_up = move_tile(state, 'up', row1, col1, row2, col2)
                            new_state_down = move_tile(state, 'down', row1, col1, row2, col2)
                            new_state_left = move_tile(state, 'left', row1, col1, row2, col2)
                            new_state_right = move_tile(state, 'right', row1, col1, row2, col2)

                            # Add only the valid new states to the successors list
                            if new_state_up and new_state_up not in successors:
                                successors.append(new_state_up)

                            if new_state_down and new_state_down not in successors:
                                successors.append(new_state_down)

                            if new_state_left and new_state_left not in successors:
                                successors.append(new_state_left)

                            if new_state_right and new_state_right not in successors:
                                successors.append(new_state_right)
                                

    return successors


def trace_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return reversed(path)


# Create an instance of the Algorithm class and test the search methods
algorithm = Algorithm(initial_state, goal_state_func, operators_func)

result_node = algorithm.breadth_first_search()
#result_node = algorithm.depth_first_search()
#result_node = algorithm.depth_limited_search(depth_limit=10)
#result_node = algorithm.iterative_deepening(depth_limit=10)
#result_node = algorithm.greedy_search(heuristic_func=Algorithm.manhattan_distance)
#result_node = algorithm.a_star_search(goal_state_func=goal_state_func, cost_func=Algorithm.cost_func, successors_func=operators_func)
#result_node = algorithm.weighted_a_star_search(goal_state_func=goal_state_func,heuristic_func=Algorithm.manhattan_distance,cost_func=Algorithm.cost_func,successors_func=operators_func,weight=1.5)


if result_node:
    path = trace_path(result_node)
    for idx, state in enumerate(path):
        print(f"Step {idx + 1}:")
        for row in state:
            print(row)
else:
    print("No solution found.")
