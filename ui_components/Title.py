from tkinter import Label, CENTER

class Title(Label):
    def __init__(self, master, text, *args, **kwargs):
        super().__init__(master, width=60, height=2, bg='#1C1F33', fg="#ED8E5A", text=text,  font=("Hallo Sans", 20, "bold"), anchor=CENTER, *args, **kwargs)
        self.grid(row=0, column=0, columnspan=1, sticky='nsew')
