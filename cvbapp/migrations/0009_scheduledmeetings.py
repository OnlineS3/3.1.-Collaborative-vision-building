# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-18 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cvbapp', '0008_remove_visionsession_rc_channel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledMeetings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.CharField(max_length=16)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cvbapp.Channel')),
            ],
        ),
    ]
