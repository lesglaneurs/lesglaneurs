# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0004_auto_20160426_2046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='address',
            new_name='addresses',
        ),
    ]
