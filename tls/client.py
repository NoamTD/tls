#!/usr/bin/env python3

from typing import Dict
import base64
from opentelemetry import trace
import urllib3
import socket
import sys
from contextlib import contextmanager
from lib.http import Method
from lib.otel import init_tracing
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace.get_tracer(__name__)

@contextmanager
def connection(ip, port, *args, **kwargs):
    connection = socket.create_connection(address=(ip, port))

    try:
        yield connection
    except:
        pass
    finally:
        connection.close()


def request(typ: Method, path: str, headers: Dict[str, str] = {}) -> str:
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier=carrier)

    try:
        headers["traceparent"] = carrier['traceparent']
    except Exception as e:
        print(e)
        pass

    return (
        "\r\n".join(
            [f'{typ.value} {path or "/"} HTTP/1.1']
            + [f"{k}: {v}" for k, v in headers.items()]
        )
        + "\r\n\r\n"
    )


def get(url):
    url = urllib3.util.url.parse_url(url)
    with connection(url.host, url.port or 80) as con:
        payload = request(Method.GET, url.path)

        trace.get_current_span().add_event("sending request", {"payload": payload})

        ok = con.send(payload.encode("utf-8"))
        if ok == 0:
            print("Failed to send request")
            sys.exit(1)

        return con.recv(1024)


def main(url):
    init_tracing("client.tls.noamtd.github.com")

    with tracer.start_as_current_span("main") as span:
        print(get(url).decode("utf-8"))


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(prog="client")
    # parser.add_argument("url", help="URL to download")

    # args = parser.parse_args()

    # url = args.url

    # url = "http://info.cern.ch/hypertext/WWW/TheProject.html"

    url = "127.0.0.1:8080"

    main(url)
