from socket import socket
from argparse import ArgumentParser
import select
import json
import logging
import threading
from handlers import handle_default_request
from protocol import validate_request, make_response
from resolvers import resolve


def read(sock, connections, requests, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        if bytes_request:
            requests.append(bytes_request)


def write(sock, connection, response):
    try:
        sock.send(response)
    except Exception:
        connection.remove(sock)


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
    'host': '127.0.0.1',
    'port': 7777,
    'buffersize': 1024
}

if args.address:
    default_config['host'] = args.address
if args.port:
    default_config['port'] = args.port

host, port = (default_config.get('host'), default_config.get('port'))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

requests = []
connections = []

try:
    sock = socket()
    sock.bind((host, port,))
    sock.settimeout(0)
    sock.listen(5)

    logging.info(f'Server was started with {host}:{port}')

    while True:
        try:
            client, address = sock.accept()

            connections.append(client)

            logging.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {connections}')
        except Exception:
            pass

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for r_client in rlist:
            r_thread = threading.Thread(
                target=read, args=(r_client, connections, requests, default_config.get('buffersize'))
            )
            r_thread.start()

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_thread = threading.Thread(
                    target=write, args=(w_client, connections, b_response)
                )
                w_thread.start()

except KeyboardInterrupt:
    logging.info('Server shutdown')
