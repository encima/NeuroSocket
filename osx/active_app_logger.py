# Active application logger with python and pyobjc

# require `pyobjc`:
#  $ pip install pyobjc

from AppKit import NSWorkspace, NSObject, NSWorkspaceDidActivateApplicationNotification, NSWorkspaceApplicationKey
from PyObjCTools import AppHelper

def main():
    nc = NSWorkspace.sharedWorkspace().notificationCenter()
    print(nc)
    nc.addObserver_selector_name_object_(
        Observer.new(),
        "handle:",
        NSWorkspaceDidActivateApplicationNotification,
        None
    )
    AppHelper.runConsoleEventLoop(installInterrupt=True)

class Observer(NSObject):
    def handle_(self, noti):
        info = noti.userInfo().objectForKey_(NSWorkspaceApplicationKey)
        for n in ["bundleIdentifier", "localizedName", "bundleURL",
                  "executableURL", "launchDate"]:
            v = info.valueForKey_(n)
            print("%s (%s):\t%s" % (n, v.className(), v))
        print("--")

main()
