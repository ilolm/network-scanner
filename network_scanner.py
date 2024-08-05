#!/usr/bin/env python3

import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-r", "--range", dest="ip_range", help="Specify an IP address range.")
    parser.add_option("-i", "--iface", dest="iface", default="eth0", help="Select an interface. Default - \"eth0\"")
    options = parser.parse_args()[0]
    if not options.ip_range:
        parser.error("\033[91m[-] Please specify a ip_range, use --help for more info.")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    try:
        return scapy.srp(arp_request_broadcast, iface=options.iface, timeout=1, verbose=False)[0]
    except:
        print(f"\033[91m[-] Cannot find any device inside the network.")
        exit()

def parse_the_result(answered):
    end_list_result = []

    for element in answered:
        end_list_result.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return end_list_result

def print_result(end_list_result):
    print("-----------------------------------------")
    print("IP\t\t\tMAC address")
    print("-----------------------------------------")

    for client in end_list_result:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
answered_list = scan(options.ip_range)
end_list_result = parse_the_result(answered_list)
print_result(end_list_result)
