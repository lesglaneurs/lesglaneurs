# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0009_role_user_userprojectrole'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Person',
        ),
        migrations.RenameModel(
            old_name='UserProjectRole',
            new_name='PersonProjectRole',
        ),
        migrations.RenameField(
            model_name='personprojectrole',
            old_name='user',
            new_name='person',
        ),
    ]
