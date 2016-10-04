from AppKit import NSApplication, NSApp, NSWorkspace
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo

class OSXActiveApp():
    def getActive():
        app_name = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        win_name = None
        for app in NSWorkspace.sharedWorkspace().runningApplications():
            # app_name = app['NSApplicationName']
            if app.isActive():
                windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
                for window in windowList:
                    if window['kCGWindowOwnerName'] == app.localizedName():
                        win_name = window['kCGWindowName']
        return {'program': app_name, 'title': win_name}

def main():
    print(OSXActiveApp.getActive())

if __name__ == '__main__':
    main()
