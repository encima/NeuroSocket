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


def split_on_code(payload):
    packets = []
    if len(payload) > 4:
        print(payload)
    # for p in range(0, len(payload)):
    #     for k in CODES:
    #         if payload[p] == ord(CODES[k]['code']):
    #             print(k)
    #             length = CODES[k]['length']
    #             if length == 1:
    #                 value = payload[p+1:(p+1)+length]
    #                 if value:
    #                     print(ord(value))
    #             elif length > 1:
    #                 print(decode(payload[(p+1):(p+1)+length]))


def parse_payload(payload):
    """Parse the payload to determine an action.
       Sample payload: \x04\x80\x02\x01\xe1\x9b\xaa\xaa\x04\x80\x02\x01\xe5\x97\xaa\xaa\x04\x80\x02\x01\xcc\xb0\xaa\xaa\x04\x80\x02\x01\xaa\xd2\xaa\xaa\x04\x80\x02\x01\x96\xe6\xaa\xaa\x04\x80\x02\x01\x9a\xe2\xaa\xaa\x04\x80\x02\x01\xa8\xd4\xaa\xaa\x04\x80\x02\x01\xad\xcf\xaa\xaa\x04\x80\x02\x01\xa5\xd7\xaa\xaa\x04\x80\x02\x01\x89\xf3\xaa\xaa\x04\x80\x02\x01X$\xaa\xaa\x04\x80\x02\x01$X\xaa\xaa\x04\x80\x02\x01\x05w\xaa\xaa\x04\x80\x02\x00\xf9\x84\xaa\xaa\x04\x80\x02\x00\xf8\x85\xaa\xaa\x04\x80\x02\x00\xe4\x99\xaa\xaa\x04\x80\x02\x00\xb3\xca\xaa\xaa\x04\x80\x02\x00w\x06\xaa\xaa\x04\x80\x02\x00L1\xaa\xaa\x04\x80\x02\x006G\xaa\xaa\x04\x80\x02\x00\x18e\xaa\xaa\x04\x80
    """
    while payload:
        # Parse data row
        print(payload)
        # for p in payload:
        #     if len(p) > 0:
        #         split_on_code(p)
        #         pass
                # try:
                #     code, payload = p[0], p[1:]
                # except IndexError:
                #     pass
                # while code == ord(CODES['EXCODE']['code']):
                #     # Count excode bytes
                #     excode += 1
                #     try:
                #         code, payload = p[0], p[1:]
                #     except IndexError:
                #         pass
                # if code < 0x80:
                #     # This is a single-byte code
                #     try:
                #         value, payload = p[0], p[1:]
                #     except IndexError:
                #         pass
                #     if code == ord(CODES['POOR_SIGNAL']['code']):
                #         # Poor signal
                #         pass
                #     elif code == ord(CODES['BATTERY']['code']):
                #         pass
                #         # print(ord(value))
                #     elif code == ord(CODES['ATTENTION']['code']):
                #         # Attention level
                #         pass
                #         # print('ATTENTION {}'.format(ord(value)))
                #     elif code == ord(CODES['MEDITATION']['code']):
                #         # Meditation level
                #         pass
                #         # print('MEDITATION {}'.format(ord(value)))
                #     elif code == ord(CODES['BLINK']['code']):
                #         # Blink strength
                #         pass
                #         # print('BLINK {}'.format(ord(value)))
                # else:
                #     # This is a multi-byte code
                #     try:
                #         vlength, payload = payload[0], payload[1:]
                #     except IndexError:
                #         continue
                #     value, payload = payload[:vlength], payload[vlength:]
                #     if code == ord(CODES['RAW_VALUE']['code']):
                #         raw = 0
                #         raw = value[0] * 256 + value[1]
                #         if (raw >= 32768):
                #             raw = raw - 65536
                #         print('Raw Value: {}'.format(raw))
                #     elif code == ord(CODES['EEG_POWER']['code']):
                #         print('EEG', len(value), value)
                #         print(decode(value))
                #         # for v in vals:
                #         #     if len(v) > 0:
                #         #         decode(v)
                #     elif code == ord(CODES['ASIC_EEG_POWER']['code']):
                #         print('ASIC', len(value), value)
                #         # for v in vals:
                #         #     if len(v) > 0:
                #         #         decode(v)
                #         # converted = int.from_bytes(value, byteorder='big', signed=False)
                #         # print(converted)
                #         #vals = struct.unpack("<I", value[0])[0]
                #         # print(vals)
                #     elif code == ord(CODES['HEADSET_CONNECTED']['code']):
                #         # Headset connect success
                #         # print('HEADSET CONNECTED')
                #         pass
                #     elif code == ord(CODES['HEADSET_NOT_FOUND']['code']):
                #         # Headset not found
                #         # print('HEADSET NOT FOUND')
                #         pass
                #     elif code == ord(CODES['HEADSET_DISCONNECTED']['code']):
                #         # Headset disconnected
                #         headset_id = value.decode('hex')
                #         # print('DISCONNECTED')
                #         pass
                #     elif code == ord(CODES['REQUEST_DENIED']['code']):
                #         # Request denied
                #         # print('DENIED')
                #         pass
                #     elif code == ord(CODES['STANDBY_SCAN']['code']):
                #         # Standby/Scan mode
                #         try:
                #             byte = ord(value[0])
                #         except IndexError:
                #             byte = None
                #         if byte:
                #             print('SCANNING')
                #         else:
                #             print('STANDBY')


print('Reading...')


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
