import requests
from dataclasses import dataclass

#requests.post()




class Printer:
    def __init__(self):
        pass

    def receive_request(self: Printer, request: Request) -> None:
#        match request.operation:
#            case "Create-Job":
#                self.create_job(request)
#            case "Send-Document":
#                self.send_document(request)
#            case "Print-Job":
#                self.print_job(request)
#            case "Get-Printer-Attributes":
#                self.get_printer_attributes(request)
#            case "Get-Jobs":
#                self.get_jobs(request)
#            case "Get-Job-Attributes":
#                self.get_job_attributes(request)
#            case "Cancel-Job":
#                self.cancel_job(request)
        print(request) #DEBUG
        return

@dataclass
class Request:
    version : str
    operation: str
    request_id: int
    groups: [Group]
    file_name: str
    data: str

    def __init__(self, data=None):
        if not data:
            return
        else:
            _parse_request(data)

    def _parse_request(data: str) -> None:
        #TODO: implement parser
        pass

    def __str__(self: Request): -> str:
        return(data)


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


