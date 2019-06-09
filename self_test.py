#!/usr/bin/python

from util import execute
from const import PARSERS, REQUESTERS


for lang_library, binary in PARSERS.iteritems():
    lang, library = lang_library.split(".", 1)
    print(lang_library)
    print(execute(lang, binary, "http://11.11.11.11", "bin/parser/"))


for lang_library, binary in REQUESTERS.iteritems():
    lang, library = lang_library.split(".", 1)
    print(lang_library)
    print(execute(lang, binary, "http://11.11.11.11", "bin/requester/"))
