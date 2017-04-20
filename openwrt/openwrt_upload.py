#!/usr/bin/python
import time, os, urllib2, urllib, json

LAST_MAC = set()
CIRCLE_LEFT = 0

SLEEP_TIME = 0.5
UPLOAD_CIRCLE = 30
URL = "http://192.168.1.111:11111/wifi"
AUTH = "YOUR_LONG_KEY"


def upload():
    global LAST_MAC, CIRCLE_LEFT
    users = []
    mac_set = set()
    for wlan in ['wlan0', 'wlan1']:
        res = os.popen('iw dev %s station dump' % wlan).readlines()
        for i in range(0, len(res), 19):
            if res[i + 13].strip().endswith("s") and res[i + 14].strip().endswith("s"):
                signal_line = res[i + 8][11:]
                mac = res[i].split(' ')[1]
                users.append({"MAC": mac, "DBM": int(signal_line[:signal_line.find(' ')])})
                mac_set.add(mac)
    if mac_set != LAST_MAC or CIRCLE_LEFT <= 0:
        urllib2.urlopen(URL, data=urllib.urlencode({"users": json.dumps(users),
                                                    "auth": AUTH}))
        LAST_MAC = mac_set
        CIRCLE_LEFT = UPLOAD_CIRCLE
    CIRCLE_LEFT -= 1
    time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    while True:
        try:
            upload()
        except KeyboardInterrupt:
            exit()
        except:
            time.sleep(1)
