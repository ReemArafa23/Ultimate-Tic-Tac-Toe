import random

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        # Reset the boards, current turn, and winner
        self.boards = [[0] * 9 for _ in range(9)]  # 9 boards of 9 cells each
        self.main_board = [0] * 9  # Main board that keeps track of the status of the 9 boards
        self.current_turn = 1  # Player 1 starts (1 for human, -1 for AI)
        self.winner = None
        self.current_board = -1  # Any board can be played initially

    def make_move(self, x, y, cell):
        if self.boards[x][y][cell] == 0 and self.winner is None:
            self.boards[x][y][cell] = self.current_turn
            if self.check_win(x, y):
                self.winner = self.current_turn
            self.current_turn = -self.current_turn  # Switch turns

    def check_win(self, x, y):
        # Check if the current player has won on the given board (3x3 grid)
        for i in range(3):
            if self.boards[x][i] == self.current_turn and self.boards[y][i] == self.current_turn:
                return True
        return False

    def get_game_state(self):
        return {
            'boards': self.boards,
            'main_board': self.main_board,
            'current_turn': self.current_turn,
            'winner': self.winner,
            'current_board': self.current_board
        }

    # AI logic using the Minimax algorithm
    def minimax(self, board, depth, maximizing_player):
        winner = self.check_winner_on_board(board)
        if winner == 1:
            return 10 - depth  # Human player wins
        elif winner == -1:
            return depth - 10  # AI wins
        elif all(cell != 0 for cell in board):
            return 0  # It's a tie (draw)

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = -1  # AI move
                    eval = self.minimax(board, depth + 1, False)
                    board[i] = 0  # Undo the move
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 1  # Human move
                    eval = self.minimax(board, depth + 1, True)
                    board[i] = 0  # Undo the move
                    min_eval = min(min_eval, eval)
            return min_eval

    def check_winner_on_board(self, board):
        # Check for a winner on a specific 3x3 board
        for i in range(3):
            if board[i] == board[i+1] == board[i+2]:
                return board[i]
        return None

    def ai_move(self):
        best_move = None
        best_value = float('-inf')
        for i in range(9):
            if self.boards[self.current_board][i] == 0:  # If the cell is empty
                self.boards[self.current_board][i] = -1  # AI move
                move_value = self.minimax(self.boards[self.current_board], 0, False)
                self.boards[self.current_board][i] = 0  # Undo the move
                if move_value > best_value:
                    best_value = move_value
                    best_move = i
        if best_move is not None:
            self.boards[self.current_board][best_move] = -1  # AI makes the move

    def play_ai_turn(self):
        if self.current_turn == -1:  # If it's the AI's turn
            self.ai_move()
            self.current_turn = 1  # Switch turn to the human player
