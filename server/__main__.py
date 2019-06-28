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

try:

    sock = socket()
    sock.bind((host, port,))
    sock.listen(5)

    print(f'Server was started with {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client was connected with {address[0]}:{address[1]}')
        c_request = client.recv(default_config.get('buffersize'))
        print(f'Message from client: {c_request.decode()}')
        s_message = f'Your message: {c_request.decode()}'
        client.send(s_message.encode())
        client.close()


except KeyboardInterrupt:
    print(' Server shutdown')
