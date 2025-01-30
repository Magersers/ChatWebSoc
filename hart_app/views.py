from django.shortcuts import render

# Create your views here.
def index(requred):
    return render(requred,'index.html')