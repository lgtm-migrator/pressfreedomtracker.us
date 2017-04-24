# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-24 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0009_incidentcategorization'),
        ('home', '0009_auto_20170424_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageIncidents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('incident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='incident.IncidentPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='incidents', to='home.HomePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
