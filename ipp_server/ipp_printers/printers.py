from dataclasses import dataclass

@dataclass
class Attribute:
    attr_type: str
    key: str
    value: str


@dataclass
class Group:
    name: str
    attributes: [Attribute]

@dataclass
class Response:
    pass


class IppRequest:
    version : str
    operation: str
    request_id: int
    groups: [Group]
    file_name: str
    data: bytes

    def __init__(self, body: bytes | dict):
        if type(body) is bytes:
            body_dict = parse_requests(body)
        else:
            body_dict = body

        #prettify dict:
        self.version = f"{body_dict['version_number_major']}.{body_dict['version_number_minor']}"
#        self.operation = 
        #etc.

    @classmethod
    def parse_request(cls, body: bytes) -> dict:
        """
        Accepts the raw bytes from the POST body of an IPP request over HTTP(S)
        and returns a dictionary containing the parsed components.
        """
	operation_attributes_tag = b'\x01'
        job_attributes_tag = b'\x02'
        end_of_attributes_tag = b'\x03'
        printer_attributes_tag = b'\x04'
        unsupported_attributes_tag = b'\x05'
        
        delimiters = (b'\x01', b'\x02', b'\x03', b'\x04', b'\x05') #same as above
        
        body = Stream(body)
        
        try:
            version_number_major = int.from_bytes(body.pop(), signed=True)
            version_number_minor = int.from_bytes(body.pop(), signed=True)
            operation_id = int.from_bytes(body.pop(2), signed=True)
            request_id = int.from_bytes(body.pop(4), signed=True)
        
            body_dict = {
                    "version_number_major": version_number_major,
                    "version_number_minor": version_number_minor,
                    "operation_id": operation_id,
                    "request_id":request_id,
                    "attribute_groups": []}
           
            #actual decoding of POST body:
            while body.get() != end_of_attributes_tag:
                begin_attribute_group_tag = body.pop()
                attribute_group = []
                
                #decode attributes repeatedly
                while body.get() not in delimiters
                    value_tag = body.pop()
                    name_length = body.pop(2)
                    name = body.pop(name_length)
                    value_length = body.pop(2)
                    value = body.pop(value_length)
                    if name_length != 0: #this is an attribute-with-one-value
                        attribute = [name, value]
                        attribute_group[value_tag] = attribute
                    else: #this is an additional-value 
                        attribute.append(value)

                body_dict["attribute_groups"][begin_attribute_group_tag] = attribute_group

            data = body[9:] or b''
            body_dict["data"] = data

            return(body_dict)
        except IndexError:
            raise IppRequestParseError()

class IppRequestParseError(Exception):
    pass

class Stream():
    """
    Auxiliary class for accessing the POST body bytes.
    """
    def __init__(self, data: bytes):
        self.data = data
        self.index = 0

    def pop(size: int = 1):
        """Returns next `size` element(s) and increments index"""
        d = self.data[index:index+size]
        index += size
        return(d)

    def get(size: int = 1):
        """Returns next `size` element(s) without incrementing index"""
        return(self.data[index:index+size)

class Printer:
    def __init__(self):
        return

    def receive_request(self, request: IppRequest) -> None:
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

