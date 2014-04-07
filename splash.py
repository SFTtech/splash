#!/usr/bin/env python3

# (c) 2014 Jonas Jelten
# released under the GNU GPLv3 or later, see "COPYING" for details.
#
# usage cat loltext | ./splash.py --speed 300

import argparse
import sys
import time

class Splash:
    def __init__(self, text):
        self.words = (word.strip() for word in (sum((line.split(" ") for line in text.split("\n")), [])))

    def word_focus(self, word):
        return ([0]*3 + [1]*4 + [2]*4 + [3]*4)[len(word)] if len(word) < 15 else 4

    def time_factor(self, word):
        default_word_length = 5.5   #this lenght gets factor 1.0
        per_char_adjust     = 0.08  #amount to adjust the factor per char deviation
        return max([((len(word) - default_word_length) * per_char_adjust) + 1, 0]) if len(word) > 0 else 0.1

    def display(self, sleeptime, dynamic_speed):
        self.displayed_word_count = 0
        for word in self.words:
            if len(word) > 0:
                c = self.word_focus(word)
                print("\x1b[2K%s%s\x1b[31m%s\x1b[0m%s\r" % (" " * (10 - c), word[:c], word[c], word[c+1:]), end="")
                self.displayed_word_count += 1
            time.sleep(sleeptime * (self.time_factor(word) if dynamic_speed else (1.0 if len(word) > 0 else 0)))

if __name__ == "__main__":
    if not sys.stdout.isatty():
        raise Exception("it makes no sense writing timed output to no tty.")

    parser = argparse.ArgumentParser(description='free (as in freedom) speed reading software.')
    parser.add_argument('--speed', "-s", type=int, default=300, help="reading speed in words per minute, default: 300")
    parser.add_argument('--dynamic-speed', "-d", action="store_true", default=False, help="wait dynamically depending on word length")
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    args = parser.parse_args()
    read_source = args.input_file.read()
    speedreader = Splash(read_source)
    start_time = time.time()

    try:
        speedreader.display(60/args.speed, args.dynamic_speed)
    except KeyboardInterrupt:
        pass
    finally:
        run_time = time.time() - start_time
        print("\ndisplayed %d words in %0.2f seconds: %.2f words per minute" % (speedreader.displayed_word_count,
                                                                                run_time,
                                                                                (speedreader.displayed_word_count*60)/run_time))
