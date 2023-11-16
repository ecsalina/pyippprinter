from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.utils.html import escape
from . import printers

def receive_request(request: HttpRequest):
    print(request.META) #DEBUG
    print(request.body) #DEBUG
    try:
        ipp_request = printers.IppRequest(request.body)
    except:
        return(HttpResponse(status=500)
    else:
        return(HttpResponse(status=200)
