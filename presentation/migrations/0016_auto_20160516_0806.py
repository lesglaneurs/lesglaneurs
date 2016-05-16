# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0015_auto_20160515_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='membership',
            new_name='role',
        ),
    ]
