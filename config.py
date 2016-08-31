HOST = "127.0.0.1"
PORT = 13854
DB_PORT = 5984
CONFSTRING = '{"enableRawOutput": false, "format": "Json"}\n'
DB_USERNAME = "encima"
DB_PWD = "Cocaine5Unicorn_Hiatus"
DB_NAME = 'mindwave_logs'
DB_DELETE = True
FG_CMD = {
        'Darwin': "osascript osx/foreground_app.scpt",
        'Windows':"windows\\appfocus.exe",
        'Linux':"xprop -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5) _NET_WM_NAME WM_CLASS"
}

READING_BUFFER = 2
BUFFER = False
