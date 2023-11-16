from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.utils.html import escape
from . import printers

def receive_request(request: HttpRequest):
    ipp_request = decode_request(request.body)
    print(request.META) #DEBUG
    print(request.body) #DEBUG
    return(HttpResponse(status=200))

def decode_request(body: bytes) -> printers.IppRequest:
    operation_attributes_tag = b'\x01'
    job_attributes_tag = b'\02'
    end_of_attributes_tag = b'\x03'
    printer_attributes_tag = b'\x04'
    unsupported_attributes_tag = b'\x05'

    body = Stream(body)

    try:
        version_number_major = int.from_bytes(body.pop(), signed=True)
        version_number_minor = int.from_bytes(body.pop(), signed=True)
        operation_id = int.from_bytes(body.pop(2), signed=True)
        request_id = int.from_bytes(body.pop(4), signed=True)

        prev_begin_attribute_group_tag = body.get()
        
        while body.get() != end_of_attributes_tag:
            begin_attribute_group_tag = body.pop()
            while begin_attribute_group_tag != prev_begin_attribute_group_tag:
                #decode single attribute
                #decode one value of attribute
                while body.get() != end#################################
                value_tag = body.pop()
                name_length = body.pop(2)
                name = body.pop(name_length)
                value_length = body.pop(2)
                value = body.pop(value_length)
                #decode additional values of attribute
                while body.get() == value_tag:  #as opposed to next attribute or attribute group
                   value_tag = body.pop() #don't really need this as should be same
                   name_length = 

            #save old group and start new group
            prev_begin_attribute_group_tag = begin_attribute_group_tag
            index += 1
                
            


            data = body[9:] or b''
            return(printers.IppRequest()) #TODO fill in attributes
    except IndexError:
        raise IppRequestParseError()


class IppRequestParseError(Exception):
    pass


class Stream():
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








