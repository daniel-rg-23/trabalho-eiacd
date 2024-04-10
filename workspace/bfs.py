from collections import deque

class Graph:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.visited = set()

    def bfs_shortest_path(self, start, end):
        queue = deque([(start, [])])  # Initialize queue with starting position and empty path

        while queue:
            current_pos, path = queue.popleft()
            row, col = current_pos

            if current_pos == end:
                return path  # Return the shortest path when the destination is reached

            if current_pos not in self.visited:
                self.visited.add(current_pos)

                # Check neighboring positions (up, down, left, right)
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_row, new_col = row + dr, col + dc

                    # Check if new position is within bounds and not a block
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.board[new_row][new_col] != 1:
                        queue.append(((new_row, new_col), path + [(new_row, new_col)]))  # Add new position to queue with updated path

        return None  # If path doesn't exist

# Define the matrix
matrix = [
    [1, 0, 0, 0],
    [3, 0, 1, 0],
    [3, 2, 0, 2],
    [0, 1, 1, 0]
]

# Define the starting and ending positions
start_pos = None
end_pos = None
for i, row in enumerate(matrix):
    for j, value in enumerate(row):
        if value == 2:
            start_pos = (i, j)
        elif value == 3:
            end_pos = (i, j)

# Create a Graph object and find the shortest path
graph = Graph(matrix)

# Measure the execution time
start_time = time.time()

shortest_path = graph.bfs_shortest_path(start_pos, end_pos)

end_time = time.time()

if shortest_path:
    print("Shortest path:", shortest_path)
else:
    print("Path doesn't exist.")
