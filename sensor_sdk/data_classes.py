from sensor_sdk import helper_functions as hf

# Data Classes
class BatteryStatus:
    def __init__(self, battery_level, is_charging):
        self.battery_level = battery_level
        self.is_charging = is_charging


## Sensor Classes
class ScannedSensor:
    def __init__(self, address, ble_address, ble_device):
        self.address = address
        self.ble_address = ble_address
        self.ble_device = ble_device
    def get_scanned_sensor_address(self):
        return self.address
    def get_scanned_sensor_ble_device(self):
        return self.ble_device
    
class ConnectedSensor:
    def __init__(self, address, client, ble_device, sensor_manager):
        self.address = address
        self.ble_device = ble_device
        self.ble_client = client
        self.sensor_manager = sensor_manager
        self.batt_level = 0
        self.raw_data = []

    def on_sensor_data(self, sender, data):
        encoded_data = hf.encode_data_packet(data)
        self.sensor_manager.sensor_data_callback(self.address, encoded_data )
        self.add_raw_data_packet(encoded_data)
        
    def on_battery_status_update(self, sender, batt):
        battery_level = hf.get_battery_level(batt)
        self.batt_level = battery_level.battery_level
        self.sensor_manager.battery_status_callback(self.address, battery_level.battery_level)
    
    def add_raw_data_packet(self, data_packet):
        self.raw_data.append(data_packet)

    def get_raw_data(self):
        return self.raw_data

    def remove_raw_data(self):
        self.raw_data = []

