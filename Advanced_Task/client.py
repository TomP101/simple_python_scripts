#!/usr/bin/env python3.13

import requests
import argparse
import sys

BASE_URL = "http://127.0.0.1:5000"

def list_menu():
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code == 200:
        for pizza in response.json():
            print(f"{pizza['id']}: {pizza['name']} (${pizza['price']})")
    else:
        print("Failed to fetch menu.")

def create_order(pizza_id, address):
    data = {"pizza_id": pizza_id, "address": address}
    response = requests.post(f"{BASE_URL}/order", json=data)
    if response.status_code == 201:
        print(f"Order created: {response.json()}")
    else:
        print("Failed to create order:", response.json())

def check_order_status(order_id):
    response = requests.get(f"{BASE_URL}/order/{order_id}")
    if response.status_code == 200:
        print(f"Order status: {response.json()}")
    else:
        print("Failed to check order status.")

def cancel_order(order_id):
    response = requests.delete(f"{BASE_URL}/order/{order_id}")
    if response.status_code == 200:
        print("Order cancelled.")
    else:
        print("Failed to cancel order:", response.json())

def admin_add_pizza(token, name, price):
    headers = {"Authorization": token}
    data = {"name": name, "price": price}
    response = requests.post(f"{BASE_URL}/menu", json=data, headers=headers)
    if response.status_code == 201:
        print("Pizza added.")
    else:
        print("Failed to add pizza:", response.json())

def admin_delete_pizza(token, pizza_id):
    headers = {"Authorization": token}
    response = requests.delete(f"{BASE_URL}/menu/{pizza_id}", headers=headers)
    if response.status_code == 200:
        print("Pizza deleted.")
    else:
        print("Failed to delete pizza:", response.json())

def admin_cancel_order(token, order_id):
    headers = {"Authorization": token}
    response = requests.delete(f"{BASE_URL}/order/{order_id}", headers=headers)
    if response.status_code == 200:
        print("Order cancelled.")
    else:
        print("Failed to cancel order:", response.json())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pizza Ordering CLI")
    parser.add_argument('command', help="Command to execute")
    parser.add_argument('--pizza_id', type=int, help="Pizza ID")
    parser.add_argument('--address', type=str, help="Delivery address")
    parser.add_argument('--order_id', type=int, help="Order ID")
    parser.add_argument('--token', type=str, help="Admin token")
    parser.add_argument('--name', type=str, help="Pizza name")
    parser.add_argument('--price', type=float, help="Pizza price")

    args = parser.parse_args()

    if args.command == "list_menu":
        list_menu()
    elif args.command == "create_order":
        if args.pizza_id and args.address:
            create_order(args.pizza_id, args.address)
        else:
            print("Missing arguments for create_order.")
    elif args.command == "check_order_status":
        if args.order_id:
            check_order_status(args.order_id)
        else:
            print("Missing order_id for check_order_status.")
    elif args.command == "cancel_order":
        if args.order_id:
            cancel_order(args.order_id)
        else:
            print("Missing order_id for cancel_order.")
    elif args.command == "admin_add_pizza":
        if args.token and args.name and args.price:
            admin_add_pizza(args.token, args.name, args.price)
        else:
            print("Missing arguments for admin_add_pizza.")
    elif args.command == "admin_delete_pizza":
        if args.token and args.pizza_id:
            admin_delete_pizza(args.token, args.pizza_id)
        else:
            print("Missing arguments for admin_delete_pizza.")
    elif args.command == "admin_cancel_order":
        if args.token and args.order_id:
            admin_cancel_order(args.token, args.order_id)
        else:
            print("Missing arguments for admin_cancel_order.")
    else:
        print("Invalid command.")
