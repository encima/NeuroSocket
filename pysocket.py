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
import re
import config
import argparse
from AppKit import NSWorkspace
import osx.OSXActiveApp as osaa

pp = pprint.PrettyPrinter(indent=4)
parser = argparse.ArgumentParser(description='Log all the productivity')
parser.add_argument('-o','--output',help='Output file name', required=False)
parser.add_argument('-d','--dbname',help='DB name', required=False, default=None)
#parser.add_argument('-d','--dbname',help='DB name', required=False, default=config.DB_NAME)
parser.add_argument('-l', '--logdir', help='Directory to save logs', required=False)
parser.add_argument('-i','--interval',help='Interval for readings', required=False, default=30, type=int)
parser.add_argument("-m", "--mindwave", help="Connect to mindwave", action="store_true")
args = parser.parse_args()
server = couchdb.Server()
server.resource.credentials = (config.DB_USERNAME, config.DB_PWD)
db = None
log_file = None
if not args.logdir:
    try:
        db = server[args.dbname]
    except:
        db = server.create(args.dbname)
    print("DB Connected")
else:
    print(datetime.today().toordinal())
    logpath = "{0}/log_{1}.json".format(args.logdir, datetime.today().toordinal())
    log_file = open(logpath, 'w+', encoding="utf8")
    print("Opened {} for writing".format(logpath))

print(args.dbname)
if args.dbname is not None:
    try:
        db = server[args.dbname]
    except:
        db = server.create(args.dbname)
    print("DB Connected")
LOG_NAME = "output/log_{0}.json"
HOST_INFO = platform.uname()
print("Running on {}".format(HOST_INFO.system))

def save_reading(reading):
    if args.logdir:
        json.dump(reading, log_file)
    elif db is not None:
        db.save(reading)

def get_app(host):
    foreground_app = None
    if host == 'Darwin':
        foreground_app = osaa.OSXActiveApp.getActive()
        print(foreground_app)
        foreground_app = foreground_app
    else:
        try:
            foreground_app = subprocess.check_output(config.FG_CMD[host], stderr=subprocess.STDOUT, shell=True)
            foreground_app = foreground_app.decode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        if host == 'Linux':
            foreground_app = foreground_app.replace("\"","")
            foreground_app = re.split("= |\n", foreground_app)
            idleTime = subprocess.check_output("xprintidle", stderr=subprocess.STDOUT,shell=True).decode()
            idleTime = float(idleTime)/1000
            foreground_app = {'program': foreground_app[3], 'title': foreground_app[1], 'idleTime':idleTime}
        elif host == 'Windows':
            foreground_app = json.loads(foreground_app)
    return foreground_app

def enrich_reading(d_json):
    print(d_json)
    d_json['time'] = str(datetime.now())
    d_json['host'] = HOST_INFO.node
    print(HOST_INFO.node)
    d_json['app'] = get_app(HOST_INFO.system)
    d_json['platform'] = HOST_INFO.system
    print(d_json)

sock = None
if args.mindwave:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readings = []
    server_address = (config.HOST, config.PORT)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
try:
    # Send config message to mindwave
    if sock:
        message = "{\"enableRawOutput\": false, \"format\": \"Json\"}\n";
    # print('sending "%s"' % message)
        sock.send(config.CONFSTRING.encode('utf8'))

    # Look for the response
    while True:
        if args.mindwave:
            data = sock.recv(1024)
            dataform = data.decode()
            print(dataform)
            try:
                struct = json.loads(dataform)

                if struct:
                    if ('status' in struct and struct['status'] != "scanning") or 'status' not in struct:
                        d_json = struct
                        #add time and foreground app to json
                        enrich_reading(d_json)
#               pp.pprint(d_json)
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
            except Exception as e:
                print("------")
                print(str(e))
                print(dataform)
                print("------")
        else:
            d_json = {}
            enrich_reading(d_json)
            pp.pprint(d_json)
            save_reading(d_json)
            time.sleep(args.interval)


#TODO add cl option for logging
except KeyboardInterrupt:
    print("Quit; saving readings")
finally:
    if log_file is not None:
        log_file.close()
        print("Closing Log")
    if sock:
        sock.close()
        print(sys.stderr, 'closing socket')
