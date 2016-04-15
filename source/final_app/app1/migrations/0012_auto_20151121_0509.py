# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_testprogammingsection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testprogammingsection',
            name='question',
        ),
        migrations.RemoveField(
            model_name='testprogammingsection',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='ide_snapshot',
            field=models.ImageField(null=True, upload_to=b'app1/static/app1/images/ide_snapshots/'),
        ),
        migrations.DeleteModel(
            name='TestProgammingSection',
        ),
    ]
