BLE_UUID_BATTERY_LEVEL      = "15173001-4947-11e9-8646-d663bd873d93"
BLE_UUID_DEVICE_CONTROL     = "15171002-4947-11e9-8646-d663bd873d93"
measurement_char_uuid       = "15172001-4947-11e9-8646-d663bd873d93"

long_payload_char_uuid      = "15172002-4947-11e9-8646-d663bd873d93"
medium_payload_char_uuid    = "15172003-4947-11e9-8646-d663bd873d93"
short_payload_char_uuid     = "15172004-4947-11e9-8646-d663bd873d93"

device_control_output_rate_char = b"\x05\x00\x3C"
device_control_indentify_char = b"\x01\01"
start_control_char = b"\x01\x01\x1A"
stop_control_char = b"\x01\x00\x1A"

manufacturer_id = 2182
device_control_indentify_char =  b'\x01\x01\x02\n\x00\x1e\x00\tXsens DOT\x00\x00\x00\x00\x00\x00\x00<\x00\x00\x00\x00\x00\x00\x00'
device_control_output_rate_20_char =  b'\x04\x00\x02\n\x00\x1e\x00\tXsens DOT\x00\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00'
device_control_output_rate_60_char =  b'\x04\x00\x02\n\x00\x1e\x00\tXsens DOT\x00\x00\x00\x00\x00\x00\x00\x3C\x00\x00\x00\x00\x00\x00'

# for custom payload 5 
csv_header = ["timestamp", "q_w", "q_x", "q_y", "q_z", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z" ]
export_dir = "exports"


