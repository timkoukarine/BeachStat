"""
Simple GUI for imputting and displaying beach volleyball statistics

Tim Koukarine
"""
from typing import Union
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def init_df(p1: str, p2: str, p3 = None, p4 = None) -> pd.DataFrame:
    
    tuples = [('Attack', 'K'), ('Attack', 'E'), ('Attack', 'TA'), ('Attack', 'PCT'), ('Set', 'A'), ('Set', 'E'), ('Block', 'B'), ('Block', 'BE'), ('Serve', 'A'), ('Serve', 'E'), ('Def', 'Dig'), ('Def', 'BHE'), ('Rec', 'RE'), ('','PTS')]
    cols = pd.MultiIndex.from_tuples(tuples)
    indx = [p1, p2] if not p3 else [p1, p2, p3, p4]

    df = pd.DataFrame(columns=cols, index=indx)
    df.index.name = 'Player'
    df.style.set_caption('Player Statistics')
    df = df.fillna(0)
    # df = df.astype({('Attack', 'K'): int, ('Attack', 'E'): int, ('Attack', 'TA'): int, ('Attack', 'PCT'): float,
                    # ('Set', 'A'): int, ('Set', 'E'): int, ('Block', 'B'): int, ('Block', 'BE'): int,
                    # ('Serve', 'A'): int, ('Serve', 'E'): int, ('Def', 'Dig'): int, ('Def', 'BHE'): int,
                    # ('Rec', 'RE'): int})
    print(df)
    return df

def out_html(df: pd.DataFrame, filename: str) -> None:
    """
    Outputs the DataFrame to an HTML file.
    
    :param df: DataFrame to output
    :param filename: Name of the output file
    """
    try:
        df.to_html(filename, index=True)
        messagebox.showinfo("Success", f"Data saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def out_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Outputs the DataFrame to a CSV file.
    
    :param df: DataFrame to output
    :param filename: Name of the output file
    """
    try:
        df.to_csv(filename, index=True)
        messagebox.showinfo("Success", f"Data saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

class StatTrackerApp:
    def __init__(self, root):
        self.root = root
        root.title("Beach Volleyball Stat Tracker")

        self.df = None
        self.players = []

        self.stat_categories = [
            ('Attack', 'K'), ('Attack', 'E'), ('Attack', 'TA'),
            ('Set', 'A'), ('Set', 'E'),
            ('Block', 'B'), ('Block', 'BE'),
            ('Serve', 'A'), ('Serve', 'E'),
            ('Def', 'Dig'), ('Def', 'BHE'),
            ('Reception', 'RE')
        ]

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Enter Player Names (2 or 4):").grid(row=0, column=0, columnspan=2)

        self.name_entries = []
        for i in range(4):
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=0, padx=5, pady=5)
            self.name_entries.append(entry)

        tk.Button(self.root, text="Start 2v2", command=self.start_game).grid(row=5, column=0, columnspan=2, pady=10)

    def start_game(self):
        names = [e.get().strip() for e in self.name_entries if e.get().strip()]
        if len(names) not in (2, 4):
            messagebox.showerror("Invalid Input", "Enter 2 or 4 player names.")
            return

        self.players = names
        self.df = init_df(*names)
        self.create_stat_screen()

    def create_stat_screen(self):
        self.clear_window()

        for col, (category, stat) in enumerate(self.stat_categories):
            tk.Label(self.root, text=f"{category}-{stat}").grid(row=0, column=col+1, padx=2)

        for row, player in enumerate(self.players):
            tk.Label(self.root, text=player).grid(row=row+1, column=0, sticky="w")

            for col, (category, stat) in enumerate(self.stat_categories):
                btn = tk.Button(self.root, text="+", width=3,
                                command=lambda p=player, c=category, s=stat: self.increment_stat(p, c, s))
                btn.grid(row=row+1, column=col+1)

        # Save buttons
        tk.Button(self.root, text="Save CSV", command=self.save_csv).grid(row=len(self.players)+2, column=0, pady=10)
        tk.Button(self.root, text="Save HTML", command=self.save_html).grid(row=len(self.players)+2, column=1, pady=10)

    def increment_stat(self, player, category, stat):
        self.df.at[player, (category, stat)] += 1

    def save_csv(self):
        out_csv(self.df, "volleyball_stats.csv")

    def save_html(self):
        out_html(self.df, "volleyball_stats.html")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = StatTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()