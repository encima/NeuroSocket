import serial
import codecs
import base64

CONNECT              = b'\xc0'
DISCONNECT           = b'\xc1'
AUTOCONNECT          = b'\xc2'
SYNC                 = b'\xaa'
EXCODE               = b'\x55'
BATTERY              = b'\x01'
POOR_SIGNAL          = b'\x02'
ATTENTION            = b'\x04'
MEDITATION           = b'\x05'
BLINK                = b'\x16'
HEADSET_CONNECTED    = b'\xd0'
HEADSET_NOT_FOUND    = b'\xd1'
HEADSET_DISCONNECTED = b'\xd2'
REQUEST_DENIED       = b'\xd3'
STANDBY_SCAN         = b'\xd4'
RAW_VALUE = '\x80'
EEG_POWER = '\x81'
ASIC_EEG_POWER = '\x83'

port = "/dev/rfcomm0"
ser = serial.Serial(port, 38400)
s = ser.read(100)

ser.flushInput()

def decode(bytes, order = 'big',):
    print(int.from_bytes(bytes, byteorder=order, signed=False))

def parse_payload(payload):
    """Parse the payload to determine an action."""
    while payload:
        # Parse data row
        excode = 0
        packets = payload.split(b'\xaa\xaa')
        for p in packets:
            if len(p) > 0:
                print(p)
                try:
                    code, payload = p[0], p[1:]
                except IndexError:
                    pass
                while code == ord(EXCODE):
                    # Count excode bytes
                    excode += 1
                    try:
                        code, payload = p[0], p[1:]
                    except IndexError:
                        pass
                if code < 0x80:
                    # This is a single-byte code
                    try:
                        value, payload = p[0], p[1:]
                    except IndexError:
                        pass
                    if code == ord(POOR_SIGNAL):
                        # Poor signal
                        pass
                    elif code == ord(BATTERY):
                        pass
                        # print(ord(value))
                    elif code == ord(ATTENTION):
                        # Attention level
                        pass
                        # print('ATTENTION {}'.format(ord(value)))
                    elif code == ord(MEDITATION):
                        # Meditation level
                        pass
                        # print('MEDITATION {}'.format(ord(value)))
                    elif code == ord(BLINK):
                        # Blink strength
                        pass
                        # print('BLINK {}'.format(ord(value)))
                else:
                    # This is a multi-byte code
                    try:
                        vlength, payload = payload[0], payload[1:]
                    except IndexError:
                        continue
                    value, payload = payload[:vlength], payload[vlength:]
                    # Multi-byte EEG and Raw Wave codes not included
                    # Raw Value added due to Mindset Communications Protocol
                    if code == ord(RAW_VALUE):
                        raw = 0
                        raw=value[0]*256+value[1]
                        if (raw>=32768):
                            raw=raw-65536
                        print('Raw Value: {}'.format(raw))
                    elif code == ord(EEG_POWER):
                        print(payload)
                        vals = value.split(b'\xaa\xaa')
                        print('EEG', len(value), vals, len(vals))
                        print(decode(value))
                        # for v in vals:
                        #     if len(v) > 0:
                        #         decode(v)
                    elif code == ord(ASIC_EEG_POWER):
                        print(value)
                        print(payload)
                        vals = value.split(b'\xaa\xaa')
                        print('ASIC', len(value), vals, len(vals))
                        # for v in vals:
                        #     if len(v) > 0:
                        #         decode(v)
                        # converted = int.from_bytes(value, byteorder='big', signed=False)
                        #print(converted)
                        #vals = struct.unpack("<I", value[0])[0]
                        #print(vals)
                    elif code == ord(HEADSET_CONNECTED):
                        # Headset connect success
                        # print('HEADSET CONNECTED')
                        pass
                    elif code == ord(HEADSET_NOT_FOUND):
                        # Headset not found
                        # print('HEADSET NOT FOUND')
                        pass
                    elif code == ord(HEADSET_DISCONNECTED):
                        # Headset disconnected
                        headset_id = value.encode('hex')
                        # print('DISCONNECTED')
                        pass
                    elif code == ord(REQUEST_DENIED):
                        # Request denied
                        # print('DENIED')
                        pass
                    elif code == ord(STANDBY_SCAN):
                        # Standby/Scan mode
                        try:
                            byte = ord(value[0])
                        except IndexError:
                            byte = None
                        if byte:
                            print('SCANNING')
                        else:
                            print('STANDBY')

print('Reading...')
while True:
    if ser.read() == SYNC:
         while True:
            plength = ord(ser.read())
            if plength != 170:
                break
            if plength > 170:
                continue

            # Read in the payload
            payload = ser.read(plength)

            # Verify its checksum
            val = sum(b for b in payload[:-1])
            # val &= 0xff
            # val = ~val & 0xff
            # chksum = ord(ser.read())

            #if val == chksum:
            if True: # ignore bad checksums
                parse_payload(payload)
            else:
                print('Bad checksum')
