# Neuro Socket

Python, Couch and Node.

Python and Couch to connect to and collect from the mindwave. Also adds time and currently running app.

Couch then opens up an EventSource through a websocket and Node subscribes to that; updating the plot in real-time as and when readings come through.

# se.py

On OSX, the headset should autoconnect using the Neurosky driver
On Linux, you will need to find the MAC address
  `rfcomm rfcomm0 <MAC>`
You can set the serial port if it is in use.

## TODO

* Split dbs up or make the eventsource only get things from that day/latest revisions
* Save the since var so Node can begin from set points
    * Set it as a URL param?
* Maybe port to D3 so I am not relying on 2 libs for one thing but C3 is nice
* config file reading for se.py
