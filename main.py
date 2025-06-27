import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar
import pandas as pd
from stat_tracker import StatTrackerApp
from video_player import VideoPlayer

def main():
    root = tk.Tk()
    app = StatTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()