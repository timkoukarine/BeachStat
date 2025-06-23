import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar
import pandas as pd

def init_df(p1: str, p2: str, p3=None, p4=None) -> pd.DataFrame:
    tuples = [
        ('Attack', 'K'), ('Attack', 'E'), ('Attack', 'TA'), ('Attack', 'PCT'),
        ('Set', 'A'), ('Set', 'E'),
        ('Block', 'B'), ('Block', 'BE'),
        ('Serve', 'A'), ('Serve', 'E'),
        ('Def', 'Dig'), ('Def', 'BHE'),
        ('Rec', 'RE')
    ]
    cols = pd.MultiIndex.from_tuples(tuples)
    indx = [p1, p2] if not p3 else [p1, p2, p3, p4]
    df = pd.DataFrame(0, index=indx, columns=cols)
    df.index.name = 'Player'
    df = df.astype({col: int for col in cols if col != ('Attack', 'PCT')})
    df[('Attack', 'PCT')] = 0.0
    return df

def out_html(df: pd.DataFrame, filename: str) -> None:
    try:
        df.to_html(filename, index=True)
        messagebox.showinfo("Success", f"Data saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def out_csv(df: pd.DataFrame, filename: str) -> None:
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
            ('Attack', 'K'), ('Attack', 'E'), ('Attack', 'TA'), ('Attack', 'PCT'),
            ('Set', 'A'), ('Set', 'E'),
            ('Block', 'B'), ('Block', 'BE'),
            ('Serve', 'A'), ('Serve', 'E'),
            ('Def', 'Dig'), ('Def', 'BHE'),
            ('Rec', 'RE')
        ]

        self.summary_window = None
        self.create_start_screen()

    def create_start_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Player Names (2 or 4):").grid(row=0, column=0, columnspan=2)

        self.name_entries = []
        for i in range(4):
            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=0, padx=10, pady=5)
            self.name_entries.append(entry)

        tk.Button(self.root, text="Go", command=self.start_game).grid(row=5, column=0, columnspan=2, pady=10)

    def start_game(self):
        names = [e.get().strip() for e in self.name_entries if e.get().strip()]
        if len(names) not in (2, 4):
            messagebox.showerror("Invalid Input", "Enter 2 or 4 player names.")
            return

        self.players = names
        self.df = init_df(*names)
        self.create_stat_screen()
        self.open_summary_window()

    def create_stat_screen(self):
        self.clear_window()
        player_frames = []

        # Create player frames side-by-side
        for i, player in enumerate(self.players):
            frame = tk.LabelFrame(self.root, text=player, padx=5, pady=5)
            frame.grid(row=0, column=i, padx=10, pady=10, sticky="n")
            player_frames.append(frame)

        # Group stats by category
        grouped = {}
        for category, stat in self.stat_categories:
            grouped.setdefault(category, []).append(stat)

        # For each player
        for i, player in enumerate(self.players):
            player_frame = player_frames[i]

            for j, (category, stats) in enumerate(grouped.items()):
                if (category, stat) != ('Attack', 'PCT'): 
                    cat_frame = tk.LabelFrame(player_frame, text=category, padx=5, pady=5)
                    cat_frame.pack(fill="both", expand=True, pady=5)

                for k, stat in enumerate(stats):
                    row = tk.Frame(cat_frame)
                    row.pack(anchor="w", pady=1)

                    tk.Label(row, text=stat, width=6).pack(side="left")
                    if (category, stat) != ('Attack', 'PCT'):
                        tk.Button(row, text="+", width=2,
                                command=lambda p=player, c=category, s=stat: self.update_stat(p, c, s, 1)).pack(side="left")
                        tk.Button(row, text="-", width=2,
                                command=lambda p=player, c=category, s=stat: self.update_stat(p, c, s, -1)).pack(side="left")

        entry_csv = tk.Entry(self.root, width=20)
        entry_csv.grid(row=len(self.players) + 2, column=0, pady=10)
        tk.Button(self.root, text="Save CSV", command=lambda: self.save_csv(entry_csv.get())).grid(row=len(self.players)+2, column=1, pady=10)
        
        entry_html = tk.Entry(self.root, width=20)
        entry_html.grid(row=len(self.players) + 3, column=0, pady=10)
        tk.Button(self.root, text="Save HTML", command=lambda: self.save_html(entry_html.get())).grid(row=len(self.players)+3, column=1, pady=10)


    def update_stat(self, player, category, stat, delta):
        if (category, stat) == ('Attack', 'PCT'):
            return  # Don't allow direct edits to percentage

        # Update with clamping to 0
        self.df.at[player, (category, stat)] = max(0, self.df.at[player, (category, stat)] + delta)

        if (category, stat) in [('Attack', 'K'), ('Attack', 'E')]:
            # Update attack percentage if K, E, or TA is modified
            self.update_stat(player, 'Attack', 'TA', delta)

        # Recalculate attack percentage
        K = self.df.at[player, ('Attack', 'K')]
        E = self.df.at[player, ('Attack', 'E')]
        TA = self.df.at[player, ('Attack', 'TA')]
        self.df.at[player, ('Attack', 'PCT')] = round((K - E) / TA, 3) if TA > 0 else 0.0

        self.update_summary_window()

    def save_csv(self, filename):
        out_csv(self.df, filename)

    def save_html(self, filename):
        out_html(self.df, filename)

    def open_summary_window(self):
        if self.summary_window:
            self.summary_window.destroy()

        self.summary_window = Toplevel(self.root)
        self.summary_window.title("Live Stats Summary")

        self.text = Text(self.summary_window, wrap="none", width=100)
        self.text.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.summary_window, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scrollbar.set)

        self.update_summary_window()

    def update_summary_window(self):
        if not self.summary_window:
            return
        self.text.delete("1.0", "end")
        self.text.insert("end", self.df.to_string())

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = StatTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()