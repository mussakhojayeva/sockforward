#!/usr/bin/env python

"""
Project: <Socket Forwarder>
Author: <Saida Mussakhojayeva>
Feedback: <saida.mussakhojayeva@nu.edu.kz>

Notes:
specially for GSoC 2016
runs and tested on python 2.7

Info:
sockforward.py tunnels specified port to another host/port (socket forwarding)
it supports HTTP(S)/FTP/SSH/Plain Text/etc. protocols.
uses pure python socket implementation.
supports threads in case multiple connections will be made.

Usage: sockforward.py listen_port remote_host remote_port

examples:
    sockforward.py 80 google.com 80
    Route incoming HTTP connections to google.com:80.

    sockforward.py 22 127.0.0.1 2228
    Route incoming SSH connections to port 2228 on localhost.
"""

import os
import sys
from socket import *
from threading import Thread

# Data buffer size
BUFFER = 1024


class Route(Thread):

    """ Binds socket and routes traffic """

    def __init__(self, listen_port, remote_host, remote_port):
        Thread.__init__(self)
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.sock = socket(AF_INET, SOCK_STREAM)
        # Bind socket on local interface
        self.sock.bind(('', listen_port))
        # Max queued connections
        self.sock.listen(10)

    def run(self):
        while True:
            try:
                # Local socket
                local, addr = self.sock.accept()
                # Socket forwarding
                fwd = socket(AF_INET, SOCK_STREAM)
                fwd.connect((self.remote_host, self.remote_port))
                # The great router itself :D
                SockSwitch(local, fwd).start()
                SockSwitch(fwd, local).start()
            except KeyboardInterrupt:
                break


class SockSwitch(Thread):

    """ Switch data from source socket to destination socket and vice versa"""

    queue = []

    def __init__(self, src, dest):
        Thread.__init__(self)
        self.dest = dest
        self.src = src
        # Socket queue IN
        SockSwitch.queue.append(self)

    def run(self):
        while True:
            # Deal with incoming data
            try:
                data = self.src.recv(BUFFER)
                if not data:
                    break
                self.dest.send(data)
            except:
                break
        # Socket queue OUT
        SockSwitch.queue.remove(self)


class Help():

    """ Dummy help text """

    def __init__(self):
        print ""
        print "Usage: %s listen_port remote_host remote_port" \
            % os.path.basename(__file__)
        print ""
        print "     sockforward tunnels specified port to another host/port (socket forwarding)"
        print ""
        print "Options:"
        print "     listen_port - listen port for incoming connections"
        print "     remote_host - destination host"
        print "     remote_port - remote port on destination host"
        print ""
        print "Hint:"
        print "     if %s doesn`t stop on Ctrl+C then use Ctrl+Break / Break" \
            % os.path.basename(__file__)


def main():
    if len(sys.argv) > 1:
        local_port = int(sys.argv[1])
        remote_host = sys.argv[2]
        remote_port = int(sys.argv[3])
        Route(local_port, remote_host, remote_port).run()
    else:
        Help()

if __name__ == '__main__':
    main()
