from dataclasses import dataclass
from typing import Union, List

@dataclass
class Attribute:
    attr_type: str
    bytecode: bytes
    name: str
    value: Union[str, List[str]]

    def __str__(self):
        string = self.name +" " + self.attr_type + " " + str(self.value)
        return(string)


@dataclass
class Group:
    name: str
    bytecode: bytes
    attributes: [Attribute]

    def __str__(self):
        from tabulate import tabulate
        table = []
        for attribute in self.attributes:
            table.append([attribute.name, attribute.attr_type, attribute.value])
        pretty_table = tabulate(
            table, tablefmt="simple",
            headers=["name", "type", "value(s)"],
            maxcolwidths=[None, None, 40]).splitlines()
        table_len = len(pretty_table[1])
        string = self.name + "\n" + "-"*table_len + "\n" + "\n".join(pretty_table)
        return(string)


class IppResponse:
    pass


class IppRequest:
    version: str
    operation: str
    request_id: int
    groups: List[Group]
    file_name: str
    data: bytes
    raw_bytes: bytes

    DELIMITERS = {
            b'\x01': "operation-attributes",
            b'\x02': "job-attributes" ,
            b'\x03': "end-of-attributes",
            b'\x04': "printer-attributes",
            b'\x05': "unsupported-attributes"}

    END_OF_ATTRIBUTES_TAG = b'\x03' #already above but useful to have separate

    VALUE_TAGS = {
            b'\x10': "unsupported",
            b'\x12': "unknown",
            b'\x13': "no-value",
            b'\x20': "unassigned-integer-data-type",
            b'\x21': "integer",
            b'\x22': "boolean",
            b'\x23': "enum",
            b'\x24': "unassigned-integer-data-type",
            b'\x25': "unassigned-integer-data-type",
            b'\x26': "unassigned-integer-data-type",
            b'\x27': "unassigned-integer-data-type",
            b'\x28': "unassigned-integer-data-type",
            b'\x29': "unassigned-integer-data-type",
            b'\x2a': "unassigned-integer-data-type",
            b'\x2b': "unassigned-integer-data-type",
            b'\x2c': "unassigned-integer-data-type",
            b'\x2d': "unassigned-integer-data-type",
            b'\x2e': "unassigned-integer-data-type",
            b'\x2f': "unassigned-integer-data-type",
            b'\x30': "octet-string-with-unspecified-format",
            b'\x31': "dateTime",
            b'\x32': "resolution",
            b'\x33': "rangeOfInteger",
            b'\x34': "begCollection",
            b'\x35': "textWithLanguage",
            b'\x36': "nameWithLanguage",
            b'\x37': "endCollection",
            b'\x38': "unassigned-octet-string-data-type", 
            b'\x39': "unassigned-octet-string-data-type",
            b'\x3a': "unassigned-octet-string-data-type",
            b'\x3b': "unassigned-octet-string-data-type",
            b'\x3c': "unassigned-octet-string-data-type",
            b'\x3d': "unassigned-octet-string-data-type",
            b'\x3e': "unassigned-octet-string-data-type",
            b'\x3f': "unassigned-octet-string-data-type",
            b'\x40': "unassigned-character-string-data-type",
            b'\x41': "textWithoutLanguage",
            b'\x42': "nameWithoutLanguage",
            b'\x44': "keyword",
            b'\x45': "uri",
            b'\x46': "uriScheme",
            b'\x47': "charset",
            b'\x48': "naturalLanguage",
            b'\x49': "mimeMediaType",
            b'\x4a': "memberAttrName",
            b'\x4b': "unassigned-character-string-data-type",
            b'\x4c': "unassigned-character-string-data-type",
            b'\x4d': "unassigned-character-string-data-type",
            b'\x4e': "unassigned-character-string-data-type",
            b'\x4f': "unassigned-character-string-data-type",
            b'\x50': "unassigned-character-string-data-type",
            b'\x51': "unassigned-character-string-data-type",
            b'\x52': "unassigned-character-string-data-type",
            b'\x53': "unassigned-character-string-data-type",
            b'\x54': "unassigned-character-string-data-type",
            b'\x55': "unassigned-character-string-data-type",
            b'\x56': "unassigned-character-string-data-type",
            b'\x57': "unassigned-character-string-data-type",
            b'\x58': "unassigned-character-string-data-type",
            b'\x59': "unassigned-character-string-data-type",
            b'\x5a': "unassigned-character-string-data-type",
            b'\x5b': "unassigned-character-string-data-type",
            b'\x5c': "unassigned-character-string-data-type",
            b'\x5d': "unassigned-character-string-data-type",
            b'\x5e': "unassigned-character-string-data-type",
            b'\x5f': "unassigned-character-string-data-type"}
        
    OPERATION_IDS = {
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


    def __init__(self, body: Union[bytes, dict]):
        #parse values if not already parsed
        if type(body) is bytes:
            parsed_request = self.parse_request(body)
        else:
            parsed_request = body

        #assign values to self while creating special data objects
        self.version = parsed_request["version"]
        self.operation = parsed_request["operation"]
        self.request_id = parsed_request["request_id"]
        self.data = parsed_request["data"]
        self.raw_bytes = parsed_request["raw_bytes"]
        groups = []
        for group in parsed_request["attribute_groups"]:
            attributes = []
            for attribute in group["attributes"]:
                attributes.append(Attribute(
                    attribute["type"]["human_readable"],
                    attribute["type"]["bytecode"],
                    attribute["name"],
                    attribute["value"]))
            groups.append(Group(
                group["group_name"]["human_readable"],
                group["group_name"]["bytecode"],
                attributes))
        self.groups = groups


    @classmethod
    def _decode_op_id(cls, operation_id: bytes) -> dict:
        """Decodes `operation-id` into human-readable format"""
        o_dict = {"bytecode": operation_id} 
        try:
            o_dict["human_readable"] = cls.OPERATION_IDS[operation_id]
        except KeyError:
            o_dict["human_readable"] = "Unknown-Operation"
        return(o_dict)

    @classmethod
    def _decode_group_tag(cls, group_tag: bytes) -> dict:
        """Decodes `begin-attribute-group-tag` into human-readable format"""
        g_dict = {"bytecode": group_tag}                
        try:
            g_dict["human_readable"] =  cls.DELIMITERS[group_tag]
        except KeyError:
            g_dict["human_readable"] =  "unknown-attributes"
        return(g_dict)

    @classmethod
    def _decode_value_tag(cls, value_tag: bytes) -> dict:
        """Decodes `value-tag` into human-readable format"""
        v_dict = {"bytecode": value_tag} 
        try:
            v_dict["human_readable"] = cls.VALUE_TAGS[value_tag]
        except KeyError:
            v_dict["human_readable"] = "type-reserved-for-future-use"
        return(v_dict)


    @classmethod
    def parse_request(cls, body: bytes) -> dict:
        """
        Accepts raw bytes from the POST body of an IPP request over HTTP(S) and returns a
        dictionary containing the parsed components in a human-readable format.
        """
        
        body = Stream(body)
       
        try:
            version_number_major = int.from_bytes(body.pop(), byteorder="big", signed=True)
            version_number_minor = int.from_bytes(body.pop(), byteorder="big", signed=True)
            version_number = float(f"{version_number_major}.{version_number_minor}")
            operation = cls._decode_op_id(body.pop(2))
            request_id = int.from_bytes(body.pop(4), byteorder="big", signed=True)
        
            body_dict = {
                    "raw_bytes": body.all(),
                    "version": version_number,
                    "operation": operation,
                    "request_id":request_id,
                    "attribute_groups": []}
           
            #actual decoding of POST body:
            while body.get() != cls.END_OF_ATTRIBUTES_TAG:
                #called `begin-attribute-group-tag` in the documentation
                group_name = cls._decode_group_tag(body.pop())
                attributes = []
                group = {"group_name": group_name, "attributes": attributes}
                
                #decode attributes repeatedly
                while body.get() not in cls.DELIMITERS.keys():
                    #called `value-tag` in the documentation
                    attr_type = cls._decode_value_tag(body.pop())
                    name_length = int.from_bytes(body.pop(2), byteorder="big", signed=True)
                    name = body.pop(name_length).decode()
                    value_length = int.from_bytes(body.pop(2), byteorder="big", signed=True)
                    value = body.pop(value_length).decode() #TODO implement decoding
                    if name_length != 0: #this is an `attribute-with-one-value`
                        attribute = {"name": name, "type": attr_type, "value": value}
                        attributes.append(attribute)
                    else: #this is an `additional-value`
                        if type(attribute["value"]) is not list:
                            attribute["value"] = [attribute["value"]]
                        attribute["value"].append(value)

                body_dict["attribute_groups"].append(group)
            
            #want to discard the first elt as it is the `end-of-attributes-tag`
            body_dict["data"] = body.tail(1)

            return(body_dict)
        except IndexError:
            raise IppRequestParseError()


    def __str__(self):
        string = f"version:    {self.version}\n" \
                 f"operation:  {self.operation['human_readable']}\n" \
                 f"request_id: {self.request_id}\n" \
                 f"attributes: \n\n"
        for group in self.groups:
            string += group.__str__() + "\n"
        return(string)


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
        """Returns the entire Stream data regardless of index, without incrementing the index."""
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

