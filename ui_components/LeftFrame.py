from tkinter import Button,Frame

from ui_components.SideBar import SideBar

class ButtonFrame(Frame):
    def __init__(self, master, console_frame, s, c, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.s = s
        self.c = c
        self.console_frame = console_frame
        self.grid(row=2, column=0,rowspan=1,columnspan=1, sticky='nsew') 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.clear_console_button =  Button(self,text='Clear console',command=self.clear_console)
        self.clear_console_button.grid(row=0, column=1, columnspan=1, sticky='ew',padx=5,pady=5)
    
    def clear_console(self):
        self.console_frame.clear_console()

class LeftFrame(Frame):
    def __init__(self, master, console_frame, s, c, plot_frame,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.s=s
        self.c=c
        self.plot_frame = plot_frame
        self.console_frame = console_frame
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.sidebar = SideBar(self,self.console_frame, self.s, self.c, self.plot_frame)

        #console buttons
        #self.button_frame = ButtonFrame(self, self.console_frame, self.s, self.c)