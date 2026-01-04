import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from tkinter.filedialog import askopenfilename, asksaveasfilename 
import json
import os
from datetime import datetime

# Constants
NOTES_DB = "notes_database.json"

# Color scheme
COLORS = {
    'bg': '#f5f5f5',
    'sidebar_bg': '#2c3e50',
    'sidebar_hover': '#34495e',
    'sidebar_text': '#ecf0f1',
    'editor_bg': '#ffffff',
    'accent': '#3498db',
    'accent_hover': '#2980b9',
    'text': '#2c3e50',
    'border': '#bdc3c7'
}


class MarkDownNotes(tk.Tk):
    
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Markdown Notes")
        self.geometry("1000x600")
        self.minsize(800, 500)
        
        # Set icon
        try:
            icon = tk.PhotoImage(file='Markdown_notes_icon_256.png')
            self.iconphoto(False, icon)
        except:
            pass
        
        # Initialize variables
        self.current_filepath = None
        self.notes_db = self.load_notes_db()
        self.unsaved_changes = False
        
        # Configure fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.normal_font = tkfont.Font(family="Segoe UI", size=10)
        self.button_font = tkfont.Font(family="Segoe UI", size=9)
        
        # Create UI
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-n>', lambda e: self.new_note())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-f>', lambda e: self.focus_search())
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create the main UI layout"""
        # Main container
        main_container = tk.Frame(self, bg=COLORS['bg'])
        main_container.pack(fill='both', expand=True)
        
        # Left sidebar (notes list)
        self.create_sidebar(main_container)
        
        # Right panel (editor)
        self.create_editor_panel(main_container)
    
    def create_sidebar(self, parent):
        """Create the left sidebar with notes list"""
        sidebar = tk.Frame(parent, bg=COLORS['sidebar_bg'], width=280)
        sidebar.pack(side='left', fill='both', padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # Header
        header = tk.Frame(sidebar, bg=COLORS['sidebar_bg'])
        header.pack(fill='x', padx=15, pady=15)
        
        title_label = tk.Label(
            header, 
            text="Your Notes", 
            font=self.title_font,
            bg=COLORS['sidebar_bg'],
            fg=COLORS['sidebar_text']
        )
        title_label.pack(anchor='w')
        
        # Search bar
        search_frame = tk.Frame(sidebar, bg=COLORS['sidebar_bg'])
        search_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_notes())
        
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.normal_font,
            bg=COLORS['editor_bg'],
            fg=COLORS['text'],
            relief='flat',
            insertbackground=COLORS['text']
        )
        self.search_entry.pack(fill='x', ipady=5)
        self.search_entry.insert(0, "Search notes...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        # Action buttons
        button_frame = tk.Frame(sidebar, bg=COLORS['sidebar_bg'])
        button_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        new_btn = tk.Button(
            button_frame,
            text="+ New Note",
            command=self.new_note,
            font=self.button_font,
            bg=COLORS['accent'],
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        new_btn.pack(side='left', expand=True, fill='x', padx=(0, 5))
        new_btn.bind('<Enter>', lambda e: e.widget.config(bg=COLORS['accent_hover']))
        new_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['accent']))
        
        open_btn = tk.Button(
            button_frame,
            text="Open File",
            command=self.open_file,
            font=self.button_font,
            bg=COLORS['sidebar_hover'],
            fg=COLORS['sidebar_text'],
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        open_btn.pack(side='left', expand=True, fill='x')
        open_btn.bind('<Enter>', lambda e: e.widget.config(bg=COLORS['sidebar_bg']))
        open_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['sidebar_hover']))
        
        # Notes listbox
        list_frame = tk.Frame(sidebar, bg=COLORS['sidebar_bg'])
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(list_frame, bg=COLORS['sidebar_bg'])
        scrollbar.pack(side='right', fill='y')
        
        self.notes_listbox = tk.Listbox(
            list_frame,
            font=self.normal_font,
            bg=COLORS['sidebar_hover'],
            fg=COLORS['sidebar_text'],
            selectbackground=COLORS['accent'],
            selectforeground='white',
            relief='flat',
            highlightthickness=0,
            borderwidth=0,
            yscrollcommand=scrollbar.set,
            activestyle='none'
        )
        self.notes_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.notes_listbox.yview)
        
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        self.notes_listbox.bind('<Double-Button-1>', self.on_note_double_click)
        
        self.refresh_notes_list()
    
    def create_editor_panel(self, parent):
        """Create the right editor panel"""
        editor_container = tk.Frame(parent, bg=COLORS['bg'])
        editor_container.pack(side='right', fill='both', expand=True)
        
        # Toolbar
        toolbar = tk.Frame(editor_container, bg=COLORS['bg'], height=60)
        toolbar.pack(fill='x', padx=20, pady=(15, 10))
        
        self.current_file_label = tk.Label(
            toolbar,
            text="New Note",
            font=self.title_font,
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        self.current_file_label.pack(side='left')
        
        # Save buttons
        button_container = tk.Frame(toolbar, bg=COLORS['bg'])
        button_container.pack(side='right')
        
        save_btn = tk.Button(
            button_container,
            text="Save",
            command=self.save_file,
            font=self.button_font,
            bg=COLORS['accent'],
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        save_btn.pack(side='left', padx=(0, 8))
        save_btn.bind('<Enter>', lambda e: e.widget.config(bg=COLORS['accent_hover']))
        save_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['accent']))
        
        save_as_btn = tk.Button(
            button_container,
            text="Save As",
            command=self.save_file_as,
            font=self.button_font,
            bg=COLORS['border'],
            fg=COLORS['text'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        save_as_btn.pack(side='left')
        save_as_btn.bind('<Enter>', lambda e: e.widget.config(bg='#95a5a6'))
        save_as_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['border']))
        
        # Text editor
        editor_frame = tk.Frame(editor_container, bg=COLORS['bg'])
        editor_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.md_edit = tk.Text(
            editor_frame,
            wrap='word',
            font=('Consolas', 11),
            bg=COLORS['editor_bg'],
            fg=COLORS['text'],
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=15,
            insertbackground=COLORS['accent'],
            selectbackground=COLORS['accent'],
            selectforeground='white',
            undo=True,
            maxundo=-1
        )
        self.md_edit.pack(side='left', fill='both', expand=True)
        
        # Add border effect
        editor_frame.config(highlightbackground=COLORS['border'], highlightthickness=1)
        
        scrollbar = tk.Scrollbar(editor_frame, command=self.md_edit.yview)
        scrollbar.pack(side='right', fill='y')
        self.md_edit.config(yscrollcommand=scrollbar.set)
        
        # Track changes for auto-save
        self.md_edit.bind('<<Modified>>', self.on_text_modified)
    
    def on_text_modified(self, event=None):
        """Handle text modifications"""
        if self.md_edit.edit_modified():
            self.unsaved_changes = True
            self.md_edit.edit_modified(False)
    
    def focus_search(self):
        """Focus the search entry"""
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
    
    def on_search_focus_in(self, event):
        """Clear placeholder text on focus"""
        if self.search_entry.get() == "Search notes...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLORS['text'])
    
    def on_search_focus_out(self, event):
        """Restore placeholder text if empty"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search notes...")
            self.search_entry.config(fg='gray')
    
    def filter_notes(self):
        """Filter notes based on search query"""
        query = self.search_var.get().lower()
        if query == "search notes...":
            query = ""
        
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes_db:
            if query in note['title'].lower():
                display_text = f"{note['title']}\n{note['last_modified']}"
                self.notes_listbox.insert(tk.END, display_text)
    
    def refresh_notes_list(self):
        """Refresh the notes list from database"""
        self.search_var.set("")
        self.filter_notes()
    
    def on_note_select(self, event):
        """Handle note selection (single click)"""
        pass
    
    def on_note_double_click(self, event):
        """Handle double-click on note"""
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        
        if self.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_file()
        
        # Get the actual index from filtered results
        index = selection[0]
        display_text = self.notes_listbox.get(index)
        title = display_text.split('\n')[0]
        
        # Find the note in the database
        for note in self.notes_db:
            if note['title'] == title:
                self.load_note(note['filepath'])
                break
    
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
        """Add or update note in database"""
        self.notes_db = [n for n in self.notes_db if n['filepath'] != filepath]
        
        if title is None:
            title = os.path.splitext(os.path.basename(filepath))[0]
        
        note_entry = {
            'title': title,
            'filepath': filepath,
            'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.notes_db.insert(0, note_entry)
        self.save_notes_db()
        self.refresh_notes_list()
    
    def open_file(self):
        """Open file dialog"""
        if self.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        filepath = askopenfilename(
            filetypes=[("Markdown files", "*.md"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            self.load_note(filepath)
    
    def load_note(self, filepath):
        """Load a note from filepath"""
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found: {filepath}")
            return
        
        self.md_edit.delete("1.0", tk.END)
        
        try:
            with open(filepath, mode="r", encoding="utf-8") as input_file:
                text = input_file.read()
                self.md_edit.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")
            return
        
        self.current_filepath = filepath
        filename = os.path.splitext(os.path.basename(filepath))[0]
        self.current_file_label.config(text=filename)
        self.unsaved_changes = False
        
        self.add_note_to_db(filepath)
    
    def save_file(self):
        """Save current file"""
        if self.current_filepath:
            self.save_to_filepath(self.current_filepath)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save as new file"""
        filepath = asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            self.save_to_filepath(filepath)
    
    def save_to_filepath(self, filepath):
        """Save current note to the specified filepath"""
        try:
            with open(filepath, mode="w", encoding="utf-8") as output_file:
                md = self.md_edit.get("1.0", tk.END)
                output_file.write(md)
            
            self.current_filepath = filepath
            filename = os.path.splitext(os.path.basename(filepath))[0]
            self.current_file_label.config(text=filename)
            self.unsaved_changes = False
            
            self.add_note_to_db(filepath)
            
            messagebox.showinfo("Success", "Note saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def new_note(self):
        """Create a new note"""
        if self.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        self.md_edit.delete("1.0", tk.END)
        self.current_filepath = None
        self.current_file_label.config(text="New Note")
        self.unsaved_changes = False
        self.md_edit.focus_set()
    
    def on_closing(self):
        """Handle window close event"""
        if self.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before closing?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        self.destroy()


# Driver Code
if __name__ == "__main__":
    app = MarkDownNotes()
    app.mainloop()