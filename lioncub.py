from terminaltables import AsciiTable
from os.path import dirname, realpath
from libs.colors import COLORS
from os import system
from libs.logo import PrintLogo

colors = COLORS()
program_path = dirname(realpath(__file__))
graphic_printer = PrintLogo(program_path)
activated_option = [f'{colors.Red}@{colors.RESET}LionCub']

global_dict = {
    'program_path' : program_path,
    'activated_option' : activated_option
}

def execfile_y(file_name, globals_variables):
    """
    file_name: this is the name of the file name to be executed
    global_variables: this is a dectionary of global variables to be passed
    """
    exec(compile(open(file_name, "rb").read(), file_name, 'exec'), globals_variables)


def print_main_options():
    options = {
        'keylogger': 'Use this option to generate keyloggers',
        'backdoor': 'Use this options to read logged keys of all victims'
    }

    table_data = [[colors.BOLD + 'Option', colors.BOLD + 'Description' + colors.RESET]]
    for option in options:
        row_data = [option, options[option]]
        table_data.append(row_data)

    table = AsciiTable(table_data)
    print(table.table, end='\n\n')


def main():
    """
    DOCSTRING: this is the main program thi program will loop over withcommands
    """
    global global_dict
    global activated_option
    global program_path

    system('clear')
    graphic_printer.print()

    while True:
        # Input the command
        command = input("".join(activated_option) + ' > ')

        if command == 'options' or command == 'show options':
            print_main_options()

        elif command == 'use keylogger':
            activated_option.append('/KeyLogger')
            execfile_y('sub_frames/keylogger.py', global_dict)

        elif command == 'exit' or command == 'quit':
            break

        elif command == 'clear':
            system('clear')

        elif command == '' or command == ' ':
            pass

        else:
            print(colors.Red + "[✘]Invalid Command use 'help' command to view help" + colors.RESET)

    
main()