from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.utils.html import escape
from . import printers

def receive_request(request: HttpRequest):
#    try:
#        ipp_request = printers.IppRequest(request.body)
#    except:
#        return(HttpResponse(status=500))
#    else:
#        return(HttpResponse(status=200))
    print(request.META) #DEBUG
    ipp_request = printers.IppRequest(request.body)
    print(ipp_request)
    print("data: ")
    print(ipp_request.data)
    printer = printers.Printer()
    printer.receive_request(ipp_request)
    return(HttpResponse(status=200))
