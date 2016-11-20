from AppKit import NSWorkspace
import threading 
import subprocess
import time
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListExcludeDesktopElements, kCGNullWindowID, kCGWindowNumber, \
                       kCGWindowName, kCGWindowOwnerName, kCGWindowListOptionAll, kCGWindowListOptionOnScreenOnly, \
                       kCGWindowListOptionOnScreenAboveWindow, kCGWindowListOptionOnScreenBelowWindow, \
                       kCGWindowListOptionIncludingWindow


class OSX_App_Helper(threading.Thread):
    

    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.options = kCGWindowListOptionOnScreenOnly + kCGWindowListExcludeDesktopElements
        self.window_list = CGWindowListCopyWindowInfo(self.options, kCGNullWindowID)
        self.interval = interval
        self.running = True
        self.active_app = None
        # time.sleep(5) #wait in case of a context switch on first launchecho $((`ioreg -c IOHIDSystem | sed -e '/HIDIdleTime/ !{ d' -e 't' -e '}' -e 's/.* = //g' -e 'q'` / 1000000000))
        for original in self.window_list:
            if self.check_app(original):
                #TODO handle for more than one app
                self.active_app = original

    def check_app(self, app):
        if "Window Server" not in app['kCGWindowOwnerName'] and app["kCGWindowBounds"]["Height"] > 0 and app["kCGWindowBounds"]["Width"] > 0 and app["kCGWindowLayer"] == 0 and app["kCGWindowStoreType"] == 1:
            return True
        else:
            return False

    def run(self):
        while self.running:
            new_windows = CGWindowListCopyWindowInfo(self.options, kCGNullWindowID)
            changes = list(set(new_windows) - set(self.window_list)) #detect changes between previous window set and new
            for change in changes:
                if self.check_app(change):
                    self.active_app = change
            idle = subprocess.check_output(["echo $((`ioreg -c IOHIDSystem | sed -e '/HIDIdleTime/ !{ d' -e 't' -e '}' -e 's/.* = //g' -e 'q'` / 1000000000))"], shell=True).decode()
            self.idle_time = int(idle)
            self.window_list = new_windows
            self.active_json = {"program": self.active_app["kCGWindowOwnerName"], "title": self.active_app["kCGWindowName"], "idleTime": self.idle_time}
            print(self.active_json)
            time.sleep(self.interval)

if __name__ == "__main__":
    osx = OSX_App_Helper(3)
    osx.start()
    try:
        while True:
            continue #yes, I know I am blocking the main thread here, but we are testing!
    except KeyboardInterrupt as e:
        osx.running = False
    
    