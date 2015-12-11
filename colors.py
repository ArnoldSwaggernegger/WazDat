'''
This class contains some basic color codes using in main.py to print progress.
'''


import sys


class Colors:

    def __init__(self):
        self._notice = "\x1b[35m[INFO]\x1b[0m "
        self._alert = "\x1b[33m[WARN]\x1b[0m "
        self._succes = "\x1b[32m[GOOD]\x1b[0m "
        self._fatal = "\x1b[31m[FAIL]\x1b[0m "

    def write(self, str):
        sys.stdout.write(str)

    def notice(self, str):
        sys.stdout.write(self._notice + str + '\n')

    def alert(self, str):
        sys.stdout.write(self._alert + str + '\n')

    def succes(self, str):
        sys.stdout.write(self._succes + str + '\n')

    def fatal(self, str):
        sys.stdout.write(self._fatal + str + '\n')
