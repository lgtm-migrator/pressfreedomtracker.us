# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-11 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('common', '0003_organizationindexpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full', label='Rich Text')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock())))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
