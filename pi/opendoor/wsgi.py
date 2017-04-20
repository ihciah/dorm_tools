import sys,os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/usr/local/share/opendoor/")
os.chdir("/usr/local/share/opendoor/")

from opendoor import app as application

if __name__ == "__main__":
    application.run()
