from argparse import ArgumentParser
from app_client import Application


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

app = Application(
    default_config.get('host'),
    default_config.get('port'),
    default_config.get('buffersize'))

app.connect()
app.run()
