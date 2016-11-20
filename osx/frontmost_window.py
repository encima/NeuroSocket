# Copyright @ Bjarte Johansen 2012
# License: http://ljos.mit-license.org/

from AppKit import NSApplication, NSApp, NSWorkspace
from Foundation import NSObject, NSLog
from PyObjCTools import AppHelper
from Quartz import kCGWindowListOptionOnScreenOnly, kCGWindowListExcludeDesktopElements, kCGNullWindowID, CGWindowListCopyWindowInfo
import time 

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        workspace = NSWorkspace.sharedWorkspace()
        activeApps = workspace.runningApplications()
        for app in activeApps:
            if app.isActive():
                options = kCGWindowListOptionOnScreenOnly + kCGWindowListExcludeDesktopElements
                windowList = CGWindowListCopyWindowInfo(options,
                                                        kCGNullWindowID)
                for window in windowList:
                    print(window)
                    if window['kCGWindowOwnerName'] == app.localizedName():
                        NSLog('%@', window)
                        break
                break
        AppHelper.stopEventLoop()

def main():
    NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()

    
if __name__ == '__main__':
    # main()
    options = kCGWindowListOptionOnScreenOnly + kCGWindowListExcludeDesktopElements
    window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    while True:
        time.sleep(5)
        new_windows = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        changes = list(set(new_windows) - set(window_list))
        for change in changes:
            if "Window Server" not in change['kCGWindowOwnerName']:
                print(change)
        window_list = new_windows
        print("----")