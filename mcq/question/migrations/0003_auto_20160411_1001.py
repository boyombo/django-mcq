# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20160409_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='label',
            field=models.CharField(max_length=50),
        ),
    ]
