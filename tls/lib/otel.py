from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (ConsoleMetricExporter,
                                              PeriodicExportingMetricReader)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter



def init_tracing(service_name):
    resource = Resource.create({SERVICE_NAME: service_name})

    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace_provider.add_span_processor(BatchSpanProcessor(JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )))

    metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    metric_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)

    # Sets the global default meter provider
    metrics.set_meter_provider(metric_provider)

    # Sets the global default tracer provider
    trace.set_tracer_provider(trace_provider)