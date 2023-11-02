import requests
from dataclasses import dataclass

#requests.post()




class Printer:
    pass

@dataclass
class Request:
    version : str
    operation: str
    request_id: int
    groups: [Group]
    file_name: str

    def __init__(self, data=None):
        if not data:
            return
        else:
            _parse_request(data)

@dataclass
class Group:
    name: str
    attributes: [Attribute]

@dataclass
class Attribute:
    attr_type: str
    key: str
    value: str

@dataclass
class Response:
    pass


