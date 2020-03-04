from time import sleep
from daemonize import Daemonize

pid = "/tmp/test.pid"


def main():
    while True:
        sleep(5)

daemon = Daemonize(app="mytank_app", pid=pid, action=main)
daemon.start()