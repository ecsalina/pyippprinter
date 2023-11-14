from django.shortcuts import render

def main(request):
    return(render(request, "ipp_site/index.html"))
