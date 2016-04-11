#sockforward

_sockforward.py_ tunnels specified port to another host/port. 

[+] Supports TCP _(HTTP/HTTPS/FTP/SSH/etc.)_ protocols and uses pure python socket implementation.

[+] Supports threads in case multiple connections will be made.

Specially written for GSoC 2016


Installation
-----------
```git clone https://github.com/mussakhojayeva/sockforward.git && cd sockforward```


Running
-------
```
Usage: sockforward.py listen_port remote_host remote_port

examples:
    sockforward.py 80 google.com 80
    Route incoming HTTP connections to google.com:80.

    sockforward.py 22 127.0.0.1 2228
    Route incoming SSH connections to port 2228 on localhost.
```


Notes
-----
_Author: Saida Mussakhojayeva_

_Feedback: saida.mussakhojayeva@nu.edu.kz_

_runs and tested on python 2.7_

