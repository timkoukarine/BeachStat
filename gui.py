import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
# from main import init_df, out_html, out_csv

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


window = tk.Tk()
window.title("Beach Volleyball Statistics")

window.geometry("400x300")
label = tk.Label(window, text="Beach Volleyball Statistics", font=("Arial", 16))
label.pack(pady=20)
label2 = tk.Label(window, text="Enter player names:")
label2.pack(pady=10)
entry1 = tk.Entry(window, width=30)
entry1.pack(pady=5)
entry2 = tk.Entry(window, width=30)
entry2.pack(pady=5)
entry3 = tk.Entry(window, width=30)
entry3.pack(pady=5)
entry4 = tk.Entry(window, width=30)
entry4.pack(pady=5)

button1 = tk.Button(window, text="Go", command=lambda: [entry1.get(), entry2.get(), entry3.get() or None, entry4.get() or None])
# button1 = tk.Button(window, text="Go", command=lambda: init_df(entry1.get(), entry2.get(), entry3.get() or None, entry4.get() or None))
button1.pack(pady=10)


window.mainloop()