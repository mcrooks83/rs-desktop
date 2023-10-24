from tkinter import  INSERT,END,LabelFrame,Text,Scrollbar

class ConsoleFrame(LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure( text = "Console")
        self.grid(row=1, column=0,columnspan=1, sticky='we')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.console = Text(self, state='disabled',  width=40, height=6,   wrap="none", borderwidth=0)
        self.textVsb = Scrollbar(self, orient="vertical", command=self.console.yview)
        self.textHsb = Scrollbar(self, orient="horizontal", command=self.console.xview)
        self.console.configure(yscrollcommand=self.textVsb.set, xscrollcommand=self.textHsb.set)
        self.console.grid(row=0, column=0, sticky="nsew")
        self.textVsb.grid(row=0, column=1, sticky="ns")
        self.textHsb.grid(row=1, column=0, sticky="esw")
        self.console.configure(font='TkFixedFont')
        self.console.configure(state ='normal')
        self.console.insert(INSERT, "\n")
        self.console.insert(INSERT,"-| Right Step Desktop |-" + "\n",'first_message')
        self.console.tag_config('first_message', foreground='green' , underline=1)
        self.console.insert(INSERT,"Welcome to Right Step Desktop \n \n")
        self.console.configure(state ='disabled')
        self.console.yview(END)

    # inserts text into the console
    def display_title_text(self):
        self.console.configure(state ='normal')
        self.console.insert(INSERT,"-| Right Step Desktop |-" + "\n",'first_message')
        self.console.tag_config('first_message', foreground='green' , underline=1)
        self.console.insert(INSERT,"Welcome to Right Step Desktop. \n \n")
        self.console.configure(state ='disabled')
        self.console.yview(END)

    def insert_text(self, text):
        self.console.configure(state ='normal')
        self.console.insert(INSERT,text)
        self.configure_state('disabled')
        self.set_yview(END)
    
    def clear_console(self):
        self.console.configure(state ='normal')
        self.console.delete("1.0","end")
        #self.console.insert(INSERT, "\n")
        #self.display_title_text()
        self.console.configure(state="disabled")
       
    def configure_state(self, state):
        self.console.configure(state=state)

    def tag_config(self, mess, foreground, underline):
        self.console.tag_config(mess, foreground=foreground, underline=underline)
    
    def set_yview(self,command):
        self.console.yview(command)