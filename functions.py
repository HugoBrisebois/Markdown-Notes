import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class app(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        # Container for Pages
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand= True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        # put the frames in an empty array
        self.frames = {}
        
        # Editing frames through a truple 
        # With different pages
        
        for F in (edit_md, note_view):
            
            frame = F(container, self)
            
            # make a frame of the object from 
            # edit page and notes view wit a for loop
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky = "nsew")
        
        self.show_frame(edit_md)
        
        # display the current frame as a parameter
        def show_frame(self, cont):
            frame = self.frame[cont]
            frame.tkraise()
            
# First window frame
class edit_md(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Label of frame layout 2
        label = ttk.Label(self, text = "edit_md")
        
        # making a grid
        label.grid(row = 0, column = 4, padx= 10, pady = 10)
        
        button1 = ttk.Button(self, text = "edit", command = lambda : controller.show_frame(note_view))
        
        # placing the button
        button1.grid(row = 1, column = 1, padx=10, pady=10)
        
        # button on frame 2 (notes view)
        button2 = ttk.Button(self, text = "Notes", command = lambda : controller.show_frame(edit_md))
        
        # placing the button
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
class note_view(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Notes", command= lambda : controller.show_frame(edit_md)) 
        
        # Button to show edit_md page
        button1 = ttk.Button(self, text="Edit", command = lambda : controller.show_frame(edit_md))
        
        # placing the button
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        # Button  to show the notes(in the notes frame)
        button2 = ttk.Button(self, text = "Notes", command = lambda : controller.show_frame(note_view))
        button2.grid(row=2, column=1, padx = 10, pady = 10)
        
        
        
        
#Making the window
app = app()
app.mainloop()       
        