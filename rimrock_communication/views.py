from django.contrib import messages

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
import requests
from rimrock_communication.forms import JobForm
from rimrock_communication.models import Job


class JobListView(ListView):
    model = Job
    template_name = 'rimrock_communication/index.html'

def new_job(request):
    job_form = JobForm(request.POST)

    if job_form.is_valid():
        job = job_form.save(commit=False)
        job.user = request.user
        job.save()
        return redirect('index')

    print job_form.errors
    return HttpResponse('Eeerr')


def new(request):
    if request.method == "GET":
        return render(request, 'rimrock_communication/new.html', {})
    elif request.method == "POST":
        return new_job(request)


def action(request):
    # data = {"host": "zeus.cyfronet.pl",
    #         "command": "date;echo yolo"}
    #
    # headers = { "Content-Type" : "application/json",
    #             "PROXY" : ""}
    #
    # r = requests.post("https://zlecaj.plgrid.pl/api/process", json=data, headers=headers, verify=False)
    #
    # messages.add_message(request, messages.INFO, r.content)
    return redirect('index')
