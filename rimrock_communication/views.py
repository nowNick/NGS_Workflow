from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
import requests

def index(request):
    return render(request, 'rimrock_communication/index.html', {})


def action(request):
    data =  { "host" : "zeus.cyfronet.pl",
              "command" : "date;echo yolo" }

    headers = { "Content-Type" : "application/json",
                "PROXY" : ""}

    r = requests.post("https://zlecaj.plgrid.pl/api/process", json = data, headers=headers, verify=False)

    messages.add_message(request, messages.INFO, r.content)
    return redirect('index')