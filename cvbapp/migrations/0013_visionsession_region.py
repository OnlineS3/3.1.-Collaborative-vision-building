# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-17 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvbapp', '0012_visionreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='visionsession',
            name='region',
            field=models.CharField(default='UK', max_length=128),
            preserve_default=False,
        ),
    ]
