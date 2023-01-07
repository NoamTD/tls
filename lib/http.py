from dataclasses import dataclass
import enum
from typing import Dict


class RequestType(str, enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

@dataclass
class HttpRequest:
    type: RequestType
    path: str
    headers: Dict[str, str]

class ParseError:
    error: str
    raw_request: str
    

def parse_request(raw_request: str) -> HttpRequest | ParseError:
    lines = raw_request.splitlines()

    request_line = lines[0]
    parts = request_line.split(' ')
    return 1