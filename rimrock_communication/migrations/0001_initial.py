# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_name', models.CharField(max_length=50)),
                ('job_queue_id', models.CharField(max_length=100)),
                ('sequence_read_url', models.URLField()),
                ('proxy', models.TextField()),
                ('output_file_path', models.TextField()),
                ('workspace_directory', models.TextField()),
                ('status', models.CharField(default=b'C', max_length=1, choices=[(b'C', b'Not run'), (b'Q', b'In queue'), (b'R', b'Running'), (b'F', b'Finished')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
