import socket
import sys
import platform
import json
import pprint
from datetime import datetime
import time
import subprocess
import couchdb
from multiprocessing import Process
import config

pp = pprint.PrettyPrinter(indent=4)

server = couchdb.Server()
server.resource.credentials = (config.DB_USERNAME, config.DB_PWD)
db = None

if config.DB_DELETE:
    server.delete(config.DB_NAME)
    db = server.create(config.DB_NAME)
else:
    db = server[config.DB_NAME]
print("DB Connected")
LOG_NAME = "output/log_{0}.json"
HOST_INFO = platform.uname()
print("Running on {}".format(HOST_INFO.system))

def save_reading(reading):
    db.save(reading)

def get_app(host):
    foreground_app = None
    try:
        foreground_app = subprocess.check_output(config.FG_CMD[host], stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    if host == 'Linux':
        #TODO format to extract window name
        foreground_app = foreground_app.decode().split("=")[1].strip().replace("\"","")
    elif host == 'Mac': #check this is the uname output
        foreground_app = foreground_app.decode().split("=")[1].strip().replace("\"","")
    elif host == 'Windows':
        foreground_app = foreground_app.decode().split("\\")[-1].strip().replace("\"","")
    return foreground_app

get_app(HOST_INFO.system)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
readings = []
server_address = (config.HOST, config.PORT)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)
try:
    # Send config message to mindwave
    message = "{\"enableRawOutput\": false, \"format\": \"Json\"}\n";
    # print('sending "%s"' % message)
    sock.send(config.CONFSTRING.encode('utf8'))

    # Look for the response
    while True:
        data = sock.recv(1024)
        dataform = data.decode()
        # str(data).strip("'<>() ").replace('\'', '\"').replace("b\"","").replace("\\r","")
        print(dataform)
        struct = json.loads(dataform)
        if struct:
            if ('status' in struct and struct['status'] != "scanning") or 'status' not in struct:
                d_json = struct
                #add time and foreground app to json
                d_json['time'] = str(datetime.now())
                d_json['host'] = HOST_INFO.node
                d_json['app'] = get_app(HOST_INFO.system)
                pp.pprint(d_json)
                if config.BUFFER:
                    readings.append(d_json)
                    if len(readings) > MAX_READING_BUFFER:
                        for reading in readings:
                            p = Process(target=save_reading, args=(reading,))
                            p.start()
                            p.join()
                        readings = []
                else:
                    save_reading(d_json)



#TODO add cl option for logging
except KeyboardInterrupt:
    print("Quit; saving readings")
    #with open(LOG_NAME.format(str(datetime.now())), 'w') as outfile:
    #    json.dump(readings, outfile)
        #, indent=4)
finally:
    print(sys.stderr, 'closing socket')
    sock.close()
