# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0013_auto_20160505_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(to='presentation.Person'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='project',
            field=models.ForeignKey(to='presentation.Project'),
        ),
    ]
