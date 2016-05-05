# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
import presentation.models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0006_auto_20160426_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(help_text=b'ville', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default=b'France', help_text=b'pays', max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(help_text=b'date de fin'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(help_text=b'date de d\xc3\xa9but'),
        ),
        migrations.AlterField(
            model_name='project',
            name='contact_name',
            field=models.CharField(help_text=b'nom du contact de r\xc3\xa9f\xc3\xa9rence', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='creation_date',
            field=models.PositiveIntegerField(help_text=b'date de cr\xc3\xa9ation', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='email',
            field=models.EmailField(help_text=b'email de contact', max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='location_target',
            field=models.ImageField(help_text=b"pr\xc3\xa9vision d'\xc3\xa9volution g\xc3\xa9ographique", null=True, upload_to=presentation.models.user_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='location_today',
            field=models.ImageField(help_text=b"pr\xc3\xa9sence du projet aujourd'hui", null=True, upload_to=presentation.models.user_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(help_text=b'photo du logo du projet', null=True, upload_to=presentation.models.user_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=datetime.datetime(2016, 5, 5, 8, 21, 29, 926663, tzinfo=utc), help_text=b'Le nom du projet', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='owner_image',
            field=models.ImageField(help_text=b'Photo du chef du projet', null=True, upload_to=presentation.models.user_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_structure',
            field=models.ImageField(help_text=b'image de la strcuture globale du projet', null=True, upload_to=presentation.models.user_directory_path, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='structure',
            field=models.CharField(help_text=b'structure administrative du projet', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='telephone',
            field=models.CharField(help_text=b'num\xc3\xa9ro de t\xc3\xa9l\xc3\xa9phone', max_length=14, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='web_site',
            field=models.URLField(help_text=b'site Web du projet', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='workers',
            field=models.TextField(help_text=b'participants au projet - b\xc3\xa9n\xc3\xa9vols, salari\xc3\xa9s', null=True, blank=True),
        ),
    ]
