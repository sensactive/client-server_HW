import hashlib
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
sock.connect((host, port))

print('Client was started')

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

sock.send(s_request.encode())
print(f'Client send message: {data}')

data = sock.recv(default_config.get('buffersize'))
res = json.loads(data.decode())
print(res)
