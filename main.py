import epd2in7.epd2in7 as epd2
import Image
import ImageFont
import ImageDraw
import socket

import ConfigParser
from location import location
from weather import weather

import time
import datetime
import sys
import logging

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
    try:

        epd = epd2.EPD()
        epd.init()

        last_tm = None

        while True:
            tm = datetime.datetime.now()
            if last_tm is None or tm.minute > last_tm.minute:
                last_tm = tm

                # For simplicity, the arguments are explicit numerical coordinates
                image = Image.new('1', (epd2.EPD_WIDTH, epd2.EPD_HEIGHT), 255)    # 255: clear the image with white
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)

                # local ip
                localIP = getLocalIp()
                draw.text((5, 5), localIP, font = font, fill = 0)

                # border
                draw.rectangle((0, 25, epd2.EPD_HEIGHT, 30), fill = 0)

                # location
                draw.text((5, 35), str(l), font = font, fill = 0)

                # border
                draw.rectangle((0, 55, epd2.EPD_HEIGHT, 60), fill = 0)

                draw.text((5, 65), weatherString(w), font=font, fill=0)

                # border
                draw.rectangle((0, 85, epd2.EPD_HEIGHT, 90), fill = 0)

                # time

                time_string = tm.strftime("%I:%M %p")
                date_string = tm.strftime("%a %b %m %Y")
                draw.text((5, 95), time_string, font=font, fill=0)
                draw.text((5, 115), date_string, font=font, fill=0)

                # border
                draw.rectangle((0, 135, epd2.EPD_HEIGHT, 140), fill = 0)

                #draw.text((5, 145), w.getLastUpdate().strftime("%I:%M %p"), font=font, fill=0)

                epd.display_frame(epd.get_frame_buffer(image))

            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("caught KeyboardInterrupt")
    except Exception, e:
        logging.warn("caught exception:", e)

    logging.info("stopping!")
    w.close()
    logging.info("stopped!")


    # display images
    #epd.display_frame(epd.get_frame_buffer(Image.open('monocolor.bmp')))

if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(threadName)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    main()
