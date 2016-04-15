# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20151115_0902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediafiles',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='mediafiles',
            old_name='user_id',
            new_name='user',
        ),
    ]
