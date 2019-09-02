import zlib
import json
import logging
import hashlib
import threading
from socket import socket
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from protocol import make_request
from utils import get_chunk


class Application:
    def __init__(self, host, port, buffersize):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._sock = socket()

    def __enter__(self):
        self._sock.connect((self._host, self._port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = 'Client stopped with error'
        logging.info(message, exc_info=exc_val)
        self._sock.close()
        return True


    def connect(self):
        self._sock.connect((self._host, self._port))

    def read(self):
        comporessed_response = self._sock.recv(self._buffersize)
        encrypted_response = zlib.decompress(comporessed_response)

        nonce, encrypted_response = get_chunk(encrypted_response, 16)
        key, encrypted_response = get_chunk(encrypted_response, 16)
        tag, encrypted_response = get_chunk(encrypted_response, 16)

        cipher = AES.new(key, AES.MODE_EAX, nonce)

        raw_responce = cipher.decrypt_and_verify(encrypted_response, tag)
        logging.info(raw_responce.decode())

    def write(self):
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)

        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = make_request(action, data, hash_obj.hexdigest())
        bytes_request = json.dumps(request).encode()
        encrypted_request, tag = cipher.encrypt_and_digest(bytes_request)

        bytes_request = zlib.compress(
            b'%(nonce)s%(key)s%(tag)s%(data)s' % {
                b'nonce':cipher.nonce, b'key':key, b'tag': tag, b'data': encrypted_request
            }
        )
        self._sock.send(bytes_request)

    def run(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

        while True:
            self.write()
