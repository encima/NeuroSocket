import serial
import codecs
import base64
import couchdb
import config
from datetime import datetime

server = couchdb.Server()
server.resource.credentials = (config.DB_USERNAME, config.DB_PWD)
db = None
log_file = None
try:
    db = server['mindwave_logs']
except:
    db = server.create('mindwave_logs')
print("DB Connected")

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
    print(code)
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
        print("Unknown code")

def handle_load(payload):
    i = 0
    while i < len(payload):
        code = payload[i]
        # parse_payload(payload)
        if (code == 'd0'):
            print("Headset connected!")
        elif (code == 'd1'):
            print("Headset not found, reconnecting")
        elif(code == 'd2'):
            print("Disconnected!")
        elif(code == 'd3'):
            print("Headset denied operation!")
        elif(code == 'd4'):
            if payload[2] == 0:
                print("Idle, trying to reconnect")
        elif(code == CODES['POOR_SIGNAL']['code']):  # poorSignal
            i = i + 1
            poor_signal = int(payload[i].hex(), 16)
            print('POOR SIGNAL', poor_signal)
        elif(code == CODES['ATTENTION']['code']):  # attention
            i = i + 1
            attention = int(payload[i].hex(), 16)
            print('ATTENTION', attention)
        elif(code == CODES['MEDITATION']['code']):  # meditation
            i = i + 1
            meditation = int(payload[i].hex(), 16)
            print('MEDITATION', meditation)
        elif(code == CODES['BLINK']['code']):  # blink strength
            i = i + 1
            blink_strength = int(payload[i].hex(), 16)
            print('BLINK', blink_strength)
        elif(code == CODES['RAW_VALUE']['code']):  # raw value
            i = i + 1  # for length/it is not used since length =1 byte long and always=2
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            raw_value = val0 * 256 + int(payload[i].hex(), 16)
            if raw_value > 32768:
                raw_value = raw_value - 65536
            # print('RAW', raw_value)
        elif(code == CODES['ASIC_EEG_POWER']['code']):  # ASIC_EEG_POWER
            w = {}
            i = i + 1  # for length/it is not used since length =1 byte long and always=2
            # delta:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['delta'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # theta:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['theta'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # lowAlpha:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['lowAlpha'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # highAlpha:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['highAlpha'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # lowBeta:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['lowBeta'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # highBeta:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['highBeta'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # lowGamma:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['lowGamma'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            # midGamma:
            i = i + 1
            val0 = int(payload[i].hex(), 16)
            i = i + 1
            val1 = int(payload[i].hex(), 16)
            i = i + 1
            w['midGamma'] = val0 * 65536 + \
                val1 * 256 + int(payload[i].hex(), 16)
            print(w)
            w['recorded'] = datetime.today()
            db.save(w)

        else:
            pass
        i = i + 1


while True:
    if ser.read(1) == CODES['SYNC']['code']:
        if ser.read(1) == CODES['SYNC']['code']:
            plength = ord(ser.read(1))
            if plength > 170:
                break
            # Read in the payload
            
            payload = []
            val = 0
            for i in range(plength):
                t = ser.read(1)
                val += sum(x for x in t)
                payload.append(t)
            # Verify its checksum
            # val = sum(b for b in payload)
            val &= 0xff
            val = ~val & 0xff
            chksum = ord(ser.read(1))
            if val ==  chksum:
                handle_load(payload)
            else:
                print('Bad checksum')

