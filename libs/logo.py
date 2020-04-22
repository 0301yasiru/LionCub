# !/usr/bin/python

class PrintLogo:
    def __init__(self, program_path):
        self.program_path = program_path
        self.COLORS = {
        "white":"\u001b[37m",
        "reset":"\u001b[0m",
        "bold": "\u001b[1m",
        "hair": "\u001b[38;5;11m",
        "face": "\u001b[38;5;208m",
        "eye": "\u001b[38;5;31m",
        "lion": "\u001b[38;5;124m"
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
