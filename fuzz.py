#!/usr/bin/python

import sys
from pprint import pprint
from itertools import product
from multiprocessing.dummy import Pool as ThreadPool

import util.fuzz as fuzz
from util import execute
from const import PARSERS, REQUESTERS

DEBUG = 'debug' in sys.argv

FIRST_IP = "11.11.11.11"
SECOND_IP = "22.22.22.22"

INS_COUNT = [0, 3, 0]
CHARSETS = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0cA01\x00'
FORMAT = "http://{}{}{}{}{}".format(
    "%c" * INS_COUNT[0],
    FIRST_IP,
    "%c" * INS_COUNT[1],
    SECOND_IP,
    "%c" * INS_COUNT[2],
)

def _print(msg):
    sys.stdout.write("%s\n" % msg)


def run_parser(url):
    res = {}

    for key, binary in PARSERS.iteritems():
        lang, libname = key.split('.', 1)
        r = execute(lang, binary, url, base='bin/parser/')

        # parse host, change here to get the result you want
        if 'host=' in r and 'port=' in r:
            res[key] = r.split('host=')[-1].split(', ')[0]
        else:
            res[key] = 'err'

    return res


def run_requester(url):
    res = {}

    for key, binary in REQUESTERS.iteritems():
        lang, libname = key.split('.', 1)

        r = execute(lang, binary, url, base='bin/requester/')
        res[key] = r

    return res


def run(random_data):
    url = FORMAT % random_data
    url = url + '/' + (''.join(random_data).encode('hex'))
    url = url.replace('\x00', '%00')

    urls = run_parser(url)
    gets = run_requester(url)

    # Bucket the parsers according to which hosts they parsed out
    #   e.g.
    #   11.11.11.11: ["Java", ...]
    #   22.22.22.22: ["Python", ...]
    total_urls = {}
    for k, v in urls.iteritems():
        if total_urls.get(v):
            total_urls[v].append(k)
        else:
            total_urls[v] = [k]

    if len(total_urls) > 1:
        msg = 'parsed url = %s\n' % url
        for k, v in sorted(total_urls.iteritems(), key=lambda x: len(x[1]), reverse=True):
            msg += '%-16s %d = %s\n'%(k, len(v), repr(v))

        _print(msg)

    total_gets = {}
    for k, v in gets.iteritems():
        # The webserver is written to reply with the port that it is listening to
        #   so if you run `./setup_iptables_servers.py install` without modification
        #   and do curl 11.11.11.11, you should get
        #   `127.0.0.1:1180/` in return

        # This line removes / and everything after it
        # If v is "err", it will still remain as "err"
        v = v.split('/')[0]

        # Bucket the requesters according to which webserver
        #   they ended up requesting
        #   e.g.
        #   "127.0.0.1:1180": ["Java", ...]
        #   "127.0.0.1:2280": ["Python", ...]
        if total_gets.get(v):
            total_gets[v].append(k)
        else:
            total_gets[v] = [k]

    if len(total_gets) > 1:
        msg = 'got url = %s\n'%url
        for k, v in sorted(total_gets.iteritems(), key=lambda x: len(x[1]), reverse=True):
            msg += '%-24s %d = %s\n'%(k, len(v), repr(v))
        _print(msg)


data_set = product(list(CHARSETS), repeat=sum(INS_COUNT))

if 'debug' in sys.argv:
    for i in data_set:
        run(i)
else:
    pool = ThreadPool(32)
    result = pool.map_async(run, data_set).get(0xfffff)
