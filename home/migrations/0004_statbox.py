# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
        ('home', '0003_auto_20170517_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('value', models.CharField(max_length=1000)),
                ('label', models.CharField(max_length=1000)),
                ('color', models.CharField(choices=[('#119abc', 'Blue'), ('#5b9932', 'Green'), ('#803e79', 'Purple'), ('#dc810b', 'Orange')], max_length=7)),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='statboxes', to='home.HomePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
