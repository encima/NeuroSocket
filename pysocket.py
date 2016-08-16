import socket
import sys
from thread import *
import threading
import json
import pprint
from datetime import datetime
import time
import subprocess
import couchdb
from multiprocessing import Process

pp = pprint.PrettyPrinter(indent=4)

server = couchdb.Server()
server.resource.credentials = ("encima", "Cocaine5Unicorn_Hiatus")
#print(server.login('encima', 'Cocaine6Unicorn_Hiatus'))
server.delete('mindwave_logs')
db = server.create('mindwave_logs')
print(server)

#db = server['mindwave_logs']

HOST = '127.0.0.1'   # Symbolic name meaning all available interfaces
PORT = 13854 # Default mindwave port
LOG_NAME = "output/log_{0}.json"
MAX_READING_BUFFER = 2
FG_CMD = "lsappinfo info -only name `lsappinfo front`"

class LogSaver(threading.Thread):
    def __init__(self, readings, db):
        self.readings = readings
        self.db = db
        threading.Thread.__init__ (self)
    
    def run(self):
        for reading in self.readings:
            self.db.save(reading)
            time.sleep(2)

def save_reading(reading):
    db.save(reading)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
readings = []
server_address = (HOST, PORT)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)
try:
    # Send config message to mindwave
    message = "{\"enableRawOutput\": false, \"format\": \"Json\"}\n";
    print('sending "%s"' % message)
    sock.sendall(message)

    # Look for the response
    
    while True:
        data = sock.recv(1024)
        if data:
            d_json = json.loads(data)
            #add time and foreground app to json 
            d_json['time'] = str(datetime.now())
            foreground_app = subprocess.check_output(FG_CMD, stderr=subprocess.STDOUT, shell=True)
            foreground_app = foreground_app.split("=")[1].strip().replace("\"","")
            d_json['app'] = foreground_app
            pp.pprint(d_json)
            #TODO check for write speed, maybe batch writes after readings size is a set value?
            readings.append(d_json)
            if len(readings) > MAX_READING_BUFFER:
                for reading in readings:
                    p = Process(target=save_reading, args=(reading,))
                    p.start()
                    p.join()
                #LogSaver(readings, db).start()
                readings = []
                
            
#TODO add cl option for logging
except KeyboardInterrupt:
    print("Quit; saving readings")
    #with open(LOG_NAME.format(str(datetime.now())), 'w') as outfile:
    #    json.dump(readings, outfile)
        #, indent=4)
finally:
    print(sys.stderr, 'closing socket')
    sock.close() 
