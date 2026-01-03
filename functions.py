import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename 
import json
 

LARGEFONT =("Verdana", 25)
 
class MarkDownNotes(tk.Tk):
    
    def __init__(self, *args, **kwargs): 
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Set the window icon
        try:
            icon = tk.PhotoImage(file='Markdown_notes_icon_256.png')
            self.iconphoto(False, icon)
        except:
            print("Icon file not found or invalid format")
        
        # Initialize current filepath
        self.current_filepath = None
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # Making frames through a tuple
        for F in (edit_md, view_notes):
 
            frame = F(container, self)
 
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(view_notes)
 
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    # File operations
    def open_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown files", "*.md")])
        if not filepath:
            return
        
        # Get the edit_md frame and its text widget
        edit_frame = self.frames[edit_md]
        edit_frame.md_edit.delete("1.0", tk.END)
        
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            edit_frame.md_edit.insert(tk.END, text)
        
        self.current_filepath = filepath
        self.title(f"MarkDown-notes - {filepath}")
        
        # Switch to edit view
        self.show_frame(edit_md)
    
    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]
        )
        if not filepath:
            return
        
        # Get the edit_md frame and its text widget
        edit_frame = self.frames[edit_md]
        
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            md = edit_frame.md_edit.get("1.0", tk.END)
            output_file.write(md)
        
        self.current_filepath = filepath
        self.title(f"MarkDown-Notes - {filepath}")


class view_notes(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        # label of frame Layout 2
        label = ttk.Label(self, text ="Notes", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
        
        button1 = ttk.Button(self, text ="View Notes",
                            command = lambda : controller.show_frame(view_notes))
        button2 = ttk.Button(self, text ="Open Note",
                            command = controller.open_file)
        button3 = ttk.Button(self, text ="New Note",
                            command = lambda : controller.show_frame(edit_md))
 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
 
 
class edit_md(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="Edit Note", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
 
        # Buttons
        View_notes = ttk.Button(self, text ="View Notes",command = lambda : controller.show_frame(view_notes))
        Open_note = ttk.Button(self, text ="Open Note",command = controller.open_file)
        Save_note = ttk.Button(self, text ="Save Note",command = controller.save_file)
    
        View_notes.grid(row = 1, column = 0, padx = 10, pady = 10)
        Open_note.grid(row = 2, column = 0, padx = 10, pady = 10)
        Save_note.grid(row = 3, column = 0, padx = 10, pady = 10)
        
        # Text editor widget
        self.md_edit = tk.Text(self, wrap="word", width=60, height=20)
        self.md_edit.grid(row = 1, column = 1, rowspan=10, padx = 10, pady = 10, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.md_edit.yview)
        scrollbar.grid(row=1, column=2, rowspan=10, sticky="ns")
        self.md_edit.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
# Driver Code
app = MarkDownNotes()
app.mainloop()