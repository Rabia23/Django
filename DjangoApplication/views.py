from django.shortcuts import render


# my view
def index(request):
    return render(request, "index.html")
