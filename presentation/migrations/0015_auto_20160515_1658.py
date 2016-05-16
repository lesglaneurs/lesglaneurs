# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import presentation.models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0014_auto_20160505_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_structure',
            field=models.ImageField(help_text=b'image de la structure globale du projet', null=True, upload_to=presentation.models.user_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='workers',
            field=models.TextField(help_text=b'participants au projet - b\xc3\xa9n\xc3\xa9voles, salari\xc3\xa9s', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(default=b'membre', help_text=b"Le role d'une personne pour un projet en particulier - membre par d\xc3\xa9faut", unique=True, max_length=128),
        ),
    ]
