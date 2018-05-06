from location import location
from weather import weather
from display import display
from baseimage import image

import time
import datetime
import sys
import logging
import socket
import ConfigParser
import daemon
import signal
import lockfile

config = None

def shutdown(signum, frame):
    sys.exit(0)

def getLocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def weatherString(w):
    current_temp_f = w.getObservation(weather.getCurrentTemperature, {"unit": "fahrenheit"})
    current_status = w.getObservation(weather.getCurrentStatus)

    deg = u"\u00b0"
    return u"%s%s %s" % (current_temp_f, deg, current_status)

def main():
    global config
    logging.info("starting!")

    l = location.Location(config.get("DEFAULT", "IPSTACK_API_KEY"))
    w = weather.Weather(config.get("DEFAULT", "WEATHER_API_KEY"), l.latitude, l.longitude)

    localIP = getLocalIp()

    disp = display.Display()
    last_tm = None

    while True:
        tm = datetime.datetime.now()
        if last_tm is None or tm.minute > last_tm.minute:
            last_tm = tm

            # For simplicity, the arguments are explicit numerical coordinates
            baseImage = image.BaseImage(disp.height, disp.width)

            # date / time
            time_string = tm.strftime("%I:%M %p")
            date_string = tm.strftime("%a %d %b %Y")
            baseImage.drawText(time_string)
            baseImage.drawText(date_string)
            baseImage.drawBorder(height=5, width=disp.height)
            logging.debug("drawing date/time")

            # weather temp / condition
            baseImage.drawText(weatherString(w))
            baseImage.drawBorder(height=5, width=disp.height)
            ogging.debug("drawing weather")

            # local ip addr
            baseImage.drawText(localIP)
            baseImage.drawBorder(height=5, width=disp.height)
            ogging.debug("drawing ip")

            disp.displayImage(baseImage.image)
            ogging.debug("drawing full image")

            time.sleep(1)

    logging.info("stopping!")
    w.close()
    logging.info("stopped!")


print "hello"
config = ConfigParser.ConfigParser()
if len(sys.argv) < 2:
    print "usage: python main.py <path to config file>"
    sys.exit(1)
config.read(sys.argv[1])

print sys.argv

with daemon.DaemonContext(
    signal_map={
        signal.SIGTERM: shutdown,
        signal.SIGTSTP: shutdown,
    },
    pidfile=lockfile.FileLock(config.get("DEFAULT", "PID_FILE")),
    stdout=sys.stdout,
    stderr=sys.stderr,
    working_directory="/home/pi/projects/kino/"
):
    logging.basicConfig(
        filename=config.get("DEFAULT", "LOG_FILE"),
        format='%(asctime)s: %(levelname)s: %(threadName)s: %(message)s',
        level=logging.DEBUG
    )
    main()
