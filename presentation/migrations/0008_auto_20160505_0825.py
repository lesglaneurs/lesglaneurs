# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0007_auto_20160505_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='code',
            field=models.CharField(help_text=b'code postal', max_length=5),
        ),
    ]
