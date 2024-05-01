from collections import deque
import copy
import heapq

GAME_SIZE = 4

class TreeNode:
    def __init__(self, state, parent=None, direction=None, heuristic=0, cost=0, g=0, h=0):
        self.state = state
        self.direction = direction
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost
        self.g = g
        self.h = h
        self.children = []

    def __lt__(self, other):
        return self.cost < other.cost

class PuzzleSolver:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.initial_threes = self.find_threes(initial_state)
        self.MATCH_TILES=[(3,3),(0,2)]
        
    def find_threes(self, matrix):
        threes = []
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if val == 3:
                    threes.append((i, j))
        return threes

    def goal_state_func(self, state):
        i=self.MATCH_TILES[0][0]
        j=self.MATCH_TILES[0][1]
        k=self.MATCH_TILES[1][0]
        l=self.MATCH_TILES[1][1]
        return state[j][i] == 2 and state[l][k] == 2

    def move_tile1(self, state, direction, row1, col1, row2, col2):
        new_state = copy.deepcopy(state)

        if direction == 'up':
            while row1 > 0 and new_state[row1 - 1][col1] != 1:
                new_state[row1][col1], new_state[row1 - 1][col1] = new_state[row1 - 1][col1], new_state[row1][col1]
                if (row1 - 1, col1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                row1 -= 1

            while row2 > 0 and new_state[row2 - 1][col2] != 1:
                new_state[row2][col2], new_state[row2 - 1][col2] = new_state[row2 - 1][col2], new_state[row2][col2]
                if (row2 - 1, col2) not in self.initial_threes:
                    new_state[row2][col2] = 0
                row2 -= 1

        elif direction == 'down':
            while row1 < GAME_SIZE - 1 and new_state[row1 + 1][col1] != 1:
                new_state[row1][col1], new_state[row1 + 1][col1] = new_state[row1 + 1][col1], new_state[row1][col1]
                if (row1 + 1, col1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                row1 += 1

            while row2 < GAME_SIZE - 1 and new_state[row2 + 1][col2] != 1:
                new_state[row2][col2], new_state[row2 + 1][col2] = new_state[row2 + 1][col2], new_state[row2][col2]
                if (row2 + 1, col2) not in self.initial_threes:
                    new_state[row2][col2] = 0
                row2 += 1

        elif direction == 'left':
            while col1 > 0 and new_state[row1][col1 - 1] != 1:
                new_state[row1][col1], new_state[row1][col1 - 1] = new_state[row1][col1 - 1], new_state[row1][col1]
                if (row1, col1 - 1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                col1 -= 1

            while col2 > 0 and new_state[row2][col2 - 1] != 1:
                new_state[row2][col2], new_state[row2][col2 - 1] = new_state[row2][col2 - 1], new_state[row2][col2]
                if (row2, col2 - 1) not in self.initial_threes:
                    new_state[row2][col2] = 0
                col2 -= 1

        elif direction == 'right':
            while col1 < GAME_SIZE - 1 and new_state[row1][col1 + 1] != 1:
                new_state[row1][col1], new_state[row1][col1 + 1] = new_state[row1][col1 + 1], new_state[row1][col1]
                if (row1, col1 + 1) not in self.initial_threes:
                    new_state[row1][col1] = 0
                col1 += 1

            while col2 < GAME_SIZE - 1 and new_state[row2][col2 + 1] != 1:
                new_state[row2][col2], new_state[row2][col2 + 1] = new_state[row2][col2 + 1], new_state[row2][col2]
                if (row2, col2 + 1) not in self.initial_threes:
                    new_state[row2][col2] = 0
                col2 += 1

        return new_state

    def operators_func(self, state):
        successors = []

        for row1 in range(len(state)):
            for col1 in range(len(state[0])):
                if state[row1][col1] == 2:
                    for row2 in range(len(state)):
                        for col2 in range(len(state[0])):
                            if state[row2][col2] == 2 and (row1 != row2 or col1 != col2):
                                new_state_up = self.move_tile1(state, 'up', row1, col1, row2, col2)
                                new_state_down = self.move_tile1(state, 'down', row1, col1, row2, col2)
                                new_state_left = self.move_tile1(state, 'left', row1, col1, row2, col2)
                                new_state_right = self.move_tile1(state, 'right', row1, col1, row2, col2)

                                if new_state_up and new_state_up != state:
                                    successors.append((new_state_up, 'up'))

                                if new_state_down and new_state_down != state:
                                    successors.append((new_state_down, 'down'))

                                if new_state_left and new_state_left != state:
                                    successors.append((new_state_left, 'left'))

                                if new_state_right and new_state_right != state:
                                    successors.append((new_state_right, 'right'))
        print (successors)
        return successors



    def breadth_first_search(self):
            root = TreeNode(self.initial_state)
            queue = deque([root])

            if not isinstance(self.initial_state, list) or not all(isinstance(row, list) for row in self.initial_state):
                raise ValueError("Initial state must be a list of lists.")

            visited = set([tuple(map(tuple, self.initial_state))])

            while queue:
                node = queue.popleft()

                if self.goal_state_func(node.state):
                    return node

                for state, direction in self.operators_func(node.state):
                    if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                        raise ValueError("State must be a list of lists.")
                    
                    state_tuple = tuple(map(tuple, state))
                    
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        child_node = TreeNode(state=state, parent=node, direction=direction)
                        node.children.append(child_node)
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

            for state, direction in self.operators_func(node.state):
                if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
                    raise ValueError("State must be a list of lists.")
                
                state_tuple = tuple(map(tuple, state))
                
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node, direction=direction)
                    node.children.append(child_node)
                    stack.append(child_node)
        return None

    def depth_limited_search(self, depth_limit):
        def sub_dls(node, depth, visited):
            if self.goal_state_func(node.state):
                return node
            if depth == depth_limit:
                return None

            for state, direction in self.operators_func(node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    child_node = TreeNode(state=state, parent=node, direction=direction)
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

            for state, direction in self.operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    successor_node = TreeNode(state, current_node, direction, heuristic=heuristic_func(state))
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None
    
    def cost_function(self, node, w=1):
        return node.g + w * self.manhattan_distance(node.state)


    def a_star_search(self, goal_test_func, cost_func, operators_func):
        return self.weighted_a_star_search(goal_test_func, cost_func, operators_func, w=1)

    def weighted_a_star_search(self, goal_test_func, cost_func, operators_func, w=1):
        open_list = []
        initial_node = TreeNode(
            self.initial_state,
            heuristic=self.manhattan_distance(self.initial_state),
            g=0,
            h=self.manhattan_distance(self.initial_state),
            cost=self.cost_function(TreeNode(self.initial_state), w)
        )
        heapq.heappush(open_list, initial_node)

        visited = set([tuple(map(tuple, self.initial_state))])

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_test_func(current_node.state):
                return current_node

            visited.add(tuple(map(tuple, current_node.state)))

            for state, direction in operators_func(current_node.state):
                state_tuple = tuple(map(tuple, state))
                if state_tuple not in visited:
                    g = current_node.g + 1  # Assuming each move has a cost of 1
                    h = self.manhattan_distance(state)
                    successor_node = TreeNode(
                        state,
                        parent=current_node,
                        direction=direction,
                        heuristic=h,
                        g=g,
                        h=h
                    )
                    successor_node.cost = cost_func(successor_node, w)
                    heapq.heappush(open_list, successor_node)
                    visited.add(state_tuple)

        return None

    def retrieve_path(self, node):
        path = []
        while node:
            if node.direction:
                path.append(node.direction)
            node = node.parent
        return path[::-1] if path else ["No path found"]


initial_state = [
    [1, 1, 0, 1],
    [0, 1, 0, 2],
    [3, 1, 2, 1],
    [0, 0, 0, 3]
]


solver = PuzzleSolver(initial_state) 
goal_node = solver.breadth_first_search()
#goal_node = solver.depth_first_search()
#goal_node = solver.depth_limited_search(depth_limit=5)
#goal_node = solver.iterative_deepening(depth_limit=10)
#goal_node = solver.greedy_search(PuzzleSolver.manhattan_distance)
#goal_node = solver.a_star_search(solver.goal_state_func, solver.cost_function, solver.operators_func)
#goal_node = solver.weighted_a_star_search(solver.goal_state_func, solver.cost_function, solver.operators_func,w=2)
result_directions = solver.retrieve_path(goal_node)
print( result_directions)


