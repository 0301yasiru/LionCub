# !/usr/bin/python

class PrintLogo:
    def __init__(self, program_path):
        self.program_path = program_path
        self.COLORS = {\
        "black":"\u001b[30;1m",
        "red": "\u001b[31;1m",
        "green":"\u001b[32m",
        "yellow":"\u001b[33;1m",
        "blue":"\u001b[34;1m",
        "magenta":"\u001b[35m",
        "cyan": "\u001b[36m",
        "white":"\u001b[37m",
        "reset":"\u001b[0m",
        "uline": '\u001b[4m'
        }

    
    def __colorText(self, text):
        for color in self.COLORS:
            text = text.replace("[[" + color + "]]", self.COLORS[color])
        return text

    def print(self):
        f  = open(f"{self.program_path}/data/logo.txt","r")
        ascii = "".join(f.readlines())
        print(self.__colorText(ascii)) 
        f.close()

    def print_help(self):
        f  = open(f"{self.program_path}/data/help.txt","r")
        ascii = "".join(f.readlines())
        print(self.__colorText(ascii)) 
        f.close()