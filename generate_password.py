#!/usr/bin/env python3

# Copyright (C) 2012-2014 Thialfihar (thi@thialfihar.org)
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
"""
The passwords generated here are much easier to remember than cryptic random passwords still being
as secure or even more secure than said cryptic passwords.

For instance, a password of four random words from a world list of ca. 3500 words is as secure as
a password of eight random chars from the charset a-zA-Z0-9, even though the former password is
entirely lowercase and only contains four easy to remember words.

"""
import argparse
import math
import sys

try:
    from Crypto.Random import random
    is_insecure_random = False
except ImportError:
    import random
    is_insecure_random = True

def generate(wordlist, num_words, num_passwords,
             min_word_length=4, max_word_length=100,
             min_length=4, max_length=100):
    wordlist = [x for x in wordlist if min_word_length <= len(x) <= max_word_length]
    generated_passwords = 0
    bad_passwords = 0
    while generated_passwords < num_passwords:
        words = [random.choice(wordlist) for unused_j in range(num_words)]
        password = ''.join(words)
        if not (min_length <= len(password) <= max_length):
            bad_passwords += 1
            if bad_passwords >= 1000:
                raise Exception("generated too many passwords not fitting the length requirements, bailing out")
            continue

        yield password, tuple(words)
        generated_passwords += 1

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
    parser.add_argument("--min-length", default=12, action="store", type=int,
                        help="minimal length of the entire password to be considered (default: 12)")
    parser.add_argument("--max-length", default=100, action="store", type=int,
                        help="maximal length of the entire password to be considered (default: 100)")
    parser.add_argument("-v", "--verbose", default=False, action="store_true",
                        help="output some info for each password")
    parser.add_argument("-q", "--quiet", default=False, action="store_true",
                        help="hide warnings")
    parser.add_argument("-l", "--list", default=False, action="store_true",
                        help="output verbose info as a tab-separated list")

    args = parser.parse_args()

    if args.min_length < 12 and not args.quiet:
        sys.stderr.write("warning: lowercase passwords shorter than 12 characters are insecure\n")
        sys.stderr.flush()

    if args.max_length < 20 and not args.quiet:
        sys.stderr.write("warning: restricting the password length too much might lower the password "
                         "strength because less passwords are available for a given configuration\n")
        sys.stderr.flush()

    if is_insecure_random and not args.quiet:
        sys.stderr.write("warning: PyCrypto not installed, using the standard random module, which "
                         "is not as secure\n")
        sys.stderr.flush()

    wordlist = [word.strip() for word in open(args.filename).read().split()]

    for password, words in generate(wordlist, args.num_words, args.num_passwords,
                                    min_word_length=args.min_word_length,
                                    max_word_length=args.max_word_length,
                                    min_length=args.min_length,
                                    max_length=args.max_length):
        readable_password = '.'.join(words)
        output = "{password}\t{readable}".format(password=password, readable=readable_password)

        if args.verbose or args.list:
            size = int(math.ceil(len(password) * math.log(26) / math.log(2)))
            strength = int(math.ceil(len(words) * math.log(len(wordlist)) / math.log(2)))

            if args.list:
                template = "\t{length}\t{size}\t{strength}"
            else:
                template = "\n\tlength: {length} chars, size:{size} bits, strength: {strength} bits\n"

            output += template.format(length=len(password), size=size, strength=strength)

        sys.stdout.write(output + '\n')
        sys.stdout.flush()

