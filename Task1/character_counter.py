#!/usr/bin/env python3.13
import argparse

parser = argparse.ArgumentParser( prog="character_counter",
		description="counts characters in a given string"
		)
parser.add_argument("-s", "--string", help="input string whose characters will be counted", required=True)

args = parser.parse_args()

chars = {}
print(args.string)
for char in args.string:
	if char in chars:
		chars[char] += 1
	else:
		chars[char] = 1
print(chars)
