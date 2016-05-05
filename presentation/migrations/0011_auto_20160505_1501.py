# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0010_auto_20160505_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('membership', models.CharField(default=b'membre', help_text=b"Le role d'une personne pour un projet en particulier", max_length=128)),
                ('person', models.ForeignKey(to='presentation.Person')),
                ('project', models.ForeignKey(to='presentation.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='personprojectrole',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personprojectrole',
            name='project',
        ),
        migrations.RemoveField(
            model_name='personprojectrole',
            name='role',
        ),
        migrations.DeleteModel(
            name='PersonProjectRole',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to='presentation.Person', through='presentation.Membership'),
        ),
    ]
