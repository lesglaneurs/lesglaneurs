# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0011_auto_20160505_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
        migrations.AddField(
            model_name='person',
            name='projects',
            field=models.ManyToManyField(to='presentation.Project', through='presentation.Membership'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(to='presentation.Project'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='project',
            field=models.ForeignKey(to='presentation.Person'),
        ),
    ]
