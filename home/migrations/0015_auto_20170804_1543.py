# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_homepage_search_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statbox',
            old_name='link',
            new_name='internal_link',
        ),
    ]
