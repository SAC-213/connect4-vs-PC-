import window
import random
import copy

class Minimax():
    
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.currentBoard = self.window.matrix
        self.depth = self.window.opt.get()
        self.alpha = -1e15
        self.beta = 1e15
        
        self.bestEval, self.bestColumn = self.algorithm(self.currentBoard, self.depth, self.alpha, self.beta, True)
        
    def validColumns(self, board):
        valid = []
        for col in range(7):
            if board[0][col] == 0:
                valid.append(col)
        return valid
    
    def algorithm(self, board, depth, alpha, beta, maxi):
        validColumnsList = self.validColumns(board)
        
        if depth == 0 or not validColumnsList:
            eval_score = self.evalBoard(board)
            return eval_score, None
        
        if maxi:
            maxEval = -1e15
            bestColumn = random.choice(validColumnsList) if validColumnsList else None
            
            for col in validColumnsList:
                tempBoard = self.simMove(board, col, 2)
                
                tempEval, _ = self.algorithm(tempBoard, depth - 1, alpha, beta, False)
                
                if tempEval >= maxEval:
                    maxEval = tempEval
                    bestColumn = col
                
                alpha = max(alpha, tempEval)
                if beta <= alpha:
                    break
            
            return maxEval, bestColumn
        
        else:
            minEval = +1e15
            bestColumn = random.choice(validColumnsList) if validColumnsList else None
            
            for col in validColumnsList:
                tempBoard = self.simMove(board, col, 1)
                
                tempEval, _ = self.algorithm(tempBoard, depth - 1, alpha, beta, True)
                
                if tempEval <= minEval:
                    minEval = tempEval
                    bestColumn = col
                
                beta = min(beta, tempEval)
                if beta <= alpha:
                    break
            
            return minEval, bestColumn
    
    def simMove(self, board, col, player):
        tempBoard = copy.deepcopy(board)
        for row in range(5, -1, -1):
            if tempBoard[row][col] == 0:
                tempBoard[row][col] = player
                break
        return tempBoard
        
    def evalBoard(self, board):
        h = 0
        for row in range(6):
            if board[row][3] == 2:
                h += 1

        for row in range(6):
            for col in range(4):
                window_vals = [board[row][col], board[row][col + 1], board[row][col + 2], board[row][col + 3]]
                h += self.evaluateWindow(window_vals)

        for row in range(3):
            for col in range(7):
                window_vals = [board[row][col], board[row + 1][col], board[row + 2][col], board[row + 3][col]]
                h += self.evaluateWindow(window_vals)

        for row in range(3):
            for col in range(4):
                window_vals = [board[row][col], board[row + 1][col + 1], board[row + 2][col + 2], board[row + 3][col + 3]]
                h += self.evaluateWindow(window_vals)

        for row in range(3, 6):
            for col in range(4):
                window_vals = [board[row][col], board[row - 1][col + 1], board[row - 2][col + 2], board[row - 3][col + 3]]
                h += self.evaluateWindow(window_vals)

        return h

    def evaluateWindow(self, window):
        myPieces = window.count(2)
        enemyPieces = window.count(1)

        if myPieces == 4:
            return float("inf")

        if enemyPieces == 3 and myPieces == 0:
            return -80

        if enemyPieces == 2 and myPieces == 0:
            return -30

        if myPieces == 3 and enemyPieces == 0:
            return 50

        if myPieces == 2 and enemyPieces == 0:
            return 5

        return 0
