#!/usr/bin/env python3.13

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Dane
menu = [
    {"id": 1, "name": "Margherita", "price": 10},
    {"id": 2, "name": "Pepperoni", "price": 12}
]
orders = {}
users = {}
admin_token = "secret_admin_token"

order_id_counter = 1

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _parse_post_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        return json.loads(post_data) if post_data else {}

    def do_GET(self):
        if self.path == '/menu':
            self._set_headers()
            self.wfile.write(json.dumps(menu).encode())
        elif self.path.startswith('/order/'):
            try:
                order_id = int(self.path.split('/')[-1])
                order = orders.get(order_id)
                if order:
                    self._set_headers()
                    self.wfile.write(json.dumps(order).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Order not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid order ID"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        global order_id_counter
        if self.path == '/order':
            data = self._parse_post_data()
            pizza_id = data.get('pizza_id')
            address = data.get('address')
            pizza = next((p for p in menu if p['id'] == pizza_id), None)
            if pizza and address:
                order = {
                    "id": order_id_counter,
                    "pizza_id": pizza_id,
                    "address": address,
                    "status": "preparing"
                }
                orders[order_id_counter] = order
                order_id_counter += 1
                self._set_headers(201)
                self.wfile.write(json.dumps(order).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid pizza ID or address"}).encode())
        elif self.path == '/menu':
            token = self.headers.get('Authorization')
            if token != admin_token:
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
                return
            data = self._parse_post_data()
            name = data.get('name')
            price = data.get('price')
            if name and price:
                new_pizza = {"id": len(menu) + 1, "name": name, "price": price}
                menu.append(new_pizza)
                self._set_headers(201)
                self.wfile.write(json.dumps(new_pizza).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid data"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_DELETE(self):
        if self.path.startswith('/order/'):
            try:
                order_id = int(self.path.split('/')[-1])
                order = orders.get(order_id)
                if not order:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Order not found"}).encode())
                    return
                if self.headers.get('Authorization') == admin_token:
                    del orders[order_id]
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Order cancelled by admin"}).encode())
                elif order['status'] != 'ready_to_be_delivered':
                    del orders[order_id]
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Order cancelled"}).encode())
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Order cannot be cancelled"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid order ID"}).encode())
        elif self.path.startswith('/menu/'):
            token = self.headers.get('Authorization')
            if token != admin_token:
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
                return
            try:
                pizza_id = int(self.path.split('/')[-1])
                pizza = next((p for p in menu if p['id'] == pizza_id), None)
                if pizza:
                    menu.remove(pizza)
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Pizza deleted"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Pizza not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid pizza ID"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
