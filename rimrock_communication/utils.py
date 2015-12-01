import json
import requests
from django.contrib import messages
from rimrock_communication.models import Job
from rimrock_communication.forms import JobForm


def generate_command(job):
    config = {
        "script_path": "dev/dna/webapp.sh",
        "walltime": "000:10:00",
        "queue": "plgrid-testing",
    }

    output_path = job.output_file_path if job.output_file_path \
        else '{jobname}.txt'.format(jobname=job.job_name)

    return "qsub -l {walltime} -q {queue} {script_path} {output_path}" \
        .format(walltime=config['walltime'],
                queue=config['queue'],
                script_path=config['script_path'],
                output_path=output_path)


def dispatch_job(job, request):
    data = {"host": "zeus.cyfronet.pl",
            "command": generate_command(job)}

    headers = {"Content-Type": "application/json",
               "PROXY": job.proxy}

    r = requests.post("https://zlecaj.plgrid.pl/api/process", json=data, headers=headers, verify=False)
    try:
        r.raise_for_status()
        print r.content
        messages.add_message(request, messages.SUCCESS, "Successfully dispatched job.")
        job.status = Job.QUEUED
        job.save()

    except requests.exceptions.HTTPError:
        error_message = json.loads(r.content)['error_message']
        err_txt = "There was a problem with dispatching job. {0}"\
            .format(error_message)
        messages.add_message(request, messages.ERROR, err_txt)


def new_job(request):
    job_form = JobForm(request.POST)

    if job_form.is_valid():
        job = job_form.save(commit=False)
        job.user = request.user
        job.status = Job.CREATED
        job.save()
        dispatch_job(job, request)
        return True

    print job_form.errors
    return False
