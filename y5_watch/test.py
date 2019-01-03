import threading
import signal
import time
import sys
from Y5 import Y5
from gatt import Device, DeviceManager
from y5_util import dbus_to_string, int_to_byte, checksum

manager = DeviceManager(adapter_name='hci0')


def signal_handler(sig, frame):
    print("caught exception")
    manager.stop()
    device.disconnect()
    time.sleep(0.5)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

device = Y5(mac_address='71:59:87:7b:12:29', manager=manager)
device.connect()

#manager.run()
t = threading.Thread(target=manager.run)

t.start()
while device.write_char is None:
    time.sleep(1)

#device.set_units(True)
#device.set_12_hour(True)
#device.set_time()
#device.tick()
device.send_msg("TestTitle", "This is a test message!")
t.join(0)
manager.stop()
device.disconnect()

# while True:
#    time.sleep(1)
