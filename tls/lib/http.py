from dataclasses import dataclass
import enum
from typing import Dict


class Method(enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

@dataclass
class Request:
    method: Method
    path: str
    headers: Dict[str, str]

@dataclass
class ParseError:
    error: str
    raw_request: str
    

def parse_request(raw_request: str) -> Request | ParseError:
    lines = [l for l in raw_request.splitlines() if l != '']

    request_line = lines[0]
    req_line_parts = request_line.split(' ')

    if len(req_line_parts) != 3:
        return ParseError('Invalid request line', raw_request)

    if req_line_parts[0] not in Method.__members__:
        return ParseError(f'Invalid request {req_line_parts[0]}', raw_request)

    headers = {}
    for line in lines[1:]:
        parts = line.split(': ')
        if len(parts) != 2:
            return ParseError(f'Invalid header {line}', raw_request)
        headers[parts[0]] = parts[1]

    return Request(
        method=Method.__members__[req_line_parts[0]],
        path=req_line_parts[1],
        headers=headers
    )