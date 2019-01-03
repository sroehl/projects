def dbus_to_string(dbus_bytes):
    string = ''
    for byte in dbus_bytes:
        raw = hex(byte)
        # print("raw: |{}|".format(raw))
        raw = raw.replace("\\x", "")
        raw += " "
        string += raw
    return string


def int_to_byte(byte, int1, int2):
    arr = [byte, (int1 >> 24 & 0xFF), (int1 >> 16 & 0xFF), (int1 >> 8 & 0xFF), (int1 & 0xFF), (int2 >> 24 & 0xFF),
           (int2 >> 16 & 0xFF), (int2 >> 8 & 0xFF), (int2 & 0xFF)]
    arr.append(checksum(arr))
    byte_arr = []
    # for val in arr:
    #    byte_arr.append(byte(val))
    return arr


def checksum(arr):
    sum = 0
    for i in range(0, 9):
        sum += arr[i]
    sum &= 0xFF
    return sum


def empty_params():
    params = []
    for i in range(0, 10):
        params.append(0)
    return params
