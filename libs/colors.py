# !/usr/bin/python
# this is a simple tutorial about linux terminal coloring

class COLORS:
    def __init__(self):
        self.Black   = '\u001b[30m'
        self.Red     = '\u001b[31m'
        self.Green   = '\u001b[32m'
        self.Yellow  = '\u001b[33m'
        self.Blue    = '\u001b[34m'
        self.Magenta = '\u001b[35m'
        self.Cyan    = '\u001b[36m'
        self.White   = '\u001b[37m'

        self.back_Black   = '\u001b[40m'
        self.back_Red     = '\u001b[41m'
        self.back_Green   = '\u001b[42m'
        self.back_Yellow  = '\u001b[43m'
        self.back_Blue    = '\u001b[44m'
        self.back_Magenta = '\u001b[45m'
        self.back_Cyan    = '\u001b[46m'
        self.back_White   = '\u001b[47m'

        self.RESET   = '\u001b[0m'
        self.BOLD    = '\u001b[1m'
        self.DARKEN  = '\u001b[2m'
        self.ITALIC  = '\u001b[3m'
        self.ULINE   = '\u001b[4m'