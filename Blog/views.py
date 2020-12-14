from django.shortcuts import render
from django.http import HttpResponse
from .models import Looked

# Create your views here.
def index(request):
    lol = Looked.objects.all()
    context = {
        "lol": lol
    }
    return render(request,'index.html',context=context)