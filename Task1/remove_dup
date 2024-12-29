#!/usr/bin/env python3.13

import argparse

p = argparse.ArgumentParser()

p.add_argument('-a', nargs="+", type=int)

args = p.parse_args()

nums = args.a
print("given list of integers: ")
print(nums)

nums = list(dict.fromkeys(nums))

print("numbers list without duplicates: ")
print(nums)

print("smallest number in the list: " + str(min(nums)))

print("biggest number in the list: " + str(max(nums)))
