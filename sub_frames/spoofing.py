# !/usr/bin/python

from libs.colors import COLORS
from os.path import dirname, realpath
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable


global program_path
global activated_option


devnull = open(devnull, 'w')
colors = COLORS()


global_dict = {
    'program_path' : program_path,
    'activated_option' : activated_option,
}


# definitions fo global program

def execfile_y(file_name, globals_variables):
    exec(compile(open(file_name, "rb").read(), file_name, 'exec'), globals_variables)


# defifnition for main program

def print_main_options():
    options = {
        'arp': 'Do ARP sfoofing, be the MITM and sniff data',
        'dns': 'Do DNS spoofing and redirect requests'
    }

    table_data = [[colors.BOLD + 'Option', colors.BOLD + 'Description' + colors.RESET]]
    for option in options:
        row_data = [option, options[option]]
        table_data.append(row_data)

    table = AsciiTable(table_data)
    print(table.table, end='\n\n')


# the main program

def main():
    global program_path
    global activated_option
    global global_dict

    # then enter the infinite command input section
    while True:
        # Input the command
        command = input("".join(activated_option) + ' > ')

        # if the command is use generation
        if command == 'use arp':
            activated_option.append(' {}spoof({}ARP{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            execfile_y(f'{program_path}/libs/spoofing/arp.py', global_dict)

        # if the command is to activate the listenet
        elif command == 'use dns':
            activated_option.append(' {}spoof({}DNS{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            execfile_y(f'{program_path}/libs/spoofing/dns.py', global_dict)

        # if the command is options or show options
        elif command == 'options' or command == 'show options':
            print_main_options()

        # if the ommcand is clear clrat the screen
        elif command == 'clear':
            call('clear', shell=True)

        # if the command is exit or quit breake the progrm
        elif command == 'quit' or command == 'exit':
            activated_option.remove('/spoofing')
            break

        elif command == 'help':
            logo_printer.print_help()

        elif command == '' or command == ' ':
            pass


        else:
            print(command)
            print(colors.Red + '[✘]Invalid command' + colors.RESET)



main()
