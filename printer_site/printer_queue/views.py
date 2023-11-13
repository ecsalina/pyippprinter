from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import loader

def main(request):
    return(render(request, "printer_queue/index.html"))
