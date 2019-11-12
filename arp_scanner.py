#!/usr/bin/env python3

import scapy.all as scapy
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="The IP range")
    args = parser.parse_args()
    if not args.target:
        parser.error("Please specify a valid IP range")
    else:
        return args


# send arp request to ip
def discover(ip):
    arp_req = scapy.ARP(pdst=ip);
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast/arp_req
    answered = scapy.srp(arp_packet, timeout=1, verbose=False)[0]

    result = []
    for elt in answered:
        new_client = {"ip": elt[1].psrc, "mac": elt[1].hwsrc}
        result.append(new_client)
    return result


def print_table(results):
    header = "IP\t\tat MAC ADDRESS\n" \
             "------------------------------------"
    print(header)
    for elt in results:
        print(elt["ip"] + "\t\t" + elt["mac"])


print_table(discover(get_args().target))
