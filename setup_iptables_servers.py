#!/usr/bin/python

import os
import sys
from subprocess import check_output, Popen

def install_iptables():
    # Redirect all packets destined for 11.11.11.11:80 to localhost:1180
    check_output("iptables -t nat -A OUTPUT -p tcp --dst 11.11.11.11 --dport 80 "
                 "-j DNAT --to-destination 127.0.0.1:1180", shell=True)
    # Redirect all packets destined for 22.22.22.22:80 to localhost:2280
    check_output("iptables -t nat -A OUTPUT -p tcp --dst 22.22.22.22 --dport 80 "
                 "-j DNAT --to-destination 127.0.0.1:2280", shell=True)

def restore_iptables():
    check_output('iptables -t nat -F', shell=True)

def install_server():
    """Starts servers to respond to fuzzing requests"""
    Popen('nodejs bin/tuf_web.js 1180 &', shell=True)
    Popen('nodejs bin/tuf_web.js 2280 &', shell=True)

def restore_server():
    """Kills servers meant to respond to fuzzing requests"""
    for pid in check_output('pgrep -f "tuf_web.js"', shell=True).splitlines():
        Popen('kill -9 %s 2>/dev/null;true'%pid, shell=True)

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'install':
        install_iptables()
        install_server()
    elif m == 'restore':
        restore_iptables()
        restore_server()
