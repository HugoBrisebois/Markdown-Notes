import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename 
import json
import os
from datetime import datetime

# global variables
LARGEFONT = ("Verdana", 25)
NOTES_DB = "notes_database.json"

 
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
        
        # Load the Database with the notes path
        self.notes_db = self.load_notes_db()
        
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
        # Refresh notes list
        if cont == view_notes:
            frame.refresh_notes_list()
        frame.tkraise()
    
    def load_notes_db(self):
        """Load the notes database from a json file"""
        if os.path.exists(NOTES_DB):
            try:
                with open(NOTES_DB, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_notes_db(self):
        """Save the notes database to JSON file"""
        with open(NOTES_DB, 'w', encoding='utf-8') as f:
            json.dump(self.notes_db, f, indent=2)
    
    def add_note_to_db(self, filepath, title=None):
        """Add or save the notes to a json file"""
        # Remove entry if it already exists
        self.notes_db = [n for n in self.notes_db if n['filepath'] != filepath]
        
        if title is None:
            title = os.path.basename(filepath)
    
        # add a new entry
        note_entry = {
            'title': title,
            'filepath': filepath,
            'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.notes_db.insert(0, note_entry)
        self.save_notes_db()
    
    def open_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown files", "*.md")])
        if not filepath:
            return
        self.load_note(filepath)
    
    def load_note(self, filepath):
        """Load a note from filepath"""
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found: {filepath}")
            return
            
        # Get the edit_md frame and its text widget
        edit_frame = self.frames[edit_md]
        edit_frame.md_edit.delete("1.0", tk.END)
        
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            edit_frame.md_edit.insert(tk.END, text)
            
        self.current_filepath = filepath
        self.title(f"MarkDown-notes - {filepath}")
        
        # Add to database
        self.add_note_to_db(filepath)
        
        # Switch to edit view
        self.show_frame(edit_md)
        
    def save_file(self):
        if self.current_filepath:
            # save to current file
            self.save_to_filepath(self.current_filepath)
        else:
            # Save to a new file
            self.save_file_as()
            
    def save_file_as(self):
        filepath = asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]
        )
        if not filepath:
            return
        
        self.save_to_filepath(filepath)
        
    def save_to_filepath(self, filepath):
        """Save current note to the specified filepath"""
        # Get the edit_md frame and its text widget
        edit_frame = self.frames[edit_md]
        
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            md = edit_frame.md_edit.get("1.0", tk.END)
            output_file.write(md)
            
        self.current_filepath = filepath
        self.title(f"MarkDown-Notes - {filepath}")
        
        # Add to database
        self.add_note_to_db(filepath)
        
    def new_note(self):
        """Create a new note"""
        edit_frame = self.frames[edit_md]
        edit_frame.md_edit.delete("1.0", tk.END)
        self.current_filepath = None
        self.title("MarkDown-Notes - New Note")
        self.show_frame(edit_md)


class view_notes(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # label for the view notes frame
        label = ttk.Label(self, text="Your Notes", font=LARGEFONT)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Buttons
        button1 = ttk.Button(self, text="New Note", command=controller.new_note)
        button2 = ttk.Button(self, text="Open File", command=controller.open_file)
        
        button1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        button2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Create a frame for the listbox and scrollbar
        list_frame = tk.Frame(self)
        list_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Listbox for notes
        self.notes_listbox = tk.Listbox(list_frame, width=60, height=15)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.notes_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.notes_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Bind double-click to open notes
        self.notes_listbox.bind('<Double-Button-1>', self.on_note_select)
        
        # Open selected button
        open_selected_btn = ttk.Button(self, text="Open Selected Note", command=self.open_selected_note)
        open_selected_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Configure grid weights
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # initial load
        self.refresh_notes_list()
        
    def refresh_notes_list(self):
        """Refresh the notes list from database"""
        self.notes_listbox.delete(0, tk.END)
        for note in self.controller.notes_db:
            display_text = f"{note['title']} - {note['last_modified']}"
            self.notes_listbox.insert(tk.END, display_text)
            
    def on_note_select(self, event):
        """Handle double-click on note"""
        self.open_selected_note()
    
    def open_selected_note(self):
        """Open selected note"""
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        note = self.controller.notes_db[index]
        self.controller.load_note(note['filepath'])
        
        
class edit_md(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Edit Note", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)
 
        # Buttons
        view_notes_btn = ttk.Button(self, text="View Notes", command=lambda: controller.show_frame(view_notes))
        open_note = ttk.Button(self, text="Open Note", command=controller.open_file)
        save_note = ttk.Button(self, text="Save Note", command=controller.save_file)
        save_as_note = ttk.Button(self, text="Save As", command=controller.save_file_as)
        
        view_notes_btn.grid(row=1, column=0, padx=10, pady=10)
        open_note.grid(row=2, column=0, padx=10, pady=10)
        save_note.grid(row=3, column=0, padx=10, pady=10)
        save_as_note.grid(row=4, column=0, padx=10, pady=10)
        
        # Text editor widget
        self.md_edit = tk.Text(self, wrap="word", width=60, height=20)
        self.md_edit.grid(row=1, column=1, rowspan=10, padx=10, pady=10, sticky="nsew")
        
        # Add the scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.md_edit.yview)
        scrollbar.grid(row=1, column=2, rowspan=10, sticky="ns")
        self.md_edit.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weight for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1) 
        
# Driver Code
app = MarkDownNotes()
app.mainloop()