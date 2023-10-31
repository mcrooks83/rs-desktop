from tkinter import LabelFrame,Frame,Label, Button

from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib import style
from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
style.use("dark_background")
import threading
import math
from scipy.signal import savgol_filter

# not clean but will work
from sensor_sdk import helper_functions as hf

class PlotFrame(LabelFrame):
    def __init__(self, master,console_frame, s, c, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.s = s
        self.console_frame = console_frame
        self.c = c
        self.rate = c.data_rate
        self.max_roll = 0
        self.max_pitch = 0
        self.max_yaw = 0
        self.configure(text = "Visualisation",)

        self.s.set_sensor_data_callback(self.sensor_data_callback)
        self.s.set_stop_sensor_data_callback(self.stop_sensor_callback)
        self.s.set_battery_status_callback(self.battery_status_callback)
        self.s.set_export_done_callback(self.export_to_csv_done_callback)

        self.grid_rowconfigure(2, weight=1)  # Bottom row weight
        self.grid_columnconfigure(0, weight=1)  # Column weight

        self.connected_sensor_frame = Frame(self)
        self.connected_sensor_frame.grid(row=0, column=0, columnspan=7, sticky="new")
        self.connected_sensor_label = Label(self.connected_sensor_frame, text=f"")
        self.connected_sensor_batt_label = Label(self.connected_sensor_frame, text=f"")
        self.connected_sensor_frame.grid_columnconfigure(6,weight=1)
        self.connected_sensor_frame.grid_rowconfigure(0, weight=1)

        self.projected_angles = Figure(figsize=(6,6))
        self.ax_proj = self.projected_angles.subplots()
        self.ax_proj.set_title(f"Projected Pitch and Yaw")
        self.ax_proj.set_xlim(-50,50)
        self.ax_proj.set_ylim(-50,50)
        self.ax_proj.spines['left'].set_position('center')
        self.ax_proj.spines['bottom'].set_position('center')
        self.ax_proj.spines['right'].set_color('none')
        self.ax_proj.spines['top'].set_color('none')
        self.ax_proj.xaxis.set_ticks_position('bottom')
        self.ax_proj.yaxis.set_ticks_position('left')
        self.ax_proj.autoscale(False)
       
        self.ax_proj.text(0.005, 1.05, f"Data rate: {self.c.data_rate} Hz ", transform=self.ax_proj.transAxes)
        #self.ax_proj.text(0.005, 1.00, f"Max pitch: {self.max_pitch} deg ", transform=self.ax_proj.transAxes)
        #self.ax_proj.text(0.005, 0.95, f"Max yaw: {self.max_yaw} deg ", transform=self.ax_proj.transAxes)
        self.projected_angles_canvas = FigureCanvasTkAgg(self.projected_angles, master=self)
        self.projected_angles_canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=2)

        self.twoD_fig = Figure()
        self.ax_2d = self.twoD_fig.subplots()
        self.ax_2d.set_title(f"Euler Angles")
        self.ax_2d.set_xlabel("packet count")
        self.ax_2d.text(0.005, 1.05, f"Data Rate: {self.c.data_rate} Hz ", transform=self.ax_2d.transAxes)
        self.twoD_fig.subplots_adjust(bottom=0.15)    
        self.twoD_plot_canvas = FigureCanvasTkAgg(self.twoD_fig, master=self)
        self.twoD_plot_canvas.get_tk_widget().grid(row=2, column=0, sticky='nsew', padx=2, pady=2)
    
        self.stream_fig = Figure()
        self.ax = self.stream_fig.subplots()
        self.ax.set_title(f"Acceleration")
        self.ax.set_xlabel("packet count")
        self.ax.text(0.005, 1.05, f"Data Rate: {self.c.data_rate} Hz ", transform=self.ax.transAxes)
        self.stream_fig.subplots_adjust(bottom=0.15)        

        self.stream_fig_canvas = FigureCanvasTkAgg(self.stream_fig, master=self)
        self.stream_fig_canvas.get_tk_widget().grid(row=2,  column=1, sticky='nsew', padx=2, pady=2)
       
        ## only deals with one sensor - should use the connected sensor data class?
        self.time = []
        self.accel_x = []
        self.accel_y = []
        self.accel_z = []
        self.yaw = []
        self.pitch = []
        self.roll = []
        self.projected_roll = []
        self.projected_pitch = []
        self.projected_yaw = []
        
        self.prev_timestamp = 0
        self.packet_count = 0
        self.list_of_timestamps = []

        self.ema_roll = None
        self.ema_pitch = None
        self.ema_yaw =  None

        self.yaw_offset = None
        self.pitch_offset = None
        self.roll_offset = None

        self.bind("<Key>", self.space_pressed)
        self.focus_set()
    
    def space_pressed(self, event):
        print("key event")
        #<KeyPress event keysym=space keycode=822083616 char=' ' x=256 y=222>
        if(event.keysym == "space"):
            self.list_of_timestamps.append(self.prev_timestamp)
            

    def set_max_pitch(self, pitch):
        self.max_pitch = pitch
    
    def set_max_roll(self, roll):
        self.max_roll = roll
    
    def set_max_yaw(self, yaw):
        self.max_yaw = yaw
    # callbacks
    def update_stream_plot(self):
        
        num_of_points = self.c.number_of_plot_points
        x = self.time[-num_of_points:]

        acc_x = self.accel_x[-num_of_points:]
        acc_y = self.accel_y[-num_of_points:]
        acc_z = self.accel_z[-num_of_points:]

        roll = self.roll[-num_of_points:]
        pitch = self.pitch[-num_of_points:]
        yaw = self.yaw[-num_of_points:]

        projected_roll = self.projected_roll
        projected_pitch = self.projected_pitch
        projected_yaw = self.projected_yaw

        self.ax_proj.clear()
        self.ax_proj.set_title(f"Projected Pitch and Roll")
        self.ax_proj.set_xlim(-50,50)
        self.ax_proj.set_ylim(-50,50)
        self.ax_proj.spines['left'].set_position('center')
        self.ax_proj.spines['bottom'].set_position('center')
        self.ax_proj.spines['right'].set_color('none')
        self.ax_proj.spines['top'].set_color('none')
        self.ax_proj.xaxis.set_ticks_position('bottom')
        self.ax_proj.yaxis.set_ticks_position('left')
        self.ax_proj.autoscale(False)
        self.ax_proj.text(0.005, 1.05, f"Data rate: {self.rate} Hz ", transform=self.ax_proj.transAxes)
        #self.ax_proj.text(0.005, 1.00, f"Max pitch: {self.max_pitch} deg ", transform=self.ax_proj.transAxes)
        #self.ax_proj.text(0.005, 0.95, f"Max yaw: {self.max_yaw} deg ", transform=self.ax_proj.transAxes)
        self.ax_proj.plot(projected_yaw, projected_pitch)
        self.projected_angles_canvas.draw()

        #non threaded
        #self.clear_and_plot( self.ax, self.stream_fig_canvas, f"Acceleration {self.c.data_rate} Hz", "packet count", x, acc_x, acc_y, acc_z )
        #self.clear_and_plot( self.ax_2d, self.twoD_plot_canvas, f"Euler Angles {self.c.data_rate} Hz", "packet count",  x, roll, pitch, yaw )

        #as threads
        thread1 = threading.Thread(target=self.clear_and_plot( self.ax, self.stream_fig_canvas, f"Acceleration {self.c.data_rate} Hz", "packet count", x, acc_x, acc_y, acc_z ))
        thread2 = threading.Thread(target=self.clear_and_plot( self.ax_2d, self.twoD_plot_canvas, f"Euler Angles {self.c.data_rate} Hz", "packet count",  x, roll, pitch, yaw ))
        # Start the threads
        thread1.start()
        thread2.start()

        # Wait for both threads to complete
        thread1.join()
        thread2.join()

        self.update_stream_plot_task_id = self.after(1, self.update_stream_plot)

    # ui callbacks 

    def sensor_data_callback(self, address, data):
        timestamp = data[0][0]

        # computes the data rate
        if(self.prev_timestamp != 0):
            self.rate = int( 1/((timestamp - self.prev_timestamp)/1e6))
            self.prev_timestamp = timestamp
        else:
            self.prev_timestamp = timestamp     

        #convert quaternion to euler angles
        #def euler_from_quaternion(x, y, z, w):
        # x, y, z, w
        # in radiants
        roll, pitch, yaw = hf.euler_from_quaternion(data[0][2], data[0][3], data[0][4], data[0][1] )   
       
        if(self.packet_count == 0):
            # capture the angles for offset correction
            self.yaw_offset = yaw

            self.time.append(self.packet_count)
            self.packet_count +=1
        else:
            self.time.append(self.packet_count)
            self.packet_count+= 1

        # function get accleration depending on payload
        a_x = data[0][5] # x accel?
        a_y = data[0][6]
        a_z = data[0][7] # z accel

        self.accel_x.append(a_x)
        self.accel_y.append(a_y)
        self.accel_z.append(a_z)

        # these are the raw valus converted to degrees
        roll_deg = math.degrees(roll)
        pitch_deg = math.degrees(pitch)
        yaw_deg = math.degrees(yaw)

        self.roll.append(roll_deg)
        self.pitch.append(pitch_deg)
        self.yaw.append(yaw_deg)

        if (roll_deg > self.max_roll):
            self.set_max_roll(round(abs(roll_deg),2))
        if (pitch_deg > self.max_pitch):
            self.set_max_pitch(round(abs(pitch_deg),2))
        if(yaw_deg > self.max_yaw):
            self.set_max_yaw(round(abs(yaw_deg), 2))

        #exponential moving average 
        roll_moving_avg = hf.calculate_ema(roll, self.c.alpha, self.ema_roll)
        #pitch_moving_avg = hf.calculate_ema(pitch, self.c.alpha, self.ema_pitch)
        #yaw_moving_avg = hf.calculate_ema(yaw - self.yaw_offset, self.c.alpha, self.ema_yaw)
        pitch_moving_avg = pitch
        yaw_moving_avg = yaw - self.yaw_offset

        # head projection 
        # head_x = x_ref + scaling_factor * math.cos(flexion_radians) * math.sin(rotation_radians)
        # head_y = y_ref + scaling_factor * math.sin(flexion_radians)

        x = self.c.x_ref + (self.c.max_rotation * math.cos(pitch_moving_avg) * math.sin(yaw_moving_avg))
        y = self.c.y_ref + (self.c.max_flex_ext * math.sin(pitch_moving_avg))
        #print(f"x :{x} y: {y}")




        #self.projected_roll.append(math.degrees(roll_moving_avg))
        self.projected_pitch.append(y)
        self.projected_yaw.append(x)


    def battery_status_callback(self, address, battery):
        print(f"ui batt status {address} {battery}%")
        # to really use this we need to be able to track the rows / connected sensors to update the correct one
        self.connected_sensor_batt_label.configure(text=f"{battery}%")
        if(battery <= 10):
            self.console_frame.insert_text(f"sensor {address} battery 10% or less" + '\n\n') 
            self.console_frame.insert_text(f"sensor {address} will not send data" + '\n\n') 
    
    def stop_sensor_callback(self, address):
        print(f"stopped sensor {address}")
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"stopped sensor {address} ..." + '\n\n') 

    # frame functions
    def identify_sensor(self, address):
        print(f"indentifying sensor {address}")
        self.s.sensor_manager.send_message("identify", address)
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"indentifying sensor {address} ..." + '\n\n') 

    def disconnect_from_sensor(self, address):
        self.s.sensor_manager.send_message("disconnect", address)
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"disconnecting sensor {address} ..." + '\n\n') 


    def start_measuring_for_sensor(self, address):
        print(f"start measuring for sensor {address}")

        self.packet_count = 0
        self.time = []
        self.accel_x = []
        self.accel_y = []
        self.accel_z = []
        self.roll = []
        self.pitch = []
        self.yaw = []
        self.projected_pitch = []
        self.projected_roll = []
        self.projected_yaw = []
        self.prev_timestamp = 0
    
        self.ax.clear()
        self.ax_2d.clear()

        self.s.sensor_manager.send_message("start_measuring", address)
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"start measuring {address} ..." + '\n\n') 
        self.update_stream_plot()
    
    def stop_measuring_for_sensor(self, address):
        print(f"stop measuring for sensor {address}")
        self.after_cancel(self.update_stream_plot_task_id)
        self.s.sensor_manager.send_message("stop_measuring", address)
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"stop measuring {address} ..." + '\n\n') 
        self.export_button = Button(self.connected_sensor_frame,  text="export to csv", command= lambda: self.export_to_csv(address))
        self.export_button.configure(bg="#ED8E5A")
        self.export_button.grid(row=0, column=7)
        
    def export_to_csv(self, address):
        print(f"export to csv: {address}")
        self.s.sensor_manager.send_message("export", address, self.list_of_timestamps )
        self.console_frame.insert_text(f"writing sensor {address} data to csv ..." + '\n\n') 
        
    def export_to_csv_done_callback(self, address):
        print(f"export for {address} done")
        self.console_frame.clear_console()
        self.console_frame.insert_text(f"export for {address} done" + '\n\n') 
        #remove export button from grid
        self.export_button.destroy()

    def clear_and_plot(self, axis, canvas, title, x_label, x, d1, d2, d3):
        axis.clear()
        axis.set_title(title)
        axis.set_xlabel(x_label)
        axis.text(0.005, 1.05, f"Data Rate: {self.rate} Hz ", transform=axis.transAxes)
        axis.plot(x, d1)
        axis.plot(x, d2)
        axis.plot(x, d3)
        canvas.draw()





    