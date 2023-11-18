from dataclasses import dataclass
from typing import Union

@dataclass
class Attribute:
    attr_type: str
    name: str
    value: str


@dataclass
class Group:
    name: str
    attributes: [Attribute]


class IppResponse:
    pass


class IppRequest:
    version : str
    operation: str
    request_id: int
    groups: [Group]
    file_name: str
    data: bytes

    def __init__(self, body: Union[bytes, dict]):
        if type(body) is bytes:
            body_dict = self.parse_request(body)
        else:
            body_dict = body

        import pprint #DEBUG
        pprint.pprint(body_dict)  #DEBUG

        #prettify dict:
        #TODO etc.

    @classmethod
    def parse_request(cls, body: bytes) -> dict:
        """
        Accepts the raw bytes from the POST body of an IPP request over HTTP(S) and returns a
        dictionary containing the parsed components in a human-readable format.
        """

        #GET THE DATA 
        
        delimiters = {
                b'\x01': "operation-attributes-tag",
                b'\x02': "job-attributes-tag" ,
                b'\x03': "end-of-attributes-tag",
                b'\x04': "printer-attributes-tag",
                b'\x05': "unsupported-attributes-tag"}

        end_of_attributes_tag = b'\x03' #already above but useful to have separate

        value_tags = {
                b'\x10': "unsupported",
                b'\x12': "unknown",
                b'\x13': "no-value",
                b'\x21': "integer",
                b'\x22': "boolean",
                b'\x23': "enum",
                b'\x31': "dateTime",
                b'\x32': "resolution",
                b'\x33': "rangeOfInteger",
                b'\x34': "begCollection",
                b'\x35': "textWithLanguage",
                b'\x36': "nameWithLanguage",
                b'\x37': "endCollection",
                b'\x41': "textWithoutLanguage",
                b'\x42': "nameWithoutLanguage",
                b'\x44': "keyword",
                b'\x45': "uri",
                b'\x46': "uriScheme",
                b'\x47': "charset",
                b'\x48': "naturalLanguage",
                b'\x49': "mimeMediaType",
                b'\x4a': "memberAttrName"}
        
        operation_ids = {
                b'\x00\x02': "Print-Job",
                b'\x00\x03': "Print-URI",
                b'\x00\x04': "Validate-Job",
                b'\x00\x05': "Create-Job",
                b'\x00\x06': "Send-Document",
                b'\x00\x07': "Send-URI",
                b'\x00\x08': "Cancel-Job",
                b'\x00\x09': "Get-Job-Attributes",
                b'\x00\x0a': "Get-Jobs",
                b'\x00\x0b': "Get-Printer-Attributes",
                b'\x00\x0c': "Hold-Job",
                b'\x00\x0d': "Release-Job",
                b'\x00\x0e': "Restart-Job",
                b'\x00\x10': "Pause-Printer",
                b'\x00\x11': "Resume-Printer",
                b'\x00\x12': "Purge-Jobs"}



        body = Stream(body)
        
        try:
            version_number_major = int.from_bytes(body.pop(), byteorder="big", signed=True)
            version_number_minor = int.from_bytes(body.pop(), byteorder="big", signed=True)
            operation_id = operation_ids[body.pop(2)]
            request_id = int.from_bytes(body.pop(4), byteorder="big", signed=True)
        
            body_dict = {
                    "raw_bytes": body.all(),
                    "version_number": float(f"{version_number_major}.{version_number_minor}"),
                    "operation_id": operation_id,
                    "request_id":request_id,
                    "attribute_groups": {}}
           
            #actual decoding of POST body:
            while body.get() != end_of_attributes_tag:
                begin_attribute_group_tag = delimiters[body.pop()]
                attribute_group = {}
                
                #decode attributes repeatedly
                while body.get() not in delimiters.keys():
                    value_tag = value_tags[body.pop()]
                    name_length = int.from_bytes(body.pop(2), byteorder="big", signed=True)
                    name = body.pop(name_length).decode()
                    value_length = int.from_bytes(body.pop(2), byteorder="big", signed=True)
                    value = body.pop(value_length).decode()
                    if name_length != 0: #this is an attribute-with-one-value
                        attribute = [name, value]
                        attribute_group[value_tag] = attribute
                    else: #this is an additional-value 
                        attribute.append(value)

                body_dict["attribute_groups"][begin_attribute_group_tag] = attribute_group
            
            #want to discard the first elt as it is the end_of_attributes_tag
            body_dict["data"] = body.tail(1)

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

    def pop(self, size: int = 1):
        """Returns next `size` element(s) and increments index.
        If there are no more elements then the empty byte b'' is returned."""
        d = self.data[self.index:self.index+size]
        self.index += size
        return(d)

    def get(self, size: int = 1):
        """Returns next `size` element(s) without incrementing index
        If there are no more elements then the empty byte b'' is returned."""
        return(self.data[self.index:self.index+size])

    def tail(self, start=0):
        """Returns the rest of the elements, leaving Stream empty.
        If `start` is supplied, then discards the first `start` elements and returns the rest of
        the elements.
        If there are no more elements then the empty byte b'' is returned."""
        self.pop(start)
        return(self.data[self.index:])

    def all(self):
        """Returns the entire data Stream regardless of index, without incrementing the index."""
        return(self.data)

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

