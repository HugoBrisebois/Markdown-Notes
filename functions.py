import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Functions(self):
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