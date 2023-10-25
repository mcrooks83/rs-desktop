class Config:
    def __init__(self):
        self.number_of_plot_points = 250
        self.data_rate = 60
        self.smoothing_window = 11
        self.polyorder = 4
        self.alpha = 0.2 # pre set alpha for exponential moving average filter