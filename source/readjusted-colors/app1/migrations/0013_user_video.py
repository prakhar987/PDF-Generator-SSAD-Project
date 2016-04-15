# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20151121_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='video',
            field=models.FileField(null=True, upload_to=b'app1/static/app1/video/'),
        ),
    ]
