# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0005_auto_20160426_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=15, blank=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=15, blank=True),
        ),
    ]
