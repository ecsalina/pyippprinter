from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.utils.html import escape
from . import printers

def receive_request(request: HttpRequest):
    ipp_request = decode_request(request.body)
    print(request.META)
#    print(request.body.decode("ascii"))
    print(request.body)
    print(request.body[0:2])
    print(request.body[2:4])
    print(request.body[4:8])
    print(request.body[8:])
    print(request.body[4])
    print(request.body[5])
    print(request.body[6])
    print(request.body[7])
    print(request.body[8])
    return(HttpResponse(status=200))

def decode_request(body: bytes) -> printers.IppRequest:
    operation_attributes_tag = b'\x01'
    job_attributes_tag = b'\02'
    end_of_attributes_tag = b'\x03'
    printer_attributes_tag = b'\x04'
    unsupported_attributes_tag = b'\x05'

    try:
        version_number_major = int.from_bytes(body[0], signed=True)
        version_number_minor = int.from_bytes(body[1], signed=True)
        operation_id = int.from_bytes(body[2:4], signed=True)
        request_id = int.from_bytes(body[4:8], signed=True)

        index = 8
        prev_begin_attribute_group_tag = body[index]
        
        while body[index] != end_of_attributes_tag:
            begin_attribute_group_tag = body[index]
            while begin_attribute_group_tag != prev_begin_attribute_group_tag:
                #decode single attribute
                value_tag = body[index+1]
                name_length = body[index+2:index+4]
                name = body[index+4:index+4+name_length]
                value_length = body[

            #save old group and start new group
            prev_begin_attribute_group_tag = begin_attribute_group_tag
            index += 1
                
            


        data = body[9:] or b''
        return(printers.IppRequest()) #TODO fill in attributes
        except IndexError:
            raise IppRequestParseError()


class IppRequestParseError(Exception)
    pass













