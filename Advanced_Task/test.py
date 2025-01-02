#!/usr/bin/env python3.13

import subprocess

print("This script tests if server.py and client.py work correctly")
subprocess.run(
    ["./client.py", "list_menu"]
)
print("creating an order")
subprocess.run(
    ["./client.py", "create_order", "-i", "1", "-a", "przykladowy_adres"]
)
print("checking order status")
subprocess.run(
    ["./client.py", "check_order_status", "-o", "1"]
)
print("canceling order")
subprocess.run(
    ["./client.py", "cancel_order", "-o", "1"]
)

print("using admin priviledges to add pizza")
subprocess.run(
    ["./client.py", "admin_add_pizza", "-t", "secret_admin_token", "-n", "hawajska", "--price", "15"]
)
print("checking if pizza was added to the menu")
subprocess.run(
    ["./client.py", "list_menu"]
)
print("using admin priviledges to add pizza")
subprocess.run(
    ["./client.py", "admin_delete_pizza", "-t", "secret_admin_token", "-i", "2"]
)
print("checking if pizza was deleted from the menu")
subprocess.run(
    ["./client.py", "list_menu"]
)
print("registering a user")
subprocess.run(
    ["./client.py", "register_user", "-u", "tomek", "-p", "123", "-a", "przykladowy_adres"]
)
print("creating an order using a user account")
subprocess.run(
    ["./client.py", "create_order", "-i", "1","-u", "tomek", "-p", "123"]
)

print("cancelling an order using admin priviledges")
subprocess.run(
    ["./client.py", "admin_cancel_order", "-t", "secret_admin_token","-o", "2"]
)