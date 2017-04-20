import time
from hashlib import sha1
from subprocess import Popen
import memcache
import logging

KEY = "your_long_key"
WIFI_KEY = "your_long_key"
MAC = ["00:00:00:00:00:00"]  # Mac to open door
BEGIN_TIME = 10
END_TIME = 22
TIME_INTERVAL = 240  # 4min
MAX_DBM = {"00:00:00:00:00:00": -70}
MAX_WINDOW = 5  # TODO: use last `MAX_WINDOW` histories to make result more accurate
LOG_PATH = "/usr/local/share/opendoor/log"


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class MC(object):
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=False)

    def get(self, name):
        return self.mc.get(name)

    def set(self, name, value, timeout=None):
        if timeout:
            return self.mc.set(name, value, timeout)
        return self.mc.set(name, value)

    def delete(self, name):
        return self.mc.delete(name)


def valid_sign(t, sign):
    t = str(t)[:15]
    sign = str(sign)[:40]
    if not t.isdigit() or not sign.isalnum():
        return False
    if abs(int(time.time()) - int(t)) > 60:
        return False
    if sha1(str(t) * 5 + KEY).hexdigest() == str(sign):
        return True
    return False


def window_update(l, v):
    if not l:
        return [v]
    if len(l) < MAX_WINDOW:
        return l + [v]
    return l[1:] + [v]


def wx_open(t, sign):
    if valid_sign(t, sign):
        Popen(["/bin/open.py"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        return True
    return False


def valid_time():
    hour_now = time.localtime(time.time()).tm_hour
    return BEGIN_TIME < hour_now < END_TIME


def valid_mac(mac):
    #  Valid mac address and it's last online time interval
    if mac not in MAC:
        return False
    mc = MC()
    last_time_list = mc.get(mac)
    if last_time_list is None:
        logging.warning("Memcache not hit!")
        return True
    if int(time.time()) - last_time_list[-1] > TIME_INTERVAL:
        return True
    return False


def valid_dbm(dbm, mac):
    #  Valid mac's dbm to make sure it's at outside
    return mac in MAX_DBM and dbm < MAX_DBM[mac]


def log_time(mac):
    #  Log valid mac's online status after auth no matter it's pass or not.
    if mac not in MAC:
        return
    mc = MC()
    mc.set(mac, window_update(mc.get(mac), int(time.time())))


def wifi_open(dbm, mac):
    ret = False
    if valid_time() and valid_mac(mac) and valid_dbm(dbm, mac):
        Popen(["/bin/open.py"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        ret = True
    log_time(mac)
    return ret


def wifi_client_auth(auth):
    return auth == WIFI_KEY
