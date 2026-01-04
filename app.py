import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename 
import json
import os
from datetime import datetime

"""Global Variables"""
# Database
NOTES_DB = "notes_database.json"
# Colour Scheme
colours= {
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
        
        self.title("MarkDown-Notes")
        self.geometry("1000x600")
        self.minsize(800, 500)
        
        # Set the window icon
        try:
            icon = tk.PhotoImage(file='Markdown_notes_256.png')
            self.iconphoto(False, icon)
        except:
            pass
        
        # Initialize variables
        self.current_filepath = None
        self.notes_db = self.load_notes_db()
        self.unsaved_changes = False
       
       # Configure fonts
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.normal_font = font.Font(family="Segeo UI", size=10)
        self.button_font = font.Font(family="Segeo UI", size=9)
        
        # Create UI
        self.create_widget()
        
        # Bind keyboard shortcuts
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-n>', lambda e: self.new_note())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-f>', lambda e: self.focus_search())
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        def create_widget(self):
            """Create the UI"""
            # Main Container
            main_container = tk.Frame(self, bg = colours['bg'])
            main_container.pack(fill='both', expand=True)
            
            # Left sidebar (notes list)
            self.create_sidebar(main_container)
            
            # Right sidebar
            self.create_editor_panel(main_container)
            
        def create_sidebar(self, parent):
            """Creae the left sidebar with notes list"""
            sidebar = tk.Frame(parent, bg=colours['sidebar_bg'])
            sidebar.pack(side='left', fill='both', padx=0, pady=0)
            sidebar.pack_propagate(False)
            
            # Header
            header = tk.Frame(sidebar, bg=colours['sidebar_bg'])
            header.pack(fill='x', padx=15, pady=15)
            
            title_label = tk.Label(
                header,
                text="Your Notes",
                font=self.title_font,
                bg = colours['sidebar_bg'],
                fg=colours['sidebar_text']
            )
            
            title_label.pack(anchor='w')
            
            # Search bar
            search_frame = tk.Frame(sidebar, bg=colours['sidebar_bg'])
            search_frame.pack(fill='x', padx=15, pady=(0, 10))
            
            self.search_var = tk.StringVar()
            self.search_var.trace('w', lambda *args: self.filter_notes())
            
            self.search_entry = tk.Entry(
                search_frame,
                textvariable=self.search_var,
                font=self.normal_font,
                bg=colours['editor_bg'],
                relief='flat',
                insertbackground=colours['text']
            )
            self.search_entry.pack(fill='x', ipady=5)
            self.search_entry.insert(0, "Search notes")
            self.searsh_entry.bind("<FocusIn>", self.on_search_focus_in)
            self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
            
            # Action buttons
            button_frame = tk.Frame(sidebar, bg=colours['sidebar_bg'])
            button_frame.pack(fill='x', padx=15, pady=(0,10))
            
            new_btn = tk.Button(
                button_frame,
                text="New Note",
                command=self.newnote,
                font=self.button_font,
                bg=colours['accent'],
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8
            )
            new_btn.pack(side='left', expand=True, fill='x', padx=(0,5))
            new_btn.bind('<Enter>', lambda e: e.widget.cnfig(bg=colours['accent_hover']))
            new_btn.bind('Leave', lambda e: e.widget.config(bg=colours['sidebar_hover']))
            
            # Notes Listbox
            list_frame = tk.Frame(sidebar, bg=colours['sidebar_bg'])
            list_frame.pack(fill="both", expand=True, padx=15, pady=(0,15))
            
            scrollbar = tk.Scrollbar(list_frame, bg=colours['sidebar_bg'])
            scrollbar.pack(side="right", fill='y')
            
            self.notes_listbox = tk.Listbox(
                list_frame,
                font=self.normal_font,
                bg=colours['sidebar_hover'],
                fg=colours['sidebar_text'],
                selectbackground=colours['accent'],
                selectforeground='white',
                relief='flat',
                highlightthickness=0,
                borderwidth=0,
                yscrollcommand=scrollbar.set,
                activestyle='none'
            )
            self.notes_listbox.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=self.notes_listbox.yview)
            
            self.note_listbox.bind('<<ListBoxSelect>>', self.on_note_select)
            self.note_listbox.bind('<<Double-Button-1>>', self.on_note_double_click)
            
            self.refresh_notes_list()
            
            def create_editor_panel(self, parent):
                """Create the right editor panel"""
                editor_container = tk.Frame(parent, bg=colours['bg'])
                editor_container.pack(side='right', fill='both', expand=True)
                
                # Toolbar
                toolbar = tk.Frame(editor_container, bg=colours['bg'])
                toolbar.pack(fill='x', padx=20, pady=(15,10))
                
                self.Current_file_label = tk.Label(
                    toolbar,
                    text="New Note",
                    font=self.title_font,
                    bg=colours['bg'],
                    fg=colours['text']
                )
                self.current_file_label.pack(side='left')
                
                # save buttons
                button_container = tk.Frame(toolbar, bg=colours['bg'])
                button_container.pack(side='left')
                
                save_btn = tk.Button(
                    button_container,
                    text='save',
                    command=self.save_file,
                    font=self.button_font,
                    bg=colours['accent'],
                    fg='white',
                    relief='flat',
                    padx=20,
                    pady=8
                )
                
                save_btn.pack(side='left')
                save_btn.bind('<Enter>', lambda e: e.widget.config(bg=colours['accent_hover']))
                save_btn.bind('<Leave>', lambda e: e.widget.config(bg=colours['accent']))

                save_as_btn = tk.Button(
                    button_container,
                    text='Save As',
                    command=self.save_file_as,
                    font=self.button_font,
                    bg=colours['border'],
                    fg=colours['text'],
                    relief='flat',
                    cursor='hand2',
                    padx=20,
                    pady=8
                )
                save_as_btn.pack(side='left')
                save_as_btn.bind('<Enter>', lambda e: e.widget.config(bg='#95a5a6'))
                save_as_btn.bind('Leave', lambda e: e.widget.config(bg=colours['border']))
                
                # Text editor
                editor_frame = tk.Frame(editor_container, bg=colours['bg'])
                editor_frame.pack(fill='both', expand=True, bg=colours['bg'])
                
                self.md_edit = tk.Text(
                    editor_frame,
                    wrap='word',
                    font=('consolas', 11),
                    bg=colours['editor_bg'],
                    fg=colours['text'],
                    relief='relief',
                    borderwidth=0,
                    padx=15,
                    pady=15,
                    insertbackground=colours['accent'],
                    selectbackground=colours['accent'],
                    selectforeground='white',
                    undo=True,
                    maxundo=-1
                )
                self.md_edit.pack(side='left', fill='both', expand=True)
                
                # Add border effect
                editor_frame.config(highlightbackground=colours['border'], highlightthickness=1)
                
                scrollbar = tk.Scrollbar(editor_frame, command=self.md_edit.yview)
                scrollbar.pack(side='right', fill='y')
                self.md_edit.config(yscrollcommand=scrollbar.set)
                
                # Track changes
                self.md_edit.bind('<<Modified>>', self.on_text_modified)
                
            def on_text_modified(self):
                """handle text modifications"""
                if self.md_edit.edit_modified():
                    self.unsaved_changes = True
                    self.search_entry.select_range(0, tk.END)
            
            def focus_search(self, event):
                """Focus the search entry"""
                self.search_entry.focus_set()
                self.search_entry.select_range(0,tk.END)
                
            def on_search_focus_in(self, event):
                """Clear placeholder text if empty"""
                if self.search_entry.get() == "Search notes":
                    self.search_entry.delete(0, tk.END)
                    self.search_entry.config(fg=colours['text'])
                    
            def on_search_focus_out(self,event):
                """Restore placeholder text if empty"""
                if not self.search_entry.get():
                    self.search_entry.insert(0, "Search notes")
                    self.search_entry.config(fg='gray')
            
            def filter_notes(self):
                """Filter the notes based on search query"""
                query = self.search_var.get().lower()
                if query == "Search notes":
                    query = ""
                self.note_listbox.delete(0, tk.END)
                
                for note in self.notes_db:
                    if query in note['title'].lower():
                        display_text = f"{note['title']}\n{note['last_modified']}"
                        self.notes_listbox.insert(tk.END, display_text)
                        
            def refresh_notes_list(self):
                """Refresh the notes list from database"""
                self.search_var.set("")
                self.filter_notes()
                
            def on_note_selected(self, event):
                """Handle note selection (single click)"""
                pass

                
            def on_note_double_click(self,event):
                """Handle double-click on note"""
                selection = self.note_listbox.curselection()
                if not selection:
                    return

                if self.unsaved_changes:
                    response = messagebox.askyesnocanel(
                        "unsaved changes",
                        "you have unsaved changes. do you want to save them"
                    )
                    if response is None: # Cancel
                        return
                    elif response: # Yes
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
                    return[]
                
            def save_notes_db(self):
                """Save the notes database to json file"""
                with open(NOTES_DB, 'w', encoding='utf-8') as f:
                    json.dump(self.notes_db, f, indent=2)
                    
            def add_note_db(self, filepath, title=None):
                """Add or update note in database"""
                self.note_db = [n for n in self.note_db if n['filepath'] != filepath]
                
                if title is None:
                    title = os.path.splittext(os.path.basename(filepath))[0]
                    
                note_entry = {
                    'title': title,
                    'filepath': filepath,
                    'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                self.note_db.insert(0, note_entry)
                self.save_notes_db()
                self.refresh_notes_list()
                
            def open_file(self):
                """Open File Dialog"""
                if self.unsaved_changes:
                    response = messagebox.askyesnocancel(
                        "Unsaved Changes",
                        "You have unsaved changes. do you want to save them"
                    )                
                    if response is None:
                        return
                    elif response:
                        self.save_file()
                
                
                
                
                
                
            
class view_notes(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # label for the view notes frame
        label = ttk.Label(self, text="Your Notes")
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
        
        label = ttk.Label(self, text="Edit Note")
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