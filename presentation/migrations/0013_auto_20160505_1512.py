# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0012_auto_20160505_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'membre', help_text=b"Le role d'une personne pour un projet en particulier", max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='membership',
            name='membership',
            field=models.ForeignKey(to='presentation.Role'),
        ),
    ]
