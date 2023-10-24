from tkinter import PanedWindow
from ui_components.LeftFrame import LeftFrame
from ui_components.PlotFrame import PlotFrame
from ui_components.Console import ConsoleFrame

class AppCanvas(PanedWindow):
    def __init__(self, master,  sensors, config,   *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        console_frame = ConsoleFrame(master)
        self.s = sensors
        self.c = config
        self.config(orient="horizontal",  sashwidth = 10)
        self.grid(row=1, column=0,rowspan=1,columnspan=1, sticky='news',padx=5,pady=5)
        self.plot_frame = PlotFrame(self, console_frame, self.s, self.c)
        self.left_frame = LeftFrame(self, console_frame, self.s, self.c, self.plot_frame)
 
        self.add(self.left_frame)
        self.add(self.plot_frame)
