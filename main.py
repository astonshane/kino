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
    logging.info("starting!")

    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    l = location.Location(config.get("DEFAULT", "IPSTACK_API_KEY"))
    w = weather.Weather(config.get("DEFAULT", "WEATHER_API_KEY"), l.latitude, l.longitude)

    localIP = getLocalIp()
    try:

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

                # weather temp / condition
                baseImage.drawText(weatherString(w))
                baseImage.drawBorder(height=5, width=disp.height)

                # local ip addr
                baseImage.drawText(localIP)
                baseImage.drawBorder(height=5, width=disp.height)

                disp.displayImage(baseImage.image)

            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("caught KeyboardInterrupt")
    except Exception, e:
        logging.warn("caught exception: %s" % str(e))

    logging.info("stopping!")
    w.close()
    logging.info("stopped!")


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(threadName)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    main()
