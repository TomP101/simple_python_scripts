#!/usr/bin/env python3.13

import argparse
import platform
import psutil
import os
import subprocess
import socket

parser = argparse.ArgumentParser(description="getting system info")
parser.add_argument("-d","--distro", action="store_true", help="show distro info")
parser.add_argument("-m","--memory", action="store_true", help="show memory info")
parser.add_argument("-c","--cpu", action="store_true", help="show CPU info")
parser.add_argument("-l","--load", action="store_true", help="show system load average")
parser.add_argument("-i","--ip", action="store_true", help="show ip addresses")
parser.add_argument("-u","--user", action="store_true", help="show user info")

args = parser.parse_args()

if args.distro:
	print("Distro info:")
	print(platform.platform())


if args.memory:
	memory = psutil.virtual_memory()
	print("total")
	print(f"{memory.total / (1024 ** 3):.2f} GB")
	print("available")
	print(f"{memory.available / (1024 ** 3):.2f} GB")

if args.cpu:
	print("CPU info:")
	print("model")
	print(platform.processor())
	print("number of cores")
	print(psutil.cpu_count(logical=false))
	print("threads")
	print(psutil.cpu_count(logical=True))

if args.load:
	print("System load average:")
	load_avg=os.getloadavg()
	print("1 min:" + str(load_avg[0]))
	print("5 min:" + str(load_avg[1]))
	print("15 min:" + str(load_avg[2]))

if args.ip:
	ip = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True)
	print(ip.stdout.decode())

if args.user:
	print("User Info:")
	print(os.getlogin())