from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import printers

def receive_request(request: HttpRequest):
    print(request)
    print("poop")
    return(HttpResponse(status=200))
