# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-19 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvbapp', '0010_auto_20170718_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledmeeting',
            name='phase',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
