from socket import socket
from argparse import ArgumentParser


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

sock = socket()
sock.connect((default_config.get('host'), default_config.get('port')))

message = input('Enter message: ')

sock.send(message.encode())
print(f'Client send message: {message}')
s_response = sock.recv(default_config.get('buffersize'))
print(f'Message from server: {s_response.decode()}')
