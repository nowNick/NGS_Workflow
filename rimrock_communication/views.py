# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from rimrock_communication.models import Job
from utils import new_job, user_has_valid_proxy, verify_proxy, reload_jobs, setup_environment, load_output_job


class JobListView(ListView):
    queryset = Job.objects.order_by('-created_time')
    model = Job
    template_name = 'rimrock_communication/index.html'

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        if not user_has_valid_proxy(self.request.user):
            context['proxy_invalid'] = True
        if not hasattr(self.request.user, 'userproxy'):
            context['first_run'] = True
        return context


def setup_proxy(request):
    if verify_proxy(request):
        return HttpResponse('Ok')
    return HttpResponseForbidden('Proxy invalid')


def refresh_jobs(request):
    reload_jobs(request.user)
    return redirect('all_jobs')


def first_run_configuration(request):
    setup_environment(request.user)
    return HttpResponse('Ok')


def refresh_output(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    output = load_output_job(job)
    ctx = {'job': job, 'output' : output}
    return render(request, 'rimrock_communication/detail.html', ctx)


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
            return redirect('new')
