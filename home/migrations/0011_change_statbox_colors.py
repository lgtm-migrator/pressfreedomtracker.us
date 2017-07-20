# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 15:11
from __future__ import unicode_literals

from django.db import migrations


OLD_TO_NEW = {
    'blue': 'eastern-blue',
    'purple': 'violet',
    'dark-gray': 'dark-gray',
    'orange': 'gamboge',
    'white': 'white',
}


NEW_TO_OLD = {
    'eastern-blue': 'blue',
    'gamboge': 'orange',
    'green-apple': 'dark-gray',
    'green': 'dark-gray',
    'sunshine': 'dark-gray',
    'pink': 'purple',
    'red': 'dark-gray',
    'royal-blue': 'dark-gray',
    'teal': 'eastern-blue',
    'violet': 'purple',
    'yellow': 'dark-gray',
}


def update_statbox_colors(apps, schema_editor):
    StatBox = apps.get_model('home', 'StatBox')
    stat_boxes = StatBox.objects.all()
    for box in stat_boxes:
        box.color = OLD_TO_NEW[box.color]
        box.save()


def undo_update_statbox_colors(apps, schema_editor):
    StatBox = apps.get_model('home', 'StatBox')
    stat_boxes = StatBox.objects.all()
    for box in stat_boxes:
        box.color = NEW_TO_OLD[box.color]
        box.save()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20170719_2347'),
    ]

    operations = [
        migrations.RunPython(update_statbox_colors, undo_update_statbox_colors)
    ]
