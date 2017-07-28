# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 15:42
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0022_add_fields_to_footer'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplepage',
            name='sidebar_content',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('rich_text', wagtail.wagtailcore.blocks.RichTextBlock())), default=None),
        ),
    ]
