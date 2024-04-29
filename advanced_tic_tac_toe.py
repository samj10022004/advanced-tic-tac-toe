import tkinter as tk
from tkinter import messagebox
import random

class AdvancedTicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Tic Tac Toe")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.moves = []
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.difficulty = 'easy'  # Initialize difficulty here
        self.create_board()
        self.create_menu()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text=' ', font=('Arial', 20), width=5, height=2,
                                                command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.difficulty_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Difficulty", menu=self.difficulty_menu)
        self.difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty("easy"))
        self.difficulty_menu.add_command(label="Medium", command=lambda: self.set_difficulty("medium"))
        self.difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty("hard"))

        self.difficulty_label = tk.Label(self.master, text="Difficulty: Easy")
        self.difficulty_label.grid(row=3, columnspan=3)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_label.config(text=f"Difficulty: {difficulty.capitalize()}")

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.moves.append((row, col))
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                self.game_over()
            else:
                self.switch_player()
                self.remove_oldest_move()

                if self.current_player == 'O':
                    self.computer_move()

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def computer_move(self):
        if self.difficulty == 'easy':
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
            row, col = random.choice(empty_cells)
        elif self.difficulty == 'medium':
            row, col = self.medium_ai_move()
        else:
            row, col = self.hard_ai_move()
        self.make_move(row, col)

    def medium_ai_move(self):
        # Check for a winning move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ' and self.check_winning_move('O', i, j):
                    return i, j
        # Check for a blocking move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ' and self.check_winning_move('X', i, j):
                    return i, j
        # If no winning or blocking move, choose randomly
        return random.choice([(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' '])

    def check_winning_move(self, player, row, col):
        temp_board = [row[:] for row in self.board]
        temp_board[row][col] = player
        # Check row
        if temp_board[row] == [player, player, player]:
            return True
        # Check column
        if [temp_board[i][col] for i in range(3)] == [player, player, player]:
            return True
        # Check diagonals
        if temp_board[0][0] == temp_board[1][1] == temp_board[2][2] == player:
            return True
        if temp_board[0][2] == temp_board[1][1] == temp_board[2][0] == player:
            return True
        return False

    def hard_ai_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_maximizing):
        result = self.check_winner()
        if result == 'O':
            return 10
        elif result == 'X':
            return -10
        elif result == 'tie':
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def remove_oldest_move(self):
        if len(self.moves) > 6:
            oldest_move = self.moves.pop(0)
            row, col = oldest_move
            self.board[row][col] = ' '
            self.buttons[row][col].config(text=' ')

    def check_winner(self):
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        # Check for a tie
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'tie'
        return None

    def game_over(self):
        winner = self.check_winner()
        if winner == 'tie':
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"{winner} wins!")

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text=' ')
        self.current_player = 'X'
        self.moves = []

def main():
    root = tk.Tk()
    game = AdvancedTicTacToe(root)
    play_again_button = tk.Button(root, text="Play Again", command=game.reset_game)
    play_again_button.grid(row=4, columnspan=3)
    root.mainloop()

if __name__ == "__main__":
    main()
