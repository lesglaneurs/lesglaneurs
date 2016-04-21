# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0002_address_eventaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventaddress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='eventaddress',
            name='event',
        ),
        migrations.AddField(
            model_name='address',
            name='events',
            field=models.ManyToManyField(to='presentation.Event'),
        ),
        migrations.DeleteModel(
            name='EventAddress',
        ),
    ]
