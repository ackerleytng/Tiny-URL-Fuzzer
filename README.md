# Tiny URL Fuzzer

A tiny and cute URL fuzzer in my talk of [Black Hat USA 2017](https://www.blackhat.com/us-17/speakers/Orange-Tsai.html) and [DEFCON 25](https://www.defcon.org/html/defcon-25/dc-25-speakers.html).

Slides:

* [A New Era of SSRF - Exploiting URL Parser in Trending Programming Languages!](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf)

Case Study:

* [How I Chained 4 vulnerabilities on GitHub Enterprise, From SSRF Execution Chain to RCE!](http://blog.orange.tw/2017/07/how-i-chained-4-vulnerabilities-on.html)


# Setup

I suggest you run this in a VM, since running the fuzzer requires you to mess around with iptables, and you might not want to mess up your host's iptables.

Use the following in a fresh installation of Ubuntu Server 18.04

```
# The trending programming languages!
sudo apt install php ruby default-jdk python nodejs

# Allow fuzzing through requests
sudo apt install python-pip
sudo pip install requests

# Allow usage of LWP::Simple for fuzzing
sudo apt install libwww-perl

# Allow usage of Ruby's addressable for fuzzing
sudo gem install addressable

# Allow usage of php's curl for fuzzing
sudo apt install php-curl
```

# Quick sanity check

Check that all the libraries under test are working

First start the servers with

```
sudo ./setup_iptables_servers.py
```

Then run the self-test

```
$ ./self_test.py
Java.net.URL
scheme=http, host=11.11.11.11, port=-1
Ruby.uri
scheme=http, host=11.11.11.11, port=80
Go.net/url
scheme=http, host=11.11.11.11, port=
PHP.parseurl
scheme=http, host=11.11.11.11, port=
NodeJS.url
scheme=http, host=11.11.11.11, port=
Python.urlparse
scheme=http, host=11.11.11.11, port=
Ruby.addressable/uri
scheme=http, host=11.11.11.11, port=
Perl.URI
scheme=http, host=11.11.11.11, port=80
Perl.LWP
127.0.0.1:1180/
NodeJS.http
127.0.0.1:1180/
Python.requests
127.0.0.1:1180/
Ruby.Net/HTTP
127.0.0.1:1180/
Python.urllib2
127.0.0.1:1180/
Python.httplib
127.0.0.1:1180/
Go.net/http
127.0.0.1:1180/
Ruby.open_uri
127.0.0.1:1180/
PHP.curl
127.0.0.1:1180/
Python.urllib
127.0.0.1:1180/
PHP.open
127.0.0.1:1180/
Java.URL
127.0.0.1:1180/
```

# Start fuzzing

```bash
$ fuzz.py
```
