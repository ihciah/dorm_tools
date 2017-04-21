from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from utils import wx_open
from utils import wifi_open
from utils import wifi_client_auth
from utils import LOG_PATH
import json
import logging

app = Flask(__name__)

handler = logging.FileHandler(LOG_PATH)  # errors logged to this file
handler.setLevel(logging.WARNING)  # only log errors and above
app.logger.addHandler(handler)  # attach the handler to the app's logger
logging.warning("Init!")


@app.route('/')
def home_page():
    return redirect(url_for('download_torrent'))


@app.route('/opendoor', methods=['GET'])
def open_door():
    time = request.args.get('time', '')
    sign = request.args.get('sign', '')
    if wx_open(time, sign):
        return 'OK'
    else:
        return "ERROR"


@app.route('/wifi', methods=['POST'])
def wifi_open_door():
    users = request.form.get('users')
    auth = request.form.get('auth')
    if not wifi_client_auth(auth):
        return ""
    if users:
        users = json.loads(users)
        logging.warning(str(users))
        for u in users:
            if u'MAC' not in u or u'DBM' not in u:
                continue
            mac = str(u[u'MAC']).upper()
            dbm = u[u'DBM']
            try:
                dbm = int(dbm)
            except:
                continue
            wifi_open(dbm, mac)
    return ""


@app.route('/download', methods=['GET', 'POST'])
def download_torrent():
    from flask import render_template
    if request.method == 'GET':
        return render_template('download.html')
    else:
        torrent = request.form['torrent']
        if not torrent:
            return render_template('download.html', info="Torrent is not valid!")
        from pt_downloader import PT_downloader
        downloader = PT_downloader()
        status, info = downloader.download_torrent(torrent)
        return render_template('download.html', info=info)


@app.route('/ui', methods=['GET'])
def ui_redirect():
    return redirect(url_for('static', filename='ui/index.html'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
