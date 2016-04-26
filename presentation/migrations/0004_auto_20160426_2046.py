# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0003_auto_20160421_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.ManyToManyField(to='presentation.Address'),
        ),
    ]
