#!/usr/bin/env python3

import socket

from opentelemetry import metrics, trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from lib.otel import init_tracing
import lib.http

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)


def main():
    init_tracing("server.tls.noamtd.github.com")

    sock = socket.create_server(
        ("", 8080), family=socket.AF_INET, backlog=20, reuse_port=True
    )

    histogram = meter.create_histogram(
        "request_count", unit="1", description="number of requests"
    )

    while True:
        (s, addr) = sock.accept()

        histogram.record(1)

        with tracer.start_as_current_span("main") as span:
            span.add_event("accepted connection", {"addr": addr})
            process_http_request(s)


def process_http_request(sock: socket.socket):
    request = sock.recv(16000)
    req = lib.http.parse_request(request.decode("utf-8"))
    match req:
        case lib.http.Request():
            traceparent = req.headers.get("traceparent", None)

            ctx=None
            if traceparent is not None:
                ctx = TraceContextTextMapPropagator().extract(carrier={"traceparent": traceparent})

            with tracer.start_as_current_span("process_http_request", context=ctx) as span:
                span.add_event("processing request")
                span.set_attribute("http.method", req.method.value)
                span.set_attribute("http.path", req.path)

        case lib.http.ParseError():
            sock.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")

    sock.close()


if __name__ == "__main__":
    main()
