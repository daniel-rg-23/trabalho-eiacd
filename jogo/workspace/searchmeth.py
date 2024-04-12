from collections import deque
import heapq

class TreeNode:
    def __init__(self, state, parent=None, heuristic= 0):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.children = []
        
    def __lt__(self, other):
        return self.cost < other.cost    

    def add_child(self, child):
        self.children.append(child)

class Algorithm:
    def __init__(self, initial_state, goal_state_func, operators_func):
        self.initial_state = initial_state
        self.goal_state_func = goal_state_func
        self.operators_func = operators_func

    def breadth_first_search(initial_state, goal_state_func, operators_func):
        root = TreeNode(self.initial_state)
        queue = deque([root])
        visited = set([self.initial_state])

        while queue:
            node = queue.popleft()

            if self.goal_state_func(node.state):
                return node

            for state in self.operators_func(node.state):
                if state not in visited:
                    visited.add(state)
                    child_node = TreeNode(state=state, parent=node)
                    node.add_child(child_node)
                    queue.append(child_node)
        return None 


#def goal_state_func(state): implement for each level
    #pass

# A função operators_func() gera todos os possíveis estados sucessores de um estado dado.
#def operators_func(state):
    # Implemente a lógica para gerar novos estados a partir do estado atual.
 #   pass
    def depth_first_search(initial_state, goal_state_func, operators_func):
        root = TreeNode(self.initial_state)
        queue = deque([root])
        visited = set([self.initial_state])
        
        while queue:
            node= queue.pop()
            if goal_state_func(node.state): #checks the goal state
                return node
            
            node_queue= deque()
            for state in operators_func(node.state):
                if state not in visited:
                    child_node = TreeNode(state= state, parent= node)
                    node.add_child(child_node)
                    node_queue.appendleft(child_node)
                    visited.add(state)
            queue += node_queue
        return None
    
    def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
        root= TreeNode(initial_state)
        visited= set([initial_state])
    
        def sub_dfs(node, depth):
            if goal_state_func(node.state):
               return node
            if depth==depth_limit:
              return None
            for state in operators_func(node.state):
              child_node = TreeNode(state= state, parent= node)
              result = sub_dfs(child_node, depth + 1)
              if result is not None:
                 return result
        return sub_dfs(Treenode(initial_state),0)

    def iterative_deepening(initial_state, goal_state_func, operators_func, depth_limit):
        for depth in range(depth_limit):
            result= depth_limited_search(initial_state, goal_state_func, operators_func, depth)
            if result is not None:
                return result

    def greedy_search(initial_state, goal_state_func, heuristic_func, successors_func):
        open_list = []
        initial_node = TreeNode(initial_state, heuristic=heuristic_func(initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
               return current_node  

            closed_list.add(current_node.state)

            for successor in successors_func(current_node.state):
               if successor not in closed_list:
                 successor_node = TreeNode(successor, current_node, heuristic_func(successor))
                 heapq.heappush(open_list, successor_node)

        return None  # If the open_list is empty and goal was not found

    def a_star_search(initial_state, goal_state_func, heuristic_func, cost_func, successors_func):
        open_list = []
        initial_node = TreeNode(initial_state, g=0, h=heuristic_func(initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(current_node.state)

            for successor in successors_func(current_node.state):
                if successor not in closed_list:
                    g_value = current_node.g + cost_func(current_node.state, successor)
                    h_value = heuristic_func(successor)
                    successor_node = TreeNode(successor, parent=current_node, g=g_value, h=h_value)
                    heapq.heappush(open_list, successor_node)

        return None 

    def weighted_a_star_search(initial_state, goal_state_func, heuristic_func, cost_func, successors_func, weight):
        open_list = []
        initial_node = TreeNode(initial_state, g=0, h=heuristic_func(initial_state))
        heapq.heappush(open_list, initial_node)

        closed_list = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if goal_state_func(current_node.state):
                return current_node  

            closed_list.add(current_node.state)

            for successor in successors_func(current_node.state):
                if successor not in closed_list:
                    g_value = current_node.g + cost_func(current_node.state, successor)
                    h_value = weight * heuristic_func(successor)  # Apply weight to the heuristic value
                    successor_node = TreeNode(successor, parent=current_node, g=g_value, h=h_value)
                    heapq.heappush(open_list, successor_node)

        return None

#acho melhor se usarmos o weight de 1 assim como o custo de cada movimento, entao para chamar pomos o valor tipo:
#result = weighted_a_star_search(initial_state, goal_state_func, heuristic_func, cost_func, successors_func, weight=1)

    
    def cost_func(current_state, successor_state):
        return 1
        

