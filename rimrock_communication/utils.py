import json
from datetime import timedelta
from django.utils import timezone
from django.utils.datetime_safe import datetime
import requests
from django.contrib import messages
from rimrock_communication.models import Job
from rimrock_communication.forms import JobForm, UserProxyForm
import re


def generate_command(job):
    config = {
        "script_path": "DNA/webapp_scripts/webapp.sh",
        "walltime": "000:10:00",
        "queue": "plgrid-testing",
    }

    output_path = job.output_file_path if job.output_file_path \
        else '{jobname}.txt'.format(jobname=job.job_name)

    return "qsub -l walltime={walltime} -q {queue} {script_path} -F '{output_path} {seq_url}'" \
        .format(walltime=config['walltime'],
                queue=config['queue'],
                script_path=config['script_path'],
                output_path=output_path,
                seq_url=job.sequence_read_url)

def generate_setup_command():
    config = {
        "script_path": "DNA/webapp_scripts/setup.sh",
        "walltime": "000:10:00",
        "queue": "plgrid-testing",
    }

    return "qsub -l walltime={walltime} -q {queue} {script_path} -F" \
        .format(walltime=config['walltime'],
                queue=config['queue'],
                script_path=config['script_path'])


def send_rimrock_command(command, proxy):
    data = {"host": "zeus.cyfronet.pl",
            "command": command}

    headers = {"Content-Type": "application/json",
               "PROXY": proxy}

    return requests.post("https://zlecaj.plgrid.pl/api/process", json=data, headers=headers, verify=False)


def refresh_jobs_rimrock_command(proxy):
    headers = {"Content-Type": "application/json",
               "PROXY": proxy}

    return requests.get("https://zlecaj.plgrid.pl/api/jobs", headers=headers, verify=False)


def dispatch_job(job, request):
    command = generate_command(job)
    print "Running command: ", command
    proxy = request.user.userproxy.proxy
    r = send_rimrock_command(command, proxy)
    try:
        print r.content
        r.raise_for_status()
        pattern = re.compile(r'(\d+).batch')
        job.job_queue_id = pattern.search(r.text).group(1)
        messages.add_message(request, messages.SUCCESS, "Successfully dispatched job. id = {0}"
                             .format(job.job_queue_id))
        job.status = Job.QUEUED
        job.save()

    except requests.exceptions.HTTPError:
        error_message = json.loads(r.content)['error_message']
        err_txt = "There was a problem with dispatching job. {0}" \
            .format(error_message)
        messages.add_message(request, messages.ERROR, err_txt)


def verify_proxy(request):
    proxy_form = UserProxyForm(request.POST)
    userproxy = proxy_form.save(commit=False)
    command = 'voms-proxy-info'
    r = send_rimrock_command(command, userproxy.proxy)
    try:
        r.raise_for_status()
        userproxy.user = request.user
        pattern = re.compile(r'timeleft\s+?:\s+?(.*?)\\n')
        timeleft = pattern.search(r.text).group(1)
        d = datetime.strptime(timeleft, "%H:%M:%S")
        userproxy.valid_until = timezone.now() + timedelta(hours=d.hour, minutes=d.minute)
        userproxy.save()
        return True

    except requests.exceptions.HTTPError:
        return False


def user_has_valid_proxy(user):
    if hasattr(user, 'userproxy'):
        return user.userproxy.valid_until > timezone.now()
    else:
        return False


def reload_jobs(user):
    command = "qstat -u $USER"

    response = send_rimrock_command(command, user.userproxy.proxy)
    print response.text
    jobs = user.job_set.all()
    for job in jobs:
        pattern = re.compile(
            r'(' +
            re.escape(job.job_queue_id) +
            r')\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
        groups = pattern.search(response.text)
        if groups:
            status = groups.group(10)
            if status == 'Q':
                job.status = Job.QUEUED
            if status == 'R':
                job.status = Job.RUNNING
        else:
            job.status = Job.FINISHED
        job.save()


def setup_environment(user):
    command = "git clone https://github.com/piotroramus/DNA.git"
    print send_rimrock_command(command, user.userproxy.proxy).text
    command = generate_setup_command
    print send_rimrock_command(command, user.userproxy.proxy).text

def load_output_job(job):
    path = "{0}.txt".format(job.job_name)
    if job.output_file_path:
        path = job.output_file_path
    command = "cat {0}".format(path)
    result = send_rimrock_command(command, job.user.userproxy.proxy)
    return json.loads(result.text)['standard_output']


def new_job(request):
    job_form = JobForm(request.POST)

    if job_form.is_valid():
        job = job_form.save(commit=False)
        job.user = request.user
        job.status = Job.CREATED
        job.created_time = timezone.now()
        job.save()
        dispatch_job(job, request)
        return True

    messages.add_message(request, messages.ERROR, job_form.errors)
    return False
