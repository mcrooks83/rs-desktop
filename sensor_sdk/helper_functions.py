from bleak import BleakScanner
import numpy as np
from sensor_sdk import data_classes as dc
from os import chdir, mkdir,listdir,remove,getcwd, makedirs
from os.path import splitext, isdir, exists
import csv
import math

########################################################################
# helper functions
########################################################################

toDeg = 180 / math.pi

def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # radians converted to degrees


def get_mac_address(id):
    return ":".join(list(reversed([id[i:i + 2] for i in range(0, len(id), 2)]))).upper()

#device = await BleakScanner.find_device_by_filter(lambda d, ad: d.name and d.name.lower() == GLOVEName.lower())
async def discover_sensors():
    devices = await BleakScanner.discover( return_adv=True)
    return devices

def get_battery_level(batt_bytes):
    segments = np.dtype([
        ("level", np.int8),
        ("charging", np.int8),

    ])
    battry_level = np.frombuffer(batt_bytes, dtype=segments)[0]
    is_charging = False
    if(battry_level[1]==0):
        is_charging=False
    else:
        is_charging=True
    batt = dc.BatteryStatus(battry_level[0], is_charging)
    return batt

# data format Custom mode 5
#   Timestamp 4 bytes
#   Quaternions 16 bytes (4 per value)
#   Acceleration 12 bytes (4 per value)
#   Angular velocity 12 bytes (4 per value)

def encode_data_packet(bytes_):

    data_segments = np.dtype([
        ('timestamp', np.uint32),
        ('q_w', np.float32),
        ('q_x', np.float32),
        ('q_y', np.float32),
        ('q_z', np.float32),
        ('acc_x', np.float32),
        ('acc_y', np.float32),
        ('acc_z', np.float32),
        ('gyr_x', np.float32),
        ('gyr_y', np.float32),
        ('gyr_z', np.float32),
        ("zero_0", np.int64),
        ("zero_1", np.int64),
        ("zero_2", np.int16),
        ("zero_3", np.int8),
        ])
    formatted_data = np.frombuffer(bytes_, dtype=data_segments)
    return formatted_data


def check_and_create_export_diretort(dir):
    if not exists(dir):
        makedirs(dir)
        print(f"Export directory '{dir}' created successfully in the current working directory!")
    else:
        print(f"Export directory '{dir}' already exists in the current working directory.")

def write_data_to_csv(export_dir, csv_file_name, row_headers, data_to_write):
        with open(export_dir + "/" + csv_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_headers)  # Write the header row
            for row in data_to_write:
                row_to_write = []
                #custom payload 5 has 11 pieces
                for d in range(11):
                    row_to_write.append(row[0][d])
                writer.writerow(row_to_write)

        return True