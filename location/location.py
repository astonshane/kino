import requests
import json
import netifaces as ni

class Location:
    def __init__(self, key):
        self.apikey = key
        self.refresh()

    def getIp(self):
        for interface in ["eth0", "en1", "en0"]:
            try:
                print ni.ifaddresses(interface)
                print ni.ifaddresses(interface)[ni.AF_INET]
                self.ipAddr = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
                break
            except ValueError:
                pass

    def __str__(self):
        return "%s, %s" % (self.city, self.region_code)

    def __repr__(self):
        return self.__str__()


    def refresh(self):

        url = "http://api.ipstack.com/check?access_key=%s&format=1" % (self.apikey)
        r = requests.get(url)
        j = json.loads(r.text)

        self.ipAddr = j["ip"]
        self.city = j["city"] # kearny
        self.zip = j["zip"] # 07032
        self.region_name = j["region_name"] # New Jersey
        self.region_code = j["region_code"] # NJ
        self.latitude = float(j["latitude"])
        self.longitude = float(j["longitude"])
