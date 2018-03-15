# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-05 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cvbapp', '0013_visionsession_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_with', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='visionsession',
            name='share_id',
            field=models.CharField(default='test', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shares',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cvbapp.VisionSession'),
        ),
    ]
