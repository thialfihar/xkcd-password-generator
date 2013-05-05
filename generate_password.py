#!/usr/bin/env python

# Copyright (C) 2012 Thialfihar (thi@thialfihar.org)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# http://www.gnu.org/licenses/

import argparse
import math
import sys

try:
    from Crypto.Random import random
    is_std_random = False
except ImportError:
    import random
    is_std_random = True

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", default='wordlist.txt',
                    help="FILE containing the wordlist", metavar="FILE")
parser.add_argument("-w", "--num-words", default=4, action="store", type=int,
                    help="number of words per password (default: 4)")
parser.add_argument("-n", "--num-passwords", default=1, action="store", type=int,
                    help="number of passwords to generate (default: 1)")
parser.add_argument("--min-word-length", default=4, action="store", type=int,
                    help="minimal length of words to be considered (default: 4)")
parser.add_argument("--max-word-length", default=100, action="store", type=int,
                    help="maximal length of words to be considered (default: 100)")
parser.add_argument("-v", "--verbose", default=False, action="store_true",
                    help="output some info")
parser.add_argument("-q", "--quiet", default=False, action="store_true",
                    help="hide warnings")
parser.add_argument("-l", "--list", default=False, action="store_true",
                    help="output verbose info as a tab-separated list, this implies -v")

args = parser.parse_args()

wordlist = [word.strip() for word in file(args.filename).read().split()]
wordlist = [x for x in wordlist if args.min_word_length <= len(x) <= args.max_word_length]

if is_std_random and not args.quiet:
    sys.stderr.write("warning: PyCrypto not installed, using the standard random module, which is not as secure")

if args.list:
    args.verbose = True

for unused_i in range(args.num_passwords):
    password = []
    for unused_j in range(args.num_words):
        password.append(random.choice(wordlist))
    raw_password = ''.join(password)
    readable_password = '.'.join(password)
    output = "%s\t%s" % (raw_password, readable_password)

    if args.verbose:
        if args.list:
            output += "\t%d\t%d\t%d" % \
                        (len(raw_password),
                         int(math.ceil(len(raw_password) * math.log(26) / math.log(2))),
                         int(math.ceil(len(password) * math.log(len(wordlist)) / math.log(2))))

        else:
            output += "\n    length: %d chars, size: %d bits, strength: %d bits\n" % \
                        (len(raw_password),
                         int(math.ceil(len(raw_password) * math.log(26) / math.log(2))),
                         int(math.ceil(len(password) * math.log(len(wordlist)) / math.log(2))))
    print output
