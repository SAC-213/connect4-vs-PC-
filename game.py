import tkinter as tk
import window
import time
import random
import minimaxAlfaBeta
from tkinter import messagebox

class Game:
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.currentPlayer = random.choice([1, 2])
        self.fullBoard = False
    
        self.updateTurnLabel()
    
    def updateTurnLabel(self):
        if self.currentPlayer == 1:
            self.window.labelCurrentPlayer.config(text="Your turn", fg="#f2ec41")
        else:
            self.window.labelCurrentPlayer.config(text="Computers turn", fg="#e74c3c")
            algorithm = minimaxAlfaBeta.Minimax(self.window)
            bestColumn = algorithm.bestColumn
            del algorithm
            self.handleMove(bestColumn)
            
    def handleMove(self, col):
        if not self.window.running or self.window.top[col] == 6:
            return

        row = 5 - self.window.top[col]

        self.window.draw(col, row, self.currentPlayer)
        self.window.matrix[row][col] = self.currentPlayer
        self.window.top[col] += 1

        if self.checkWinner(self.window.matrix, self.currentPlayer):
            winner = "You" if self.currentPlayer == 1 else "Computer"
            messagebox.showinfo("Fin del juego", f"Winner: {winner}!")
            self.window.running = True
            return

        if all(top == 6 for top in self.window.top):
            messagebox.showinfo("Draw!.")
            self.window.running = True
            return

        self.currentPlayer = 2 if self.currentPlayer == 1 else 1

        self.updateTurnLabel()
        
    def checkWinner(self, board, player):
        for row in range(6):
            for col in range(4):
                if (board[row][col] == player and 
                    board[row][col+1] == player and 
                    board[row][col+2] == player and 
                    board[row][col+3] == player):
                    return True

        for row in range(3):
            for col in range(7):
                if (board[row][col] == player and 
                    board[row+1][col] == player and 
                    board[row+2][col] == player and 
                    board[row+3][col] == player):
                    return True

        for row in range(3):
            for col in range(4):
                if (board[row][col] == player and 
                    board[row+1][col+1] == player and 
                    board[row+2][col+2] == player and 
                    board[row+3][col+3] == player):
                    return True

        for row in range(3, 6):
            for col in range(4):
                if (board[row][col] == player and 
                    board[row-1][col+1] == player and 
                    board[row-2][col+2] == player and 
                    board[row-3][col+3] == player):
                    return True

        return False