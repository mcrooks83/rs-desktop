from sensor_sdk.SensorManager import SensorManager as sm
import time

class Sensors:
    def __init__(self):
        # sensor manager data
        self.sensor_manager = sm(self.on_sensor_data_received, 
                                self.on_sensor_connected, 
                                self.on_sensor_disconnected, 
                                self.on_battery_status_update, 
                                self.on_scanned_sensors, 
                                self.on_sensor_stop_measuring, 
                                self.on_sensor_init,
                                self.on_export_to_csv_done )
        
        self.discovered_sensors = None
        self.connected_sensor = None
        self.sensor_data = None
        self.stop_sensor_data = None
        self.battery_status = None
        self.export_done_callback = None

    def set_discovered_sensors_callback(self, func):
        self.discovered_sensors = func
    
    def set_connected_sensors_callback(self, func):
        self.connected_sensor = func

    def set_sensor_data_callback(self, func):
        self.sensor_data = func
    
    def set_stop_sensor_data_callback(self, func):
        self.stop_sensor_data = func

    def set_battery_status_callback(self, func):
        self.battery_status = func

    def set_export_done_callback(self, func):
        self.export_done_callback = func
    '''
    def test_sensor_manager(self):
         # start a scan
        self.sensor_manager.send_message("scan", {})
        print("sleeping for 10 seconds")
        time.sleep(10)
        scanned_sensors = self.sensor_manager.get_scanned_sensors()
        if(len(scanned_sensors)> 0):
            print('connecting to a sensor')
            self.sensor_manager.send_message("connect", scanned_sensors[0].get_scanned_sensor_address())
        print("sleeping for 5 seconds")
        time.sleep(5)
         #sensor_manager.send_message("start_measuring",sensor.address)
        self.sensor_manager.send_message("identify", self.sensor_manager.connected_sensors[0].address)
    '''
    # sensor manager callbacks
    def on_sensor_init(self, address):
        print(f"sensor {address} initialised")

    def on_battery_status_update(self,address, batt_level):
        print(f"{address} {batt_level}")
        self.battery_status(address, batt_level)

    def on_sensor_stop_measuring(self, address):
        print(f"sensor {address} stopped")
        self.stop_sensor_data(address)

    def on_sensor_data_received(self,address, data):
        self.sensor_data(address, data)

    def on_scanned_sensors(self,sensors):
        print(f"Discovered Sensors {sensors}", flush=True)
        self.discovered_sensors(sensors)
    
    def on_sensor_connected(self, sensor):
        print(f"Connected Sensor {sensor.address}")
        self.connected_sensor(sensor)

    def on_sensor_disconnected(self, sensor):
        print(f"disconnected from {sensor}", flush=True)

    def on_export_to_csv_done(self, address):
        print(f"export to csv done for {address}")
        self.export_done_callback(address)


