#!/usr/bin/env python3

import argparse
import urllib3
import socket
from typing import Tuple
import sys
from contextlib import contextmanager


@contextmanager
def connection(ip, port, *args, **kwargs):
    connection = socket.create_connection(address=(ip, port))

    try:
        yield connection
    except:
        pass
    finally:
        connection.close()


def get(url):
    url = urllib3.util.url.parse_url(url)
    with connection(url.host, url.port or 80) as con:
        payload = (
            f"GET {url.path} HTTP/1.1\r\nHost: {url.host}\r\nConnection: close\r\n\r\n"
        )
        ok = con.send(payload.encode("utf-8"))
        if ok == 0:
            print("Failed to send request")
            sys.exit(1)

        return con.recv(1024)


def main(url):
    print(get(url).decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="client")
    parser.add_argument("url", help="URL to download")

    args = parser.parse_args()

    url = args.url

    # url = "http://info.cern.ch/hypertext/WWW/TheProject.html"

    main(url)
