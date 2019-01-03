import threading
import time

from gatt import Device

from y5_util import dbus_to_string, checksum, int_to_byte, empty_params


class Y5(Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def characteristic_value_updated(self, characteristic, value):
        self.parse_characteristic_values(value)
        self.print_attributes()

    def characteristic_enable_notifications_succeeded(self, characteristic):
        print("Enabled notifications on {}".format(characteristic.uuid))

    def characteristic_enable_notifications_failed(self, characteristic, error):
        print("Enable notifications failed on {} for: {}".format(characteristic.uuid, error))

    def characteristic_write_value_succeeded(self, characteristic):
        self.write_lock.release()
        print("Wrote value correctly")

    def characteristic_write_value_failed(self, characteristic, error):
        self.write_lock.release()
        print("Write value failed: {}".format(error))

    def write_value(self, value, offset=0):
        print("Writing {}".format(value))
        self.write_lock.acquire()
        self.write_char.write_value(value, offset)

    def services_resolved(self):
        super().services_resolved()

        for service in self.services:
            for characteristic in service.characteristics:
                if '33f3' in characteristic.uuid:
                    self.write_char = characteristic
                if '33f4' in characteristic.uuid:
                    self.read_char = characteristic
                    characteristic.enable_notifications()

    def set_12_hour(self, hour_12):
        params = empty_params()
        params[0] = 62
        if hour_12:
            params[1] = 1
        else:
            params[1] = 0
        params[9] = checksum(params)
        self.write_value(params)

    def print_attributes(self):
        print("Steps: {}".format(self.steps))
        print("Power: {}%".format(self.power))
        print("HR: {}".format(self.current_hr))

    def parse_characteristic_values(self, value):
        if value[0] == 254:  # Sleep data
            print("Sleep data: {}".format(dbus_to_string(value)))
            pass
        elif value[0] == 253:  # Update max heart
            print("update max heart: {}".format(dbus_to_string(value)))
            pass
        elif value[0] == 252:  # Update current heart
            self.current_hr = value[8]
        elif value[0] == 247:  # Watch power (0xF7)
            self.power = value[8]
            pass
        elif value[0] == 246:  # Save settings? (0xF6)
            print("Save setting: {}".format(dbus_to_string(value)))
            pass
        elif value[0] == 245:  # Alarm?
            print("Alarm?: {}".format(dbus_to_string(value)))
            pass
        elif value[0] == 236:  # Mac address (0xEC)
            pass
        elif value[0] == 249:  # Steps (0xF9)
            self.steps = (value[5] << 24) + (value[6] << 16) + (value[7] << 8) + value[8]
            # print("Steps: {}".format(steps))
        else:
            print("Found {} with values: {}".format(value[0], dbus_to_string(value)))

    def set_units(self, english):
        if english:
            self.write_value(int_to_byte(58, 0, 1))
        else:
            self.write_value(int_to_byte(58, 0, 0))

    def set_time(self, datetimestr=None):
        if datetimestr is None:
            datetimestr = time.strftime("%Y%m%d%H%M%S")
        params = empty_params()
        params[0] = 8
        params[1] = int(datetimestr[0:2])  # First half of year
        params[2] = int(datetimestr[2:4])  # Second half of year
        params[3] = int(datetimestr[4:6]) - 1  # Month
        params[4] = int(datetimestr[6:8])  # Day
        params[5] = int(datetimestr[8:10])  # Hour
        params[6] = int(datetimestr[10:12])  # Minute
        params[7] = int(datetimestr[12:14])  # Second
        params[8] = 5  # Day of week TODO: calculate day of week
        params[9] = checksum(params)

        self.write_value(params)

    @staticmethod
    def utf8_to_array(string):
        remainder = len(string) % 16
        packets = int(len(string) / 16)
        if remainder != 0:
            packets += 1

        arr = []
        for i in range(0, packets):
            arr.append([])
            count = 3
            for byte in bytearray(string[(i * 16):(i * 16) + 16], "UTF-8"):
                arr[i].append(byte)
                count += 1
                # Need to add a zero byte at position 9
                if count == 9:
                    arr[i].append(0)
                    count += 1
            for j in range(count, 20):
                arr[i].append(0)
        return arr

    def send_msg(self, title, msg):
        remainder = len(msg) % 16
        packets = int(len(msg) / 16)
        if remainder != 0:
            packets += 1
        packets += 2

        init_packet = [44, packets, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        title_packet = [44, packets, 2] + Y5.utf8_to_array(title)[0]
        self.write_value(init_packet)
        self.write_value(title_packet)
        msg_packet_count = 3
        byte_arrs = Y5.utf8_to_array(msg)
        for byte_arr in byte_arrs:
            message_packet = [44, packets, msg_packet_count] + byte_arr
            self.write_value(message_packet)
            msg_packet_count += 1
            #count = 3
            #for byte in bytearray(msg[(i * 16):(i * 16) + 16], "UTF-8"):
            #    message_packet.append(byte)
            #    count += 1
            #    # Need to add a zero byte at position 9
            #    if count == 9:
            #        message_packet.append(0)
            #        count += 1
            #for j in range(count, 20):
            #    message_packet.append(0)
            #print("length is: {}".format(len(message_packet)))

    def tick(self):
        self.write_value(int_to_byte(13, 0, 1))

    def __init__(self, mac_address, manager, managed=True):
        super().__init__(mac_address, manager, managed)
        self.steps = 0
        self.power = 0
        self.current_hr = 0
        self.write_char = None
        self.read_char = None
        self.write_lock = threading.Lock()
