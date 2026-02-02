import requests

ip_address = "https://alexandriatorch.onrender.com"

class Connection:
    def __init__(self, ip):
        self.ip = ip

        self.connected = None
        self.server_alive = False

    def connect_with_server(self):

        endpoint = "/connect"

        response = requests.get(ip_address + endpoint)
        result = response.json()

        if result.get("code", None) == 3:
            self.connected = True
        else:
            self.connected = False

    def push(self, data):
        endpoint = "/push"
        response = requests.post(ip_address + endpoint, json=data)

    def ping(self):
        endpoint = "/ping"
        response = requests.get(ip_address + endpoint)
        if response.json().get("code", None) == 2:
            self.server_alive = True
        else:
            self.server_alive = False

