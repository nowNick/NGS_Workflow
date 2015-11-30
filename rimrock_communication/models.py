from django.contrib.auth.models import User
from django.db import models



class Job(models.Model):
    user = models.ForeignKey(User)
    job_name = models.CharField(max_length=50)
    sequence_read_url = models.URLField()
    proxy = models.TextField()
    output_file_path = models.TextField()
    workspace_directory = models.TextField()
