# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-11 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvbapp', '0003_visionstatement'),
    ]

    operations = [
        migrations.AddField(
            model_name='visionstatement',
            name='phase',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
