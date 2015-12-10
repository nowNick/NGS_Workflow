# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views.generic import ListView
from rimrock_communication.forms import UserProxyForm
from rimrock_communication.models import Job
from utils import new_job, user_has_valid_proxy, verify_proxy, reload_jobs


class JobListView(ListView):
    model = Job
    template_name = 'rimrock_communication/index.html'

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        if not user_has_valid_proxy(self.request.user):
            context['proxy_invalid'] = True
        return context


def setup_proxy(request):
    if verify_proxy(request):
            return HttpResponse('Ok')
    return HttpResponseForbidden('Proxy invalid')

def refresh_jobs(request):
    reload_jobs(request.user)
    return redirect('all_jobs')


def new(request):
    if request.method == "GET":
        ctx = {}
        if not user_has_valid_proxy(request.user):
            ctx['proxy_invalid'] = True
        return render(request, 'rimrock_communication/new.html', ctx)
    elif request.method == "POST":
        if new_job(request):
            return redirect('all_jobs')
        else:
            return HttpResponse('Eeerr')
