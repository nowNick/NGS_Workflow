# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rimrock_communication.models import Job
from utils import new_job

class JobListView(ListView):
    model = Job
    template_name = 'rimrock_communication/index.html'

def new(request):
    if request.method == "GET":
        return render(request, 'rimrock_communication/new.html', {})
    elif request.method == "POST":
        if new_job(request):
            return redirect('all_jobs')
        else:
            return HttpResponse('Eeerr')
