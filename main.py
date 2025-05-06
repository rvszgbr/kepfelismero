# main.py

import tkinter as tk
from gui.app import FruitRecognizerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FruitRecognizerApp(root)
    root.mainloop()
