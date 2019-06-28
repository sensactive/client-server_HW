from socket import socket
from argparse import ArgumentParser

import timestamp as timestamp
import json

parser = ArgumentParser()

parser.add_argument(
    '-a', '--address', type=str,
    required=False, help='Set address'
)
parser.add_argument(
    '-p', '--port', type=int,
    required=False, help='Set port'
)
args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 7777,
    'buffersize': 1024
}

if args.address:
    default_config['host'] = args.address
if args.port:
    default_config['port'] = args.port

host, port = (default_config.get('host'), default_config.get('port'))
client_data = {
    "action": "presence",
    "time": timestamp(),
    "type": "status",
    "user": {
        "account_name":  "C0deMaver1ck",
        "status":      "Yep, I am here!"
    }
}

sock = socket()
sock.connect((host, port))

sock.send(json.dumps(client_data).encode())
print(f'Client send message: {client_data}')
s_response = sock.recv(default_config.get('buffersize'))
print(f'Message from server: {s_response.decode()}')
