from dataclasses import dataclass
from typing import Union, List

DELIMITERS = {
        b'\x01': "operation-attributes",
        b'\x02': "job-attributes" ,
        b'\x03': "end-of-attributes",
        b'\x04': "printer-attributes",
        b'\x05': "unsupported-attributes"}

VALUE_TAGS = {
        #out-of-band types
        b'\x10': "unsupported",
        b'\x12': "unknown",
        b'\x13': "no-value",
        b'\x20': "unassigned-integer-data-type",
        #integer (adjacent) types
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
        #octet-string types
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
        #character-string types
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

#already in above dicts but useful to have separate
END_OF_ATTRIBUTES_TAG = b'\x03' 
BEGIN_COLLECTION_TAG = b'\x34'
END_COLLECTION_TAG = b'\x37'
MEMBER_ATTRIBUTE_TAG = b'\x4a'


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
    attributes: List[Attribute]

    def __str__(self):
        #TODO the first two columns of the group attributes table should have no maximum width,
        #while the third "value(s)" column should expand to fill the remainder of the terminal.
        #Need to find new table library
        import os
        from tabulate import tabulate
        table = []
        for attribute in self.attributes:
            table.append([attribute.name, attribute.attr_type, attribute.value])
        pretty_table = tabulate(
            table, tablefmt="simple",
            headers=["name", "type", "value(s)"],
            #max width for second column is len of largest type string
            maxcolwidths=[30, 36, os.get_terminal_size()[0]-66]).splitlines()
        table_len = len(pretty_table[1])
        string = self.name + "\n" + "-"*table_len + "\n" + "\n".join(pretty_table)
        return(string)


class IppParseError(Exception):
    pass


def raises_ipp_parse_error(f):
    def func(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            raise IppParseError()
    return(func)


class IppResponse:
    pass


class IppRequest:
    version: str
    operation: str
    request_id: int
    attribute_groups: List[Group]
    file_name: str
    data: bytes
    raw_bytes: bytes

    def __init__(self, body: Union[bytes, dict]):
        #parse values if not already parsed
        if type(body) is bytes:
            parsed_request = self.parse_request(body)
        else:
            parsed_request = body

        #assign values to self with special Group, Attribute data objects
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
        self.attribute_groups = groups


    @classmethod
    def _decode_op_id(cls, operation_id: bytes) -> dict:
        """Decodes `operation-id` into human-readable format"""
        o_dict = {"bytecode": operation_id} 
        try:
            o_dict["human_readable"] = OPERATION_IDS[operation_id]
        except KeyError:
            o_dict["human_readable"] = "Unknown-Operation"
        return(o_dict)

    @classmethod
    def _decode_group_tag(cls, group_tag: bytes) -> dict:
        """Decodes `begin-attribute-group-tag` into human-readable format"""
        g_dict = {"bytecode": group_tag}                
        try:
            g_dict["human_readable"] =  DELIMITERS[group_tag]
        except KeyError:
            g_dict["human_readable"] =  "unknown-attributes"
        return(g_dict)

    @classmethod
    def _decode_value_tag(cls, value_tag: bytes) -> dict:
        """Decodes `value-tag` into human-readable format"""
        v_dict = {"bytecode": value_tag} 
        try:
            v_dict["human_readable"] = VALUE_TAGS[value_tag]
        except KeyError:
            v_dict["human_readable"] = "type-reserved-for-future-use"
        return(v_dict)

    @classmethod
    def _decode_value(cls, value: bytes, attr_type: str, charset: str):
        """Decodes `value` into proper interpretation based on `value-tag`"""
        #TODO should be case/switch but need upgrade OS/python
        
        #out-of-band types 
        if attr_type in ["unsupported", "unknown", "no-value"]:
            return(None)

        #integer (adjacent) types
        elif attr_type in ["integer", "enum", "unassigned-integer-data-type"]:
            #the proper way to decode `unassigned-integer-data-type` is not in the documentation,
            #so I have inferred it to be the same as the other int types
            return(int.from_bytes(value, byteorder="big", signed=True))
        elif attr_type == "boolean":
            if value == b"\x00":
                return(False)
            elif value == b"\x01":
                return(True)

        #octet-string types
        elif attr_type in ["textWithLanguage"]:
            #string based on language supplied in the `value` itself
            value = Stream(value)
            language_size = int.from_bytes(value.pop(2), byteorder="big", signed=True)
            natural_language = value.pop(language_size).decode("us-ascii")
            text_size = int.from_bytes(value.pop(2), byteorder="big", signed=True)
            text = value.pop(text_size).decode(charset)
            return({"naturalLanguage": natural_language, "textWithoutLanguage": text})
        elif attr_type in ["nameWithLanguage"]:
            #string based on language supplied in the `value` itself
            value = Stream(value)
            language_size = int.from_bytes(value.pop(2), byteorder="big", signed=True)
            natural_language = value.pop(language_size).decode("us-ascii")
            name_size = int.from_bytes(value.pop(2), byteorder="big", signed=True)
            name = value.pop(name_size).decode(charset)
            return({"naturalLanguage": natural_language, "nameWithoutLanguage": name})
        elif attr_type == "dateTime":
            #`DateAndTime` type from RFC2579
            value = Stream(value)
            year = int.from_bytes(value.pop(2), byteorder="big", signed=False)
            month = int.from_bytes(value.pop(1), byteorder="big", signed=False)
            day = int.from_bytes(value.pop(1), byteorder="big", signed=False)
            hour = int.from_bytes(value.pop(1), byteorder="big", signed=False)
            minute = int.from_bytes(value.pop(1), byteorder="big", signed=False)
            second = int.from_bytes(value.pop(1), byteorder="big", signed=False)
            decisecond = int.from_bytes(value.pop(1), byteorder="big", signed=False)
            if value.get(1) != b'':
                utc_direction = value.pop(1).decode("us-ascii")
                hours_from_utc = int.from_bytes(value.pop(1), byteorder="big", signed=False)
                minutes_from_utc = int.from_bytes(value.pop(1), byteorder="big", signed=False)
                return({"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
                        "second":second, "decisecond": decisecond, "utc_direction": utc_direction,
                        "hours_from_utc": hours_from_utc, "minutes_from_utc": minutes_from_utc})
            else:
                return({"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
                        "second":second, "decisecond": decisecond})
        elif attr_type == "resolution":
            return({
            "cross_feed_direction_resolution":
                int.from_bytes(value[:4], byteorder="big", signed=True),
            "feed_direction_resolution":
                int.from_bytes(value[4:8], byteorder="big", signed=True),
            "units":
                int.from_bytes(value[8], byteorder="big", signed=True)})
        elif attr_type == "rangeOfInteger":
            return({
                "lower_bound":
                    int.from_bytes(value[:4], byteorder="big", signed=True),
                "upper_bound":
                    int.from_bytes(value[4:], byteorder="big", signed=True)})
        elif attr_type in ["octetString", "octet-string-with-unspecified-format",
                "unassigned-octet-string-data-type"]:
            #the proper way to decode `unassigned-octet-string-data-type` and
            #`octet-string-with-unspecified-format` is not in the documentation,
            #so I have inferred it to be the same as the other int types
            return(value)
        elif attr_type in ["begCollection", "endCollection"]:
            return(value) #value should be empty byte anyways
        
        #character-string types
        elif attr_type in ["textWithoutLanguage", "nameWithoutLanguage",
                "unassigned-character-string-data-type"]:
            #localized string based on `charset`
            #the proper way to decode `unassigned-character-string-data-type` is not in the
            #documentation, so I have inferred it to be a localized string
            return(value.decode(charset))
        elif attr_type in ["charset" ,"naturalLanguage", "mimeMediaType",
                "keyword", "uri","uriScheme", "memberAttrName"]:
            #us-ascii string
            return(value.decode("us-ascii"))
        


    #@raises_ipp_parse_error #TODO seems to be broken
    @classmethod
    def parse_request(cls, body: bytes) -> dict:
        """
        Accepts raw bytes from the POST body of an IPP request over HTTP(S) and returns a
        dictionary containing the parsed components in a human-readable format.

        Notes:
        I have deliberately chosen to separate this method out from the constructor of the
        IppRequest class in case anyone would like to call this function directly and receive a
        more lightweight dict which is more easily parsed by external libraries. This method is
        directly called by the constructor to populate the attribute_groups field of this class 
        with the heavier Group objects (which are themselves populated with Attribute objects).
        """
        if not body: raise IppParseError

        body = Stream(body)
       
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

        print(body_dict) #DEBUG

        charset = "us-ascii" #default charset
       
        #actual decoding of POST body:
        is_member_attribute = False
        is_additional_member_attribute = False
        while body.get() != END_OF_ATTRIBUTES_TAG:
            #called `begin-attribute-group-tag` in the documentation:
            group_name = cls._decode_group_tag(body.pop())
            attributes = []
            group = {"group_name": group_name, "attributes": attributes}
            
            #decode attributes repeatedly
            while body.get() not in DELIMITERS.keys():
                #called `value-tag` in the documentation:
                attr_type = cls._decode_value_tag(body.pop())
                name_length = int.from_bytes(body.pop(2), byteorder="big", signed=True)
                name = body.pop(name_length).decode("us-ascii")
                value_length = int.from_bytes(body.pop(2), byteorder="big", signed=True)
                value = cls._decode_value(body.pop(value_length),
                        attr_type["human_readable"], charset)

                print("type: ", attr_type) #DEBUG
                print("name_length: ", name_length) #DEBUG
                print("name: ", name) #DEBUG
                print("value_length: ", value_length) #DEBUG
                print("value: ", value) #DEBUG

                if name == "attributes-charset": #update charset value
                    charset = value
                
                if name_length != 0:
                    if attr_type == BEGIN_COLLECTION_TAG:
                        attribute = {"name": name, "type": attr_type, "value": []}
                        attributes.append(attribute)
                    elif attr_type == END_COLLECTION_TAG:
                        #discard
                        pass
                    else: #this is an `attribute-with-one-value`
                        attribute = {"name": name, "type": attr_type, "value": value}
                        attributes.append(attribute)
                else:
                    if attr_type == MEMBER_ATTRIBUTE_TAG: #first half of `member-attribute`
                        if value_length != 0:
                            attribute["value"].append({"name": value})
                            is_member_attribute = True
                        else:
                            is_additional_member_attribute = True
                    elif is_member_attribute:             #second half of `member-attribute`
                        attribute["value"][-1] |= {"type": attr_type, "value": value}
                        is_member_attribute = False
                    elif is_additional_member_attribute:
                        if type(attribute["value"][-1]["value"]) is not list:
                            attribute["value"][-1]["value"] = [attribute["value"][-1]["value"]]
                        attribute["value"][-1]["value"].append(value)
                        is_additional_member_attribute = False
                    else: #this is an `additional-value`
                        if type(attribute["value"]) is not list:
                            attribute["value"] = [attribute["value"]]
                        attribute["value"].append(value)

            body_dict["attribute_groups"].append(group)
        
        #want to discard the first elt as it is the `end-of-attributes-tag`
        body_dict["data"] = body.tail(1)

        return(body_dict)

    def __str__(self):
        string = f"version:    {self.version}\n" \
                 f"operation:  {self.operation['human_readable']}\n" \
                 f"request_id: {self.request_id}\n" \
                 f"attributes: \n\n"
        for group in self.attribute_groups:
            string += group.__str__() + "\n\n"
        return(string)


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
        """Returns next `size` element(s) without incrementing index.
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
    #status attributes
    printer_state: int
    printer_state_reasons: str
    #capability atributes
    capability_attributes: dict
    #information attributes
    printer_uri_supported: List[str]
    uri_authentication_supported: dict
    uri_security_supported: dict
    printer_info: str
    printer_more_info: str
    printer_location: str
    printer_geo_location: str

    def __init__(self):
        return

    def receive_request(self, request: IppRequest) -> None:
        #TODO should use match/case format but need to update python which requires updating OS
        if request.operation == "Create-Job":
            self.create_job(request)
        elif request.operation == "Send-Document":
            self.send_document(request)
        elif request.operation == "Print-Job":
            self.print_job(request)
        elif request.operation == "Get-Printer-Attributes":
            self.get_printer_attributes(request)
        elif request.operation == "Get-Jobs":
            self.get_jobs(request)
        elif request.operation == "Get-Job-Attributes":
            self.get_job_attributes(request)
        elif request.operation == "Cancel-Job":
            self.cancel_job(request)
        return

    def get_jobs(self):
        pass    
