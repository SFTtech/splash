#!/usr/bin/env python3

# Copyright (c) 2014-2015 Jonas Jelten
# released under the GNU GPLv3 or later, see "COPYING" for details.
#
# usage cat loltext | ./splash.py --speed 300

"""
main speedreading algorithm routines

word center calculations and file parsing happen in here.
"""

import argparse
import sys
import time


def word_focus(word):
    """
    which character to put in the center, depending on word length.
    """
    if len(word) < 15:
        return ([0]*3 + [1]*4 + [2]*4 + [3]*4)[len(word)]
    else:
        return 4

def time_factor(word):
    """
    word progress time adjustment by word length.
    """
    default_word_length = 5.5   # this lenght gets factor 1.0
    per_char_adjust = 0.08      # factor adjust amount per char deviation
    if len(word) > 0:
        return max([((len(word) - default_word_length) * per_char_adjust) + 1, 0])
    else:
        return 0.1              # an empty word (e.g. blank line)


class Splash:
    """
    manages the reading state of one file.
    provides functions to advance words or display them on the terminal.
    """

    def __init__(self, input_file):
        self.file = input_file
        self.worditer = None
        self.displayed_word_count = 0

    def get_words(self):
        """
        generator for all the words in the file
        """
        for line in self.file:
            for word in line.split(" "):
                yield word.strip()

    def display(self, sleeptime, static_speed):
        """
        show the current word on the console
        """
        self.displayed_word_count = 0
        for word in self.get_words():
            if len(word) > 0:
                center = word_focus(word)
                print("\x1b[2K%s%s\x1b[31m%s\x1b[0m%s\r" % (
                    " " * (10 - center), word[:center],
                    word[center], word[center+1:]), end="")
                self.displayed_word_count += 1
            if static_speed:
                factor = 1.0 if len(word) > 0 else 0
            else:
                factor = time_factor(word)
            time.sleep(sleeptime * factor)

    def advance(self, wpm):
        """
        advance one word in the internal iterator.
        this is the API function you want to use.
        """
        self.displayed_word_count = 0

        if not self.worditer:
            self.worditer = self.get_words()

        try:
            word = next(self.worditer)
            center = word_focus(word)
            delay = wpm * time_factor(word)
            self.displayed_word_count += 1
            end = False

        except StopIteration:
            self.worditer = None
            word = "..."
            center = 1
            delay = 0
            end = True

        return end, word, center, delay


def main():
    """
    main entry point for the terminal operation mode
    """

    if not sys.stdout.isatty():
        raise Exception("it makes no sense writing timed output to no tty.")

    parser = argparse.ArgumentParser(
        description="free (as in freedom) speedreading software.")
    parser.add_argument('--speed', "-s", type=int, default=300,
                        help="reading speed in words per minute, default: 300")
    parser.add_argument('--static-speed', "-d", action="store_true",
                        default=False,
                        help="don't wait dynamically depending on word length")
    parser.add_argument('input_file', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help="name of the plain text file to display")

    args = parser.parse_args()
    speedreader = Splash(args.input_file)
    start_time = time.time()

    try:
        speedreader.display(60/args.speed, args.static_speed)
    except KeyboardInterrupt:
        pass
    finally:
        run_time = time.time() - start_time
        print(("\ndisplayed %d words in %0.2f seconds: "
               "%.2f words per minute") % (
                   speedreader.displayed_word_count,
                   run_time,
                   (speedreader.displayed_word_count*60)/run_time))


if __name__ == "__main__":
    main()
