import random

def initialize_board(size):
    symbols = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pairs = symbols * 2
    random.shuffle(pairs)
    board = [pairs[i:i+size] for i in range(0, size*size, size)]
    return board

def display_board(board, revealed):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if revealed[row][col]:
                print(board[row][col], end=' ')
            else:
                print('*', end=' ')
        print()

def check_win(revealed):
    return all(all(row) for row in revealed)

def main():
    size = 4  # Change this to adjust the size of the board
    board = initialize_board(size)
    revealed = [[False] * size for _ in range(size)]
    matched = set()
    
    while not check_win(revealed):
        display_board(board, revealed)
        try:
            print("Enter the row and column of the first tile (e.g., 1 2): ")
            row1, col1 = map(int, input().split())
            print("Enter the row and column of the second tile: ")
            row2, col2 = map(int, input().split())
            if row1 < 0 or row1 >= size or col1 < 0 or col1 >= size or row2 < 0 or row2 >= size or col2 < 0 or col2 >= size:
                raise ValueError("Invalid input! Row and column must be within the range of the board size.")
        except ValueError as e:
            print(e)
            continue
        
        if board[row1][col1] == board[row2][col2] and (row1, col1) != (row2, col2):
            revealed[row1][col1] = True
            revealed[row2][col2] = True
            matched.add(board[row1][col1])
            print("Match found!")
        else:
            print("No match. Try again.")
        
    print("Congratulations! You won!")

if __name__ == "__main__":
    main()
