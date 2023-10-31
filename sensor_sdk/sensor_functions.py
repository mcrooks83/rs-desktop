from bleak import BleakClient
from sensor_sdk import helper_functions as hf
from sensor_sdk import data_classes as dc
from sensor_sdk import constants as c
from datetime import datetime


async def discover_sensors(sensor_manager):
    sensor_manager.remove_all_scanned_sensors()
    sensors = await hf.discover_sensors()
    scanned_sensors = []
    if(sensors):
        for s, a in sensors.values():
            if( len(list(a.manufacturer_data.keys())) != 0 and list(a.manufacturer_data.keys())[0] == c.manufacturer_id ):
                mac_address = hf.get_mac_address(a.manufacturer_data[2182].hex())
                scanned_sensor = dc.ScannedSensor(mac_address, s.address, s)
                scanned_sensors.append(scanned_sensor)
    return scanned_sensors

async def connect_to_sensor(sensor_manager, address):
    #find device in scanned sensors 
    sensor = list(filter(lambda x: x.address == address, sensor_manager.scanned_sensors))[0]
    device = BleakClient(sensor.ble_device, loop=sensor_manager.loop)
    await device.connect()

    connected_sensor = dc.ConnectedSensor(sensor.address, device, sensor.ble_device, sensor_manager)
    sensor_manager.connected_sensors.append(connected_sensor)

    await device.start_notify(c.long_payload_char_uuid, connected_sensor.on_sensor_data )
    #read initial battery
    batt = await device.read_gatt_char(c.BLE_UUID_BATTERY_LEVEL, response=True)
    connected_sensor.on_battery_status_update(connected_sensor.address, batt)
    # subscribe to battery status
    await device.start_notify(c.BLE_UUID_BATTERY_LEVEL, connected_sensor.on_battery_status_update)

    return connected_sensor

async def disconnect_from_sensor(sensor_manager, address):
    sensor = list(filter(lambda x: x.address == address, sensor_manager.connected_sensors))[0]
    disconnected = await sensor.ble_client.disconnect()
    return disconnected

async def start_measuring(sensor_manager, address):
    sensor = list(filter(lambda x: x.address == address, sensor_manager.connected_sensors))[0]
    print("Sensor", sensor)
    if(sensor):    
        print("Writing the start gatt char")
        await sensor.ble_client.write_gatt_char(c.measurement_char_uuid, c.start_control_char, response=True)

async def stop_measuring(sensor_manager, address):
    sensor = list(filter(lambda x: x.address == address, sensor_manager.connected_sensors))[0]
    #await sensor.ble_client.stop_notify(c.long_payload_char_uuid)
    await sensor.ble_client.write_gatt_char(c.measurement_char_uuid, c.stop_control_char, response=True)
    sensor_manager.stop_sensor_callback(sensor.address)

async def indentify_sensor(sensor_manager, address):
    sensor = list(filter(lambda x: x.address == address, sensor_manager.connected_sensors))[0]
    await sensor.ble_client.write_gatt_char(c.BLE_UUID_DEVICE_CONTROL, c.device_control_indentify_char, response=True)
    #control = await sensor.ble_client.read_gatt_char(c.BLE_UUID_DEVICE_CONTROL, response=True)  
    
async def export_to_csv(sensor_manager, address, list_of_timestamps):
    # should export all active sensors.  currently there is only one so use the address to find it.
    sensor = list(filter(lambda x: x.address == address, sensor_manager.connected_sensors))[0]
    data_to_write_to_csv = sensor.get_raw_data()

    modified_address = address.replace(":", "_")

    now = int(datetime.timestamp(datetime.now()) * 1000)
    csv_file_name = f'{now}_{modified_address}.csv'
    row_headers = c.csv_header

    hf.check_and_create_export_diretort(c.export_dir)

    done = hf.write_data_to_csv(c.export_dir, csv_file_name, row_headers, data_to_write_to_csv, list_of_timestamps)
    
    if(done):
        # remove raw data
        sensor.remove_raw_data()
        sensor_manager.export_to_csv_done_callback(sensor.address)

    