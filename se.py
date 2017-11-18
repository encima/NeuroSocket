import serial
import codecs
import base64

CODES = {
    'CONNECT': {'code': b'\xc0', 'length': 0},
    'DISCONNECT': {'code': b'\xc1', 'length': 0},
    'AUTOCONNECT': {'code': b'\xc2', 'length': 0},
    'SYNC': {'code': b'\xaa', 'length': 0},
    'EXCODE': {'code': b'\x55', 'length': 0},
    'BATTERY': {'code': b'\x01', 'length': 0},
    'POOR_SIGNAL': {'code': b'\x02', 'length': 0},
    'ATTENTION': {'code': b'\x04', 'length': 1},
    'MEDITATION': {'code': b'\x05', 'length': 1},
    'BLINK': {'code': b'\x16', 'length': 1},
    'HEADSET_CONNECTED': {'code': b'\xd0', 'length': 0},
    'HEADSET_NOT_FOUND': {'code': b'\xd1', 'length': 0},
    'HEADSET_DISCONNECTED': {'code': b'\xd2', 'length': 0},
    'REQUEST_DENIED': {'code': b'\xd3', 'length': 0},
    'STANDBY_SCAN': {'code': b'\xd4', 'length': 0},
    'RAW_VALUE': {'code': b'\x80', 'length': 2},
    'EEG_POWER': {'code': b'\x81', 'length': 32},
    'ASIC_EEG_POWER': {'code': b'\x83', 'length': 24}
}


port = "/dev/rfcomm0"
ser = serial.Serial(port, 38400)
s = ser.read(100)

ser.flushInput()


def decode(bytes, order='big',):
    print(int.from_bytes(bytes, byteorder=order, signed=False))


def parse_payload(payload):
    """Parse the payload to determine an action.
       Sample payload: \x04\x80\x02\x01\xe1\x9b
    """
    print(payload)
    code = ord(payload[0])
    if code in CODES:
        print(code)
        length = CODES[code]['length']
        if length == 1:
            value = payload[1:2]
            if value:
                print(ord(value))
        elif length > 1:
            print(decode(payload[1:1+length]))
        parse_payload(payload[1 + length:])
    else:
        Print("Unknown code")


while True:
    if ser.read(1) == CODES['SYNC']['code']:
        if ser.read(1) == CODES['SYNC']['code']:
            plength = ord(ser.read(1))
            if plength > 170:
                break
            # Read in the payload
            
            payload = b''
            for i in range(plength):
                t = ser.read(1)
                payload += t
            # Verify its checksum
            val = sum(b for b in payload)
            val &= 0xff
            val = ~val & 0xff
            chksum = ord(ser.read(1))
            if val ==  chksum:
                parse_payload(payload)
            else:
                print('Bad checksum')

