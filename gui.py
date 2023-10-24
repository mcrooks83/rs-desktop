#tkinter
from tkinter import Tk
from classes.Sensors import Sensors
from classes.Config import Config
from ui_components.Title import Title
from ui_components.AppCanvas import AppCanvas

# main application class
class MainApplication(Tk):
    def __init__(self):
        super().__init__()

        #local class that has all the callbacks and the sensor manager on it
        self.s = Sensors()
        self.c = Config()

        #simple test function
        #s.test_sensor_manager()

        self.width = Tk.winfo_screenwidth(self)
        self.height = Tk.winfo_screenheight(self)
        self.geometry(f"{self.width}x{self.height}")
        self.title("powered by Right Step")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.canvas = AppCanvas(self, self.s, self.c)
        self.title_label = Title(self, text="Right Step Desktop")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
