#!/usr/bin/python

import sys
from util import execute
from const import PARSERS, REQUESTERS


test_target = "http://11.11.11.11"
if len(sys.argv) > 1:
    test_target = sys.argv[1]


for lang_library, binary in PARSERS.iteritems():
    lang, library = lang_library.split(".", 1)
    print(lang_library)
    print(execute(lang, binary, test_target, "bin/parser/"))


for lang_library, binary in REQUESTERS.iteritems():
    lang, library = lang_library.split(".", 1)
    print(lang_library)
    print(execute(lang, binary, test_target, "bin/requester/"))
