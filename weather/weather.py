import pyowm
import time
import datetime
import logging
from threading import Thread, Event, Lock

def getCurrentTemperature(observation, unit):
    w = observation.get_weather()
    return int(w.get_temperature(unit)["temp"])

def getCurrentStatus(observation):
    w = observation.get_weather()
    return w.get_status()


class Weather:
    def __init__(self, key, lat, lon):
        self.apikey = key
        self.owm = pyowm.OWM(self.apikey)

        self.lat = lat
        self.lon = lon

        # the last observation made
        self.observation = None
        self.lock = Lock()

        self.stop = Event()
        self.lastUpdate = None

        self.thread = Thread(target=self.updater)
        self.thread.setName("WeatherUpdater")
        self.thread.start()

    def updater(self):
        logging.info("starting!")
        nextUpdate = datetime.datetime.now() + datetime.timedelta(minutes=30)

        while not self.stop.isSet():
            now = datetime.datetime.now()
            if (self.observation is None) or (now >= nextUpdate):
                logging.info("updating weather!")
                self.lastUpdate = now
                nextUpdate = now + datetime.timedelta(minutes=30)
                new_observation = self.owm.weather_at_coords(self.lat, self.lon)

                with self.lock:
                    self.observation = new_observation

            time.sleep(1)
        logging.info("stopping!")

    def getLastUpdate(self):
        while True:
            with self.lock:
                if self.lastUpdate is not None:
                    return self.lastUpdate
            time.sleep(0.1)

    # acquire the lock and then call the function passed in
    # kwargs is a map of arguments to be passed to weatherFunc
    # observation will be added to it
    def getObservation(self, weatherFunc, kwargs={}):
        while True:
            with self.lock:
                if self.observation is not None:
                    kwargs["observation"] = self.observation
                    return weatherFunc(**kwargs)
            time.sleep(0.1)

    def close(self):
        self.stop.set()
        self.thread.join()
