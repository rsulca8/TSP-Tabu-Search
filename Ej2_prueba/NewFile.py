import tkinter as tk 

window = tk.Tk()

class NewFile(tk.Tk):
    for r in range(0, 5):
        for c in range(0, 5):
            cell = tk.Entry(window, width=10)
            cell.grid(row=r, column=c)
            cell.insert(0, '({}, {})'.format(r, c))
