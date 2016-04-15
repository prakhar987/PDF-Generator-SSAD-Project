# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20151110_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFiles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('media_file', models.ImageField(upload_to=b'app1/static/app1/images/media_files/')),
                ('question_id', models.ForeignKey(to='app1.Question')),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to=b'app1/static/app1/images/company/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(upload_to=b'app1/static/app1/images/user/'),
        ),
        migrations.AddField(
            model_name='mediafiles',
            name='user_id',
            field=models.ForeignKey(to='app1.User'),
        ),
    ]
