
import numpy as np
import asyncio
from sensor_sdk import helper_functions as hf
from sensor_sdk import data_classes as dc
from sensor_sdk import sensor_functions as sf
import threading


####################################################################
## Sensor Manager
####################################################################
class SensorManager:
    def __init__(self, data_callback, connected_callback, disconnected_callback, battery_status_callback, discover_callback, stop_callback, init_callback, export_to_csv_done_callback):
        # sensor manager data
        self.scanned_sensors = []
        self.connected_sensors = []

        # configuration
        self.data_rate = 60

        # Initialize callbacks - one for all sensors
        self.sensor_data_callback = None
        self.sensor_connected_callback = None
        self.sensor_disconnected_callback = None
        self.battery_status_callback = None
        self.sensor_init_callback = None
        self.discover_sensor_callback = None
        self.stop_sensor_callback = None
        self.export_to_csv_done_callback = None

        self.running = False

        # Create a thread to run the SensorManager
        thread = threading.Thread(target=self.run_manager_loop)
        thread.start()

        self.intialise_sensor_callbacks(data_callback, connected_callback, disconnected_callback, battery_status_callback, discover_callback, stop_callback, init_callback, export_to_csv_done_callback)

    def intialise_sensor_callbacks(self,data_callback, connected_callback, disconnected_callback, battery_status_callback, discover_callback, stop_callback, init_callback, export_to_csv_done_callback):
        self.sensor_data_callback = data_callback
        self.sensor_connected_callback = connected_callback
        self.sensor_disconnected_callback = disconnected_callback
        self.battery_status_callback = battery_status_callback
        self.sensor_init_callback = init_callback
        self.discover_sensor_callback = discover_callback
        self.stop_sensor_callback = stop_callback
        self.export_to_csv_done_callback = export_to_csv_done_callback

    def run_manager_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.message_queue = asyncio.Queue()
        self.loop.run_until_complete(self.manager_loop())
    
    def send_message(self, msg, address):
        print(f"Received message from client: {msg} from {address}")
        self.loop.call_soon_threadsafe(self.message_queue.put_nowait, {"message": msg, "address": address,})
       
    def add_scanned_sensors(self, s):
        self.scanned_sensors = s

    def get_scanned_sensors(self):
        return self.scanned_sensors

    def remove_all_scanned_sensors(self):
        self.scanned_sensors = []   

    def add_connected_sensor(self, s):
        self.connected_sensors.append(s) 

    def remove_all_connected_sensors(self):
        self.connected_sensors = []

    def remove_single_connected_sensor(self, address):
        #filter out the one to remove
        connected_sensors = list(filter(lambda x: x.address != address, self.connected_sensors))
        self.connected_sensors = connected_sensors 
        print("removed", connected_sensors)   

    def set_data_rate(self, rate):
        self.data_rate = rate
    
    def get_data_rate(self):
        return self.data_rate
    
    async def manager_loop(self):
        self.running = True
        while self.running:

            msg = await self.message_queue.get()
            print(msg, flush=True)
            #Scanning for sensors
            if msg["message"] == "scan":
                scanned_sensors = await sf.discover_sensors(self)  
                self.add_scanned_sensors(scanned_sensors)
                self.discover_sensor_callback(self.scanned_sensors) 

            #connecting to a sensor
            elif msg["message"] == "connect":
                connected_sensor = await sf.connect_to_sensor(self, msg["address"])
                if(connected_sensor):
                    self.sensor_connected_callback(connected_sensor)

            # disconnect a sensor
            elif msg["message"] == "disconnect":
                disconnected = await sf.disconnect_from_sensor(self, msg["address"])
                if(disconnected):
                    self.remove_single_connected_sensor(msg["address"])
                    self.sensor_disconnected_callback(msg["address"])

            # start measuring
            elif(msg["message"] == "start_measuring"):
                await sf.start_measuring(self, msg["address"])    

            # stop measuring
            elif(msg["message"] == "stop_measuring"):
                print("stop measuring", flush=True)
                await sf.stop_measuring(self, msg["address"])
                
            # identify a sensor
            elif(msg["message"] == "identify"):
                await sf.indentify_sensor(self, msg["address"])

            elif(msg["message"] == "export"):
                await sf.export_to_csv(self, msg["address"])
                
            elif msg["message"] == "quit":
                self.running = False

   



    



