"""TIC-TAC-TOE GAME"""


import tkinter as tk
from tkinter import font
from dataclasses import dataclass
from itertools import cycle


@dataclass
class Player():
    label: str
    color: str


@dataclass
class Move():
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
PLAYERS = (
    Player(label="X", color="purple"),
    Player(label="O", color="green"),
)

class Game:
    def __init__(self, players=PLAYERS, board_size=BOARD_SIZE):
        self.players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.players)
        self.winner_combination_cells = []
        self.current_moves = []
        self.has_winner = False
        self.winning_combination_cells = []
        self.setup_board()

    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self.winning_combination_cells = self.get_winning_combination_cells()

    def get_winning_combination_cells(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        """Return True if move has not been played and current game has no winner yet, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self.current_moves[row][col].label == ""
        no_winner = not self.has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self.current_moves[row][col] = move
        for combination in self.winning_combination_cells:
            result = set(
                self.current_moves[n][m].label
                for n, m in combination
            )
            is_win = (len(result) == 1) and ("" not in result)
            if is_win:
                self.has_winner = True
                self.winner_combination_cells = combination
                break

    def winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self.has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self.has_winner
        played_moves = (
            move.label for row in self.current_moves for move in row
        )
        return no_winner and all(played_moves) # Check if there is a winner and if all the moves in .current_moves have a label different from the empty string.

    def alternate_player(self):
        self.current_player = next(self.players) # For the next player to take their turn.


class Board(tk.Tk):
    def __init__(self, tictactoe):
        super().__init__()
        self.title("TIC-TAC-TOE")
        self.cells = {}
        self.game = tictactoe
        self.board_display()
        self.board_grid()
    
    def board_display(self):
        display = tk.Frame(master=self)
        display.pack()
        self.display = tk.Label(
            master=display,
            text="Ready?",
            font=font.Font(size=20, weight="bold"),
        )
        self.display.pack()

    def board_grid(self):
        grid = tk.Frame(master=self)
        grid.pack()
        for row in range(self.game.board_size):
            self.rowconfigure(row)
            self.columnconfigure(row)
            for col in range(self.game.board_size):
                button = tk.Button(
                    master=grid,
                    text="",
                    font=font.Font(size=30, weight="bold"),
                    width=3,
                    height=1,
                )
                self.cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)  # Binds the click event of every button on the game board with the .play() method.
                button.grid(                                    # This way, whenever a player clicks a given button, the method will run to process the move and update the game state.
                    row=row,
                    column=col,
                    padx=5,
                    pady=5
                )

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self.cells[clicked_btn]
        move = Move(row, col, self.game.current_player.label)
        if self.game.is_valid_move(move):      # If there is no valid move, no further action is taken.
            self.update_button(clicked_btn)
            self.game.process_move(move)
            if self.game.is_tied():
                self.update_display(msg="It's a tie!", color="maroon")
            elif self.game.winner():
                msg = f'Player "{self.game.current_player.label}" won!'
                color = self.game.current_player.color
                self.update_display(msg, color)
            else:                              # No tie and no winner, yet
                self.game.alternate_player()
                msg = f"{self.game.current_player.label}'s turn"
                self.update_display(msg)
    
    def update_button(self, clicked_btn):
        clicked_btn.config(text=self.game.current_player.label)
        clicked_btn.config(fg=self.game.current_player.color)
    
    def update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["foreground"] = color


def main():
    game = Game()
    board = Board(game)
    board.mainloop()

if __name__ == "__main__":
    main()

