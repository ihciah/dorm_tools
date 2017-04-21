import requests
from hashlib import sha1
from base64 import b64encode
import re
import time
import json

PT_USERNAME = "ihciah"
PT_USERINFO = "fdu_pt_hashed_user_pass"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/52.0.2743.116 Safari/537.36"
AUTH = "token:yourpassword"
CONFIG = {"split": "5", "max-connection-per-server": "5", "seed-ratio": "1.0", "seed-time": "0"}
RPC_URL = "http://127.0.0.1:6800/jsonrpc"


class PT_downloader():
    def __init__(self):
        self.s = self.get_pt_session()

    @staticmethod
    def get_pt_session():
        s = requests.session()
        res = s.get("https://pt.vm.fudan.edu.cn/index.php?action=login2").text
        time.sleep(2)
        p = re.compile(r"sSessionId:'(\w*)")
        r = p.search(res)
        sessionid = r.groups()[0]
        h = sha1()
        h.update(PT_USERINFO+sessionid)
        hexd = h.hexdigest()
        res = s.post("https://pt.vm.fudan.edu.cn/index.php?action=login2",
                     data={"user": PT_USERNAME, "passwrd": "", "cookielength": 1440, "hash_passwrd": hexd},
                     headers={"Origin": "http://pt.vm.fudan.edu.cn",
                              "Referer": "http://pt.vm.fudan.edu.cn/index.php?action=login2",
                              "User-Agent": USER_AGENT
                              }
                     )
        if "login" in res.url:
            return None
        else:
            return s

    @staticmethod
    def get_torrent_id(input_url):
        p = re.compile(r"(torrent|id)=(\d*)")
        r = p.search(input_url)
        if not r:
            return None
        ids = r.groups()
        if len(ids) < 2:
            return None
        return ids[1]

    def download_torrent(self, input_url):
        if not self.s:
            return False, "Login failed!"
        torrent_id = self.get_torrent_id(input_url)
        if not torrent_id:
            return False, "Error: Cannot parse torrent_id! torrent_id = %s" % torrent_id
        download_url = "https://pt.vm.fudan.edu.cn/index.php?action=dltorrent;id=%d" % int(torrent_id)
        torrent = self.s.get(download_url)
        if torrent.status_code != 200:
            return False, "Error: Cannot download torrent file! status_code = %d" % torrent.status_code
        torrent = b64encode(torrent.content)
        requests.post(RPC_URL, json.dumps({
            "jsonrpc": "2.0",
            "method": "aria2.addTorrent",
            "id": 1,
            "params": [AUTH, torrent, [], CONFIG]
        }))
        return True, "Uploaded!"
