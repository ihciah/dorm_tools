import time, os
t = open("/root/openwrt_log", "w", 0)
while True:
    for wlan in ['wlan0', 'wlan1']:
        res = os.popen('iw dev %s station dump' % wlan).readlines()
        for i in range(0, len(res), 19):
            t.write(str(time.time()) + "\t" + res[i])
    time.sleep(5)
