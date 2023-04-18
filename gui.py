import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

path = filedialog.askdirectory(initialdir="/", title="Select file")
print(path)

root.mainloop()