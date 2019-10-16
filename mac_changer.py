#!/usr/bin/env python

import subprocess
import argparse
import re

# Script to change the mac address of a Linux machine:

# 1. Parse command line arguments
# 2. Change mac address of specified interface
# 3. Check if mac address has successfully been changed


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="interface", help="The network interface")
    parser.add_argument("--mac", dest="mac", help="The new mac address")
    args = parser.parse_args()
    if not (args.interface or args.mac):
        parser.error("Please specify a valid interface and mac")
    else:
        return args


def change_mac(interface, new_mac):
    print(">> Changing mac address of " + interface + " to: " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_curr_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    found_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    return found_mac.group(0) if found_mac else -1


args = get_args()
change_mac(args.interface, args.mac)

if get_curr_mac(args.interface) == args.mac:
    print(">> Successfully changed MAC to: " + args.mac)
else:
    print(">> Unable to change MAC")









