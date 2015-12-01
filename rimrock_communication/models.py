from django.contrib.auth.models import User
from django.db import models



class Job(models.Model):
    user = models.ForeignKey(User)
    job_name = models.CharField(max_length=50)
    job_queue_id = models.CharField(max_length=100)
    sequence_read_url = models.URLField()
    proxy = models.TextField()
    output_file_path = models.TextField()
    workspace_directory = models.TextField()

    CREATED = 'C'
    QUEUED = 'Q'
    RUNNING = 'R'
    FINISHED = 'F'
    JOB_STATUS = (
        (CREATED, 'Not run'),
        (QUEUED, 'In queue'),
        (RUNNING, 'Running'),
        (FINISHED, 'Finished')
    )
    status = models.CharField(max_length=1, choices=JOB_STATUS, default=CREATED)
