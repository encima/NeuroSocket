from AppKit import NSWorkspace
from Cocoa import NSApplicationActivateAllWindows, NSApplicationActivateIgnoringOtherApps

for app in NSWorkspace.sharedWorkspace().runningApplications():
    print(app)
