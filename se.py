import serial
import codecs
import base64

CONNECT              = '\xc0'
DISCONNECT           = '\xc1'
AUTOCONNECT          = '\xc2'
SYNC                 = '\xaa'
EXCODE               = '\x55'
POOR_SIGNAL          = '\x02'
ATTENTION            = '\x04'
MEDITATION           = '\x05'
BLINK                = '\x16'
HEADSET_CONNECTED    = '\xd0'
HEADSET_NOT_FOUND    = '\xd1'
HEADSET_DISCONNECTED = '\xd2'
REQUEST_DENIED       = '\xd3'
STANDBY_SCAN         = '\xd4'
RAW_VALUE = '\x80'
ASIC_EEG_POWER = '\x83'

port = "/dev/rfcomm0"
ser = serial.Serial(port, 38400)
s = ser.read(100)

ser.flushInput()

def parse_payload(payload):
    """Parse the payload to determine an action."""
    while payload:
        # Parse data row
        excode = 0
        try:
            code, payload = payload[0], payload[1:]
        except IndexError:
            pass
        while code == EXCODE:
            # Count excode bytes
            excode += 1
            try:
                code, payload = payload[0], payload[1:]
            except IndexError:
                pass
        if ord(code) < 0x80:
            # This is a single-byte code
            try:
                value, payload = payload[0], payload[1:]
            except IndexError:
                pass
            if code == POOR_SIGNAL:
                # Poor signal
                pass
            elif code == ATTENTION:
                # Attention level
                pass
                # print('ATTENTION {}'.format(ord(value)))
            elif code == MEDITATION:
                # Meditation level
                pass
                # print('MEDITATION {}'.format(ord(value)))
            elif code == BLINK:
                # Blink strength
                pass
                # print('BLINK {}'.format(ord(value)))
        else:
            # This is a multi-byte code
            try:
                vlength, payload = ord(payload[0]), payload[1:]
            except IndexError:
                continue
            value, payload = payload[:vlength], payload[vlength:]
            # Multi-byte EEG and Raw Wave codes not included
            # Raw Value added due to Mindset Communications Protocol
            if code == RAW_VALUE:
                raw=ord(value[0])*256+ord(value[1])
                if (raw>=32768):
                    raw=raw-65536
                print('Raw Value: {}'.format(raw))
            elif code == ASIC_EEG_POWER:
                eeg = ord(value[0])
                print(ord(value[0]), ord(value[1]))
            elif code == HEADSET_CONNECTED:
                # Headset connect success
                print('HEADSET CONNECTED')
            elif code == HEADSET_NOT_FOUND:
                # Headset not found
                print('HEADSET NOT FOUND')
            elif code == HEADSET_DISCONNECTED:
                # Headset disconnected
                headset_id = value.encode('hex')
                print('DISCONNECTED')
            elif code == REQUEST_DENIED:
                # Request denied
                print('DENIED')
            elif code == STANDBY_SCAN:
                # Standby/Scan mode
                try:
                    byte = ord(value[0])
                except IndexError:
                    byte = None
                if byte:
                    print('SCANNING')
                else:
                    print('STANDBY')


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
            val = sum(ord(b) for b in payload[:-1])
            val &= 0xff
            val = ~val & 0xff
            chksum = ord(ser.read())

            #if val == chksum:
            if True: # ignore bad checksums
                parse_payload(payload)
