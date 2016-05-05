# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0008_auto_20160505_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'membre', help_text=b"Le role d'une personne pour un projet en particulier", max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Le pr\xc3\xa9nom de la personne', max_length=128)),
                ('surname', models.CharField(help_text=b'Le nom de la personne', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserProjectRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='presentation.Project')),
                ('role', models.ForeignKey(to='presentation.Role')),
                ('user', models.ForeignKey(to='presentation.User')),
            ],
        ),
    ]
