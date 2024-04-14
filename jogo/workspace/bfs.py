from collections import deque

class Graph:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def bfs_shortest_path(self, start1, start2, end1, end2):
        queue = deque([(start1, start2, [])])  # Initialize queue with starting positions and empty path
        visited = set()

        while queue:
            current_pos1, current_pos2, path = queue.popleft()
            row1, col1 = current_pos1
            row2, col2 = current_pos2

            if current_pos1 == end1 and current_pos2 == end2:
                return path  # Return the shortest path when both movable tiles reach their respective targets

            if (current_pos1, current_pos2) not in visited:
                visited.add((current_pos1, current_pos2))

                # Check neighboring positions for both movable tiles (up, down, left, right)
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_row1, new_col1 = row1 + dr, col1 + dc
                    new_row2, new_col2 = row2 + dr, col2 + dc

                    # Check if new positions are within bounds and not a block
                    if (0 <= new_row1 < self.rows and 0 <= new_col1 < self.cols and 
                        0 <= new_row2 < self.rows and 0 <= new_col2 < self.cols and
                        self.board[new_row1][new_col1] != 1 and self.board[new_row2][new_col2] != 1):
                        queue.append(((new_row1, new_col1), (new_row2, new_col2), path + [(new_row1, new_col1), (new_row2, new_col2)]))  # Add new positions to queue with updated path

        return None  # If path doesn't exist

# Define the board
board = [
    [1, 0, 0, 0],
    [3, 0, 1, 0],
    [3, 2, 0, 2],
    [0, 1, 1, 0]
]

# Define the starting and ending positions for both movable tiles and targets
start_pos1 = None
start_pos2 = None
end_pos1 = None
end_pos2 = None

for i, row in enumerate(board):
    for j, value in enumerate(row):
        if value == 2:
            if start_pos1 is None:
                start_pos1 = (i, j)
            else:
                start_pos2 = (i, j)
        elif value == 3:
            if end_pos1 is None:
                end_pos1 = (i, j)
            else:
                end_pos2 = (i, j)

# Create a Graph object and find the shortest path
graph = Graph(board)

shortest_path = graph.bfs_shortest_path(start_pos1, start_pos2, end_pos1, end_pos2)

if shortest_path:
    print("Shortest path:", shortest_path)
else:
    print("Path doesn't exist.")
