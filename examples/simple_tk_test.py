import tkinter as tk
import tkinter.ttk

root = tk.Tk()
root.title("Simple Tkinter Test")

frame = tkinter.ttk.Frame(root, padding=10)
frame.pack()

button = tkinter.ttk.Button(frame, text="Hello Button")
button.pack()

root.mainloop()