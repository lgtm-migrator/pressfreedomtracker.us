# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 07:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailcore', '0039_collectionviewrestriction'),
        ('common', '0024_personpage_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialSharingSEOSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_description', models.TextField(blank=True, help_text="Default text description for pages that don't have another logical field for text descirptions", null=True)),
                ('facebook_page_id', models.CharField(blank=True, help_text='Find on your Facebook page by navigating to "About" and scrolling to the bottom', max_length=255, null=True)),
                ('default_image', models.ForeignKey(blank=True, help_text="Default image for pages that don't have another logical image for social sharing", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Social Sharing/SEO',
            },
        ),
    ]
