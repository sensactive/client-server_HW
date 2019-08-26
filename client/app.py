import zlib
import json
import logging
import hashlib
import threading
from socket import socket
from datetime import datetime

from protocol import make_request


class Application:
    def __init__(self, host, port, buffersize):
        self._host = host
        self._port = port
        self._buffersize = buffersize

        self._sock = None

    def __enter__(self):
        if not self._sock:
            self._sock = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = 'Client stopped with error'
        logging.info(message)
        self._sock.close()
        return True

    def connect(self):
        if not self._sock:
            self._sock = socket()
        self._sock.connect((self._host, self._port))

    def read(self):
        compressed_response = self._sock.recv(self._buffersize)
        b_response = zlib.decompress(compressed_response)
        logging.info(b_response.decode())

    def write(self):
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = make_request(action, data, hash_obj.hexdigest())
        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode())
        self._sock.send(b_request)

    def run(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

        while True:
            self.write()
