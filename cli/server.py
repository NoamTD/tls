#!/usr/bin/env python3

import argparse
import urllib3
import socket
from typing import Tuple
import sys

def main():
    sock = socket.create_server(('', 8080), family=socket.AF_INET, backlog=20, reuse_port=True)

    while True:
        (s, addr) = sock.accept()
        print(f'received connection from {addr}')
        process_http_request(s)
        

def process_http_request(sock):
    r = sock.recv(16000)
    print(r.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    args = parser.parse_args()

    main()
