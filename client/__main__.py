import hashlib
import zlib
from socket import socket
from argparse import ArgumentParser

from datetime import datetime
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
parser.add_argument(
    '-m', '--mode', type=str, default='r',
    required=False, help='Sets config file path'
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


def write(sock):
    hash_obj = hashlib.sha256()
    hash_obj.update(
        str(datetime.now().timestamp()).encode()
    )

    action = input('Enter action: ')
    data = input('Enter data: ')

    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
        'token': hash_obj.hexdigest()
    }

    s_request = json.dumps(request)
    b_request = zlib.compress(s_request.encode())
    sock.send(b_request)
    print(f'Client send data: {data}')


def read(sock):
    comporessed_response = sock.recv(default_config.get('buffersize'))

    b_response = zlib.decompress(comporessed_response)

    print(b_response.decode())


sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

print(f'Client was started')

try:
    while True:
        if args.mode == 'w':
            write(sock)

        elif args.mode == 'r':
            read(sock)
except KeyboardInterrupt:
    sock.close()
    print('Client shutdown')
