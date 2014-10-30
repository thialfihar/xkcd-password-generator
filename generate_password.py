#!/usr/bin/env python3

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
    is_insecure_random = False
except ImportError:
    import random
    is_insecure_random = True

def generate(wordlist, num_words, num_passwords, min_word_length=4, max_word_length=100):
    wordlist = [x for x in wordlist if min_word_length <= len(x) <= max_word_length]
    for unused_i in range(num_passwords):
        password = []
        for unused_j in range(num_words):
            password.append(random.choice(wordlist))

        yield tuple(password)

if __name__ == "__main__":
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

    if is_insecure_random and not args.quiet:
        sys.stderr.write("warning: PyCrypto not installed, using the standard random module, which is not as secure")

    wordlist = [word.strip() for word in open(args.filename).read().split()]

    for words in generate(wordlist, args.num_words, args.num_passwords,
                          min_word_length=args.min_word_length,
                          max_word_length=args.max_word_length):
        raw_password = ''.join(words)
        readable_password = '.'.join(words)
        output = "{password}\t{readable}".format(password=raw_password, readable=readable_password)

        if args.verbose or args.list:
            size = int(math.ceil(len(raw_password) * math.log(26) / math.log(2)))
            strength = int(math.ceil(len(words) * math.log(len(wordlist)) / math.log(2)))

            if args.list:
                template = "\t{length}\t{size}\t{strength}"
            else:
                template = "\n\tlength: {length} chars, size:{size} bits, strength: {strength} bits\n"

            output += template.format(length=len(raw_password), size=size, strength=strength)

        sys.stdout.write(output + '\n')
        sys.stdout.flush()

