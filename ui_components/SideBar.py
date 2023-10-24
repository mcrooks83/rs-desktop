
from tkinter import PanedWindow, Frame, LabelFrame,Label, Button, BOTH

class SideBar(PanedWindow):
     def __init__(self, master, console_frame, s, c, plot_frame, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.s = s
        self.c = c
        self.plot_frame = plot_frame
        self.configure(orient="vertical",  sashwidth = 10)
        self.grid(row=0, column=0,rowspan=2,columnspan=1, sticky='news')
        self.grid_rowconfigure(0, weight=1)

        self.scan_and_connect_frame = ScanSensorFrame(self, console_frame, self.s, self.c, self.plot_frame)
        self.console_frame = console_frame

        self.add(self.console_frame)
        self.add(self.scan_and_connect_frame)

class ScanSensorFrame(LabelFrame):
    def __init__(self, master,console_frame, s, c, plot_frame, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.s = s
        self.c =c
        self.plot_frame = plot_frame
        self.console_frame = console_frame

        self.s.set_discovered_sensors_callback(self.discovered_senors)
        self.s.set_connected_sensors_callback(self.connected_sensor)
        #self.s.set_battery_status_callback(self.battery_status)
       
        self.configure(text = "Scan For Sensors",)
        self.grid(row=0, column=0,rowspan=1,columnspan=1, sticky='nesw')
        self.scan_button =  Button(self,text='Scan',command=self.scan_for_sensors)
        self.scan_button.grid(row=0, column=0, columnspan=1, sticky='ew',padx=5,pady=5)

        self.scanned_sensors_frame = Frame(self)
        self.scanned_sensors_frame.grid(row=1, column=0, columnspan=1, sticky='ew', padx=5, pady=5)

    def scan_for_sensors(self):
        # send the message to the sensor manager on the sensors class
        self.s.sensor_manager.send_message("scan", {})
        self.console_frame.clear_console()
        self.console_frame.insert_text("scanning for dots ..." + '\n\n') 

    def connect_to_sensor(self, address):
        print(address, "connect to")
        self.s.sensor_manager.send_message("connect", address)
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"connecting to dot {address} ..." + '\n\n') 
        
    def connected_sensor(self, sensor):
        print(f"UI connected to {sensor}")
        self.console_frame.clear_console()
        self.console_frame.insert_text("Connected to Dot: " + sensor.address + " " +'\n')

        # this only shows one sensor - need to keep track of sensor count for addition of rows
        #connected_sensor_frame
        #self.plot_frame.connected_sensor_frame.grid()
        self.plot_frame.connected_sensor_label.configure(text=f"{sensor.address}") 
        self.plot_frame.connected_sensor_label.grid(row=0, column=0)
        self.plot_frame.connected_sensor_batt_label.configure(text=f"{sensor.batt_level}%")
        self.plot_frame.connected_sensor_batt_label.grid(row=0, column=1)
    
        self.plot_frame.connected_sensor_identity_button = Button(self.plot_frame.connected_sensor_frame, text="identify", command= lambda: self.plot_frame.identify_sensor(sensor.address))
        self.plot_frame.connected_sensor_identity_button.grid(row=0, column=2)
        self.plot_frame.start_measuring_button = Button(self.plot_frame.connected_sensor_frame, text="start measuring", command= lambda: self.plot_frame.start_measuring_for_sensor(sensor.address))
        self.plot_frame.start_measuring_button.grid(row=0, column=3)
        self.plot_frame.stop_measuring_button = Button(self.plot_frame.connected_sensor_frame, text="stop measuring", command= lambda: self.plot_frame.stop_measuring_for_sensor(sensor.address))
        self.plot_frame.stop_measuring_button.grid(row=0, column=4)
        self.plot_frame.disconnect_button = Button(self.plot_frame.connected_sensor_frame, text="disconnect", command= lambda: self.plot_frame.disconnect_from_sensor(sensor.address))
        self.plot_frame.disconnect_button.grid(row=0, column=5)

    def discovered_senors(self, sensors):
        print(f" discovered sensors on UI {sensors}")
        labels = []
        connect_buttons = []
        battery_labels = []

        def connect_lambda(address):
            return lambda: self.connect_to_sensor(address)
    
        if(len(sensors)> 0):
            self.console_frame.clear_console()
            for s in sensors:
                self.console_frame.insert_text("Dot found: " + s.address + " " +'\n')
                label = Label(self.scanned_sensors_frame, text=f"{s.address}")
                labels.append(label)
                connect_button = Button(self.scanned_sensors_frame, text="connect", command=connect_lambda(s.address))
                connect_buttons.append(connect_button) 

            for i in range(len(labels)):
                labels[i].grid(row=i, column=0)
                connect_buttons[i].grid(row=i, column=1)    
        else:
            self.console_frame.clear_console()
            self.console_frame.insert_text("NO Dots found")