import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename 
import json
 

LARGEFONT =("Verdana", 25)
 
class MarkDownNotes(tk.Tk):
    
    # __init__ function for class MarkDownNotes 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Set the window icon - must be done AFTER tk.Tk.__init__
        try:
            icon = tk.PhotoImage(file='Markdown_notes_icon_256.png')
            self.iconphoto(False, icon)
        except:
            print("Icon file not found or invalid format")
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # Making frames through a truple
        for F in (edit_md, view_notes):
 
            frame = F(container, self)
 
            # Making frames through a loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(view_notes)
 
    # display the frame through a parameter change
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class view_notes(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        # label of frame Layout 2
        label = ttk.Label(self, text ="Notes", font = LARGEFONT)
        
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
 
        button1 = ttk.Button(self, text ="View Notes",
        command = lambda : controller.show_frame(  view_notes))
    
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
 
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Open note",command = lambda : controller.show_frame(edit_md))
    
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
 
         
 
 
# second window frame page1 
class edit_md(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="Edit Note", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
 
        View_notes = ttk.Button(self, text ="View Notes",command = lambda : controller.show_frame(edit_md))
        # placing the button
        Edit_md = ttk.Button(self, text ="Open Note",command = lambda : controller.show_frame(view_notes))
    
        # placing the buttons
        Edit_md.grid(row = 1, column = 0, padx = 10, pady = 10)
        View_notes.grid(row = 2, column = 0, padx = 10, pady = 10)
 
        
        
        
# Driver Code
app = MarkDownNotes()
app.mainloop()