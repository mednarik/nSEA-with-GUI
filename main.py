import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter Loop")


info_label = tk.Label(root, text="Paste URL")

entry = tk.Entry(root)
entry.pack()

# Start the main event loop
root.mainloop()