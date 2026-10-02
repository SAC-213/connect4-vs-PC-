import tkinter as tk
import game

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Búsqueda Adversaria - Conecta 4")
        
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.geometry("420x460")
        
        self.resizable(False,False)
        
        self.matrix = [[0 for _ in range(7)] for _ in range(6)]
        
        self.top = [0,0,0,0,0,0,0]
        
        self.canvas = tk.Canvas(self, width=420, height=420, highlightthickness=0, bg="#5b6ee1")
        
        self.canvas.pack()
        
        self.running = False
        
        self.game = None
        
        self.initTools()
        self.initBoard()
        
    def initBoard(self):
        tileWidth = 60
        tileHeight = 70
        for row in range(6):
            for col in range(7):
                xCenter = (col * tileWidth) + (tileWidth / 2)
                yCenter = (row * tileHeight) + (tileHeight / 2)
                x0 = xCenter - 20
                y0 = yCenter - 20
                x1 = xCenter + 20
                y1 = yCenter + 20
                self.canvas.create_oval(x0, y0, x1, y1, fill="#3f3f74", outline="")
                
        self.canvas.bind("<Button-1>", self.handleClick)
    
    def handleClick(self, event):
        if not self.running or not self.game or not self.game.currentPlayer:
            return
            
        x, y = event.x, event.y
        
        if 0 <= x < 420 and 0 <= y < 420:
            tileWidth = 60
            col = int(x // tileWidth)
            self.game.handleMove(col)
            
    def draw(self, col, row, player):
        tileWidth = 60
        tileHeight = 70
        xCenter = (col * tileWidth) + (tileWidth / 2)
        yCenter = (row * tileHeight) + (tileHeight / 2)
        x0 = xCenter - 20
        y0 = yCenter - 20
        x1 = xCenter + 20
        y1 = yCenter + 20
        color = "#f2ec41" if player == 1 else "#e74c3c"
        self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline="")

    def initTools(self):
        self.toolBar = tk.Frame(self, bg="#3f3f74")
        self.toolBar.pack(side=tk.TOP, fill=tk.X)
    
        self.btnStart = tk.Button(self.toolBar, text="Start", command=self.run)
        self.btnStart.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.labelLevel = tk.Label(self.toolBar, text="Level:", bg="#3f3f74", fg="white")
        self.labelLevel.pack(side=tk.LEFT, padx=(10, 2), pady=10)
        level = [1, 2, 3]
        self.opt = tk.IntVar(value=1)
    
        self.optionMenu = tk.OptionMenu(self.toolBar, self.opt, *level)
        self.optionMenu.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.labelCurrentPlayer = tk.Label(self.toolBar, text="", bg="#3f3f74", fg="white")
        self.labelCurrentPlayer.pack(side=tk.LEFT, padx=(10, 2), pady=10)
        
    def run(self):
        if self.running:
            print("Restarting")
            self.game = None
            self.running = False
            self.matrix = [[0 for _ in range(7)] for _ in range(6)]
            self.top = [0,0,0,0,0,0,0]
            self.canvas.delete("all")
            self.initBoard()
            self.optionMenu.config(state="normal")
            self.btnStart.config(text="Start")
        else:
            print("Starting")
            self.running = True
            self.optionMenu.config(state="disabled")
            self.btnStart.config(text="Restart")
            self.game = game.Game(self)