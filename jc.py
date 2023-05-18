#!/usr/bin/env python3

import argparse
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError

# Define the command-line arguments and options
parser = argparse.ArgumentParser(description="Run Junos commands remotely using PyEZ")
parser.add_argument("-d", "--device", metavar="<device>",
                    help="the device to run the command on")
parser.add_argument("-c", "--command", metavar="<command>",
                    help="the command to run")
parser.add_argument("-i", "--inventory-file", metavar="<device_list_file>",
                    help="read devices from inventory file")
parser.add_argument("-m", "--command-file", metavar="<command_list_file>",
                    help="read commands from command file")
parser.add_argument("-u", "--username", metavar="<username>",
                    help="the username to authenticate with")
parser.add_argument("-p", "--password", metavar="<password>",
                    help="the password to authenticate with")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="display verbose output")

# Parse the command-line arguments and options
args = parser.parse_args()
# print(args)

# Read the devices from a file, if specified
if args.inventory_file:
    with open(args.inventory_file) as f:
        devices = [line.strip() for line in f]
# Read the devices from the command-line arguments, if specified
elif args.device:
    devices = [args.device]
# If no devices are specified, display an error message and exit
else:
    parser.error("no devices specified")

# Read the commands from a file, if specified
if args.command_file:
    with open(args.command_file) as f:
        commands = [line.strip() for line in f]
# Read the command from the command-line arguments, if specified
elif args.command:
    commands = [args.command]
# If no command is specified, display an error message and exit
else:
    parser.error("no command specified")

# Prompt the user for their username and password, if not specified
if not args.username:
    username = input("Enter your RIMNET username: ")
else:
    username = args.username

if not args.password:
    password = getpass()
else:
    password = args.password

# Loop through each device and run each command
for device in devices:
    for command in commands:
        if args.verbose:
            print(f"Running command '{command}' on device '{device}'...")
        try:
            dev = Device(host=device, user=username, password=password)
            dev.open()
            output = dev.rpc.cli(command, format="text").text
            print(f"\nDevice: {device}\n")
            print(output)
            dev.close()
        except ConnectError as e:
            print(f"Failed to connect to device {device}: {e}")
