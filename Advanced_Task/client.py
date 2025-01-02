#!/usr/bin/env python3.13

import requests
import argparse

BASE_URL = "http://127.0.0.1:8000"

def list_menu():
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code == 200:
        for pizza in response.json():
            print(f"{pizza['id']}: {pizza['name']} (${pizza['price']})")
    else:
        print("failed to fetch menu")

def create_order(pizza_id, address=None, username=None, password=None):
    data = {"pizza_id": pizza_id, "address": address,"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/order", json=data)
    if response.status_code == 201:
        print(f"order created: {response.json()}")
    else:
        print("failed to create order:", response.json())

def check_order_status(order_id):
    response = requests.get(f"{BASE_URL}/order/{order_id}")
    if response.status_code == 200:
        print(f"order status: {response.json()}")
    else:
        print("failed to check order status")

def cancel_order(order_id):
    response = requests.delete(f"{BASE_URL}/order/{order_id}")
    if response.status_code == 200:
        print("order cancelled")
    else:
        print("failed to cancel order:", response.json())

def admin_add_pizza(token, name, price):
    headers = {"Authorization": token}
    data = {"name": name, "price": price}
    response = requests.post(f"{BASE_URL}/menu", json=data, headers=headers)
    if response.status_code == 201:
        print("pizza added")
    else:
        print("failed to add pizza:", response.json())

def admin_delete_pizza(token, pizza_id):
    headers = {"Authorization": token}
    response = requests.delete(f"{BASE_URL}/menu/{pizza_id}", headers=headers)
    if response.status_code == 200:
        print("pizza deleted")
    else:
        print("failed to delete pizza:", response.json())

def admin_cancel_order(token, order_id):
    headers = {"Authorization": token}
    response = requests.delete(f"{BASE_URL}/order/{order_id}", headers=headers)
    if response.status_code == 200:
        print("order cancelled")
    else:
        print("failed to cancel order:", response.json())

def register_user(username, password, address):
    data = {"username": username, "password": password, "address": address}
    response = requests.post(f"{BASE_URL}/register", json=data)
    if response.status_code == 201:
        print("user registered")
    else:
        print("failed to register")


   
   
parser = argparse.ArgumentParser(description="Pizza Ordering CLI")
parser.add_argument('command', help="Command to execute")
parser.add_argument('-i', '--pizza_id', type=int, help="Pizza ID")
parser.add_argument('-a', '--address', type=str, help="Delivery address")
parser.add_argument('-o', '--order_id', type=int, help="Order ID")
parser.add_argument('-t', '--token', type=str, help="Admin token")
parser.add_argument('-u', '--username', type=str, help="username")
parser.add_argument('-p', '--password', type=str, help="user password")
parser.add_argument('-n', '--name', type=str, help="Pizza name")
parser.add_argument('--price', type=float, help="Pizza price")

args = parser.parse_args()

if args.command == "list_menu":
    list_menu()
elif args.command == "create_order":
    if args.pizza_id and args.address  :
        create_order(args.pizza_id, args.address)
    elif args.pizza_id and args.username and args.password:
        create_order(args.pizza_id, None, args.username, args.password)
    else:
        print("you need to provide pizza_id from the menu and your address")
elif args.command == "register_user":
    if args.username and args.password and args.address:
        register_user(args.username, args.password, args.address)
    else:
        print("you need to provide name password and address")
elif args.command == "check_order_status":
    if args.order_id:
        check_order_status(args.order_id)
    else:
        print("order_id not provided")
elif args.command == "cancel_order":
    if args.order_id:
        cancel_order(args.order_id)
    else:
        print("order_id not provided")
elif args.command == "admin_add_pizza":
    if args.token and args.name and args.price:
        admin_add_pizza(args.token, args.name, args.price)
    else:
        print("you need to provide token, name and price")
elif args.command == "admin_delete_pizza":
    if args.token and args.pizza_id:
        admin_delete_pizza(args.token, args.pizza_id)
    else:
        print("you need to provide token and pizza_id")
elif args.command == "admin_cancel_order":
    if args.token and args.order_id:
        admin_cancel_order(args.token, args.order_id)
    else:
        print("you need to provide token and order_id")
else:
    print("invalid command.")
