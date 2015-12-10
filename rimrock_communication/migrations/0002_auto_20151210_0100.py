# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rimrock_communication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='dispatched_time',
            new_name='created_time',
        ),
    ]
