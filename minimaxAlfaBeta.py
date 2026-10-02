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
        
        print(f"\n[MINIMAX INIT] Iniciando búsqueda con profundidad (depth) = {self.depth}")
        
        valid_cols = self.validColumns(self.currentBoard)
        print(f"[MINIMAX INIT] Columnas válidas en el tablero actual: {valid_cols}")
        
        self.bestEval, self.bestColumn = self.algorithm(self.currentBoard, self.depth, self.alpha, self.beta, True)
        
        print(f"[MINIMAX RESULT] Mejor evaluación obtenida: {self.bestEval} | Columna elegida: {self.bestColumn}\n")
        
    def validColumns(self, board):
        valid = []
        for col in range(7):
            if board[0][col] == 0:
                valid.append(col)
        return valid
    
    def algorithm(self, board, depth, alpha, beta, maxi):
        validColumnsList = self.validColumns(board)
        
        indent = "  " * (self.depth - depth)
        print(f"{indent}[ALGORITHM] Profundidad: {depth} | Turno Maximizing (Computadora): {maxi} | Columnas válidas: {validColumnsList}")
        
        if depth == 0 or not validColumnsList:
            eval_score = self.evalBoard(board)
            print(f"{indent}[BASE CASE] Fin de rama (Profundidad 0 o sin columnas). Evaluación del tablero: {eval_score}")
            return eval_score, None
        
        if maxi:
            maxEval = -1e15
            bestColumn = random.choice(validColumnsList) if validColumnsList else None
            
            for col in validColumnsList:
                tempBoard = self.simMove(board, col, 2)
                print(f"{indent}[MAXI] Computadora simula colocar ficha en columna {col} (Profundidad {depth})")
                
                tempEval, _ = self.algorithm(tempBoard, depth - 1, alpha, beta, False)
                print(f"{indent}[BRANCH EVAL] Rama [Computadora -> Columna {col}] obtuvo evaluación: {tempEval}")
                
                if tempEval >= maxEval:
                    maxEval = tempEval
                    bestColumn = col
                
                alpha = max(alpha, tempEval)
                if beta <= alpha:
                    print(f"{indent}[MAXI PRUNE] Poda Alfa-Beta activada (beta: {beta} <= alpha: {alpha})")
                    break
            
            print(f"{indent}[MAXI RESULT] Mejor evaluación de esta rama MAXI: {maxEval} eligiendo columna {bestColumn}")
            return maxEval, bestColumn
        
        else:
            minEval = +1e15
            bestColumn = random.choice(validColumnsList) if validColumnsList else None
            
            for col in validColumnsList:
                tempBoard = self.simMove(board, col, 1)
                print(f"{indent}[MINI] Humano simula colocar ficha en columna {col} (Profundidad {depth})")
                
                tempEval, _ = self.algorithm(tempBoard, depth - 1, alpha, beta, True)
                print(f"{indent}[BRANCH EVAL] Rama [Humano -> Columna {col}] obtuvo evaluación: {tempEval}")
                
                if tempEval <= minEval:
                    minEval = tempEval
                    bestColumn = col
                
                beta = min(beta, tempEval)
                if beta <= alpha:
                    print(f"{indent}[MINI PRUNE] Poda Alfa-Beta activada (beta: {beta} <= alpha: {alpha})")
                    break
            
            print(f"{indent}[MINI RESULT] Mejor evaluación de esta rama MINI: {minEval} eligiendo columna {bestColumn}")
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