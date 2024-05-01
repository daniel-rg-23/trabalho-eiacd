# Create an instance of the Algorithm class and test the search methods
#algorithm = Algorithm(initial_state, goal_state_func, operators_func)

#result_node = algorithm.breadth_first_search()
#result_node = algorithm.depth_first_search()
#result_node = algorithm.depth_limited_search(depth_limit=10)
#result_node = algorithm.iterative_deepening(depth_limit=10)
#result_node = algorithm.greedy_search(heuristic_func=Algorithm.manhattan_distance)
#result_node = algorithm.a_star_search(goal_state_func=goal_state_func, cost_func=Algorithm.cost_func, successors_func=operators_func)
#result_node = algorithm.weighted_a_star_search(goal_state_func=goal_state_func,heuristic_func=Algorithm.manhattan_distance,cost_func=Algorithm.cost_func,successors_func=operators_func,weight=1.5)

class TreeNode:
    def __init__(self, state, parent=None, direction=None, heuristic=0, cost=0, g=0, h=0):
        self.state = state
        self.direction = direction
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
    def trace_path(node):
        path = []
        while node.parent:  # Check if node has a parent
            parent_state = node.parent.state
            child_state = node.state
            
            # Find the position of '2' in parent and child states
            parent_pos = [(i, j) for i, row in enumerate(parent_state) for j, val in enumerate(row) if val == 2]
            child_pos = [(i, j) for i, row in enumerate(child_state) for j, val in enumerate(row) if val == 2]
            
            print(f"Parent position: {parent_pos}, Child position: {child_pos}")
            
            # Calculate the difference between the positions to determine the move
            diff_row = child_pos[0][0] - parent_pos[0][0]
            diff_col = child_pos[0][1] - parent_pos[0][1]
            
            if diff_row == -1:  # '2' moved up
                path.append('up')
            elif diff_row == 1:  # '2' moved down
                path.append('down')
            elif diff_col == -1:  # '2' moved left
                path.append('left')
            elif diff_col == 1:  # '2' moved right
                path.append('right')
            
            node = node.parent  # Move to the parent node
        
        # Reverse the path to get the correct order
        path.reverse()
        
        return path


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
    
    def get_direction(self, state1, state2):
        if len(state1) != len(state2) or len(state1[0]) != len(state2[0]):
            raise ValueError("States have different dimensions")

        diff = [[state2[i][j] - state1[i][j] for j in range(len(state1[0]))] for i in range(len(state1))]
        
        rows, cols = len(state1), len(state1[0])
        
        # Check for a single difference in a row
        if diff[0].count(1) == 1 and diff[0].count(-1) == 0:
            return 'right'
        elif diff[0].count(-1) == 1 and diff[0].count(1) == 0:
            return 'left'
        
        # Check for a single difference in a column
        elif [diff[i][0] for i in range(rows)].count(1) == 1 and [diff[i][0] for i in range(rows)].count(-1) == 0:
            return 'down'
        elif [diff[i][0] for i in range(rows)].count(-1) == 1 and [diff[i][0] for i in range(rows)].count(1) == 0:
            return 'up'
        
        else:
            raise ValueError("Invalid move between states")


    
    def breadth_first_search(self):
        root_direction = None  # Start with no direction
        queue = deque([(self.initial_state, root_direction)])  # Queue stores tuples of (state, direction)
        
        visited = set()
        visited.add(tuple(map(tuple, self.initial_state)))  # Convert the initial state to a tuple and add to visited set

        max_depth = 50  # Set a maximum depth to prevent infinite loop
        depth = 0

        while queue and depth < max_depth:
            state, direction = queue.popleft()
            
            if self.goal_state_func(state):
                return direction  # Return the direction if the goal state is reached

            operator_results = self.operators_func(state)
            
            if isinstance(operator_results, bool):
                raise ValueError("operators_func returned a boolean value instead of a list of directions")

            if not hasattr(operator_results, '__iter__'):
                raise ValueError("operators_func returned a non-iterable value")

            for next_direction in operator_results:
                child_state = self.get_direction(state, next_direction)  # Apply direction to get the child state
                
                # Check if child state is valid
                if child_state is None:
                    continue
                    
                child_state_tuple = tuple(map(tuple, child_state))
                
                if child_state_tuple not in visited:
                    visited.add(child_state_tuple)
                    queue.append((child_state, next_direction))

            depth += 1

        return None  # Return None if no solution found within max_depth

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
    def cost_function(self, state, successor_state):
        # Find the position of the '1' and '2' tiles in the current state
        row1, col1 = self.find_tile_position(1)
        row2, col2 = self.find_tile_position(2)

        # Find the position of the '1' and '2' tiles in the successor state
        succ_row1, succ_col1 = self.find_tile_position(successor_state, 1)
        succ_row2, succ_col2 = self.find_tile_position(successor_state, 2)

        # Calculate the number of moves required to transition from the current state to the successor state
        moves = abs(row1 - succ_row1) + abs(col1 - succ_col1) + abs(row2 - succ_row2) + abs(col2 - succ_col2)

        return moves

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



# Create an instance of the Algorithm class and test the search methods
#algorithm = Algorithm(initial_state, goal_state_func, operators_func)

#result_node = algorithm.breadth_first_search()
#result_node = algorithm.depth_first_search()
#result_node = algorithm.depth_limited_search(depth_limit=10)
#result_node = algorithm.iterative_deepening(depth_limit=10)
#result_node = algorithm.greedy_search(heuristic_func=Algorithm.manhattan_distance)
#result_node = algorithm.a_star_search(goal_state_func=goal_state_func, cost_func=Algorithm.cost_func, successors_func=operators_func)
#result_node = algorithm.weighted_a_star_search(goal_state_func=goal_state_func,heuristic_func=Algorithm.manhattan_distance,cost_func=Algorithm.cost_func,successors_func=operators_func,weight=1.5)


