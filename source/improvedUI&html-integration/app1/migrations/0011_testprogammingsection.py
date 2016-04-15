# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20151115_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestProgammingSection',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('code', models.FileField(upload_to=b'app1/static/app1/code_samples/')),
                ('question', models.ForeignKey(to='app1.Question')),
                ('user', models.ForeignKey(to='app1.User')),
            ],
        ),
    ]
