from socket import socket
from argparse import ArgumentParser
from app import Application
import select
import json
import logging
import threading
from handlers import handle_default_request
from protocol import validate_request, make_response
from resolvers import resolve





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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

app = Application(
    default_config.get('host'),
    default_config.get('port'),
    default_config.get('buffersize'),
    handle_default_request
)

app.bind()
app.run()