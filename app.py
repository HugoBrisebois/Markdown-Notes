import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import asksaveasfilename
# Functions

# Function for the open file name
def open_file():
    # Open a Note doc for editing or reviewing
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown files", "*.md")])
    if not filepath:
        return
    md_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        md_edit.insert(tk.END, text)
    window.title(f"MarkDown-notes - {filepath}")
    
# Function for saving files
def save_file():
    # save the file
    filepath = asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        md = md_edit.get("1.0", tk.END)
        output_file.write(md)
    window.title(f"MarkDown-Notes - {filepath}")
    

window = tk.Tk() # Make the Window
window.title("MarkDown-Note")

# configure the window's content
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

# Declaring the UI
md_edit = tk.Text(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open file", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As", command=save_file)

# placing the UI on th screen
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1,column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
md_edit.grid(row=0, column=1, sticky="nsew")


window.mainloop()