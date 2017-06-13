# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-12 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20170609_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='statboxes_label',
            field=models.CharField(blank=True, default='Quick Stats', help_text='Title displayed above stat boxes', max_length=255, null=True),
        ),
    ]
