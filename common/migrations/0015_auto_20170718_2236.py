# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 22:36
from __future__ import unicode_literals

import common.blocks
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_fix_custom_image_sequence_but_actually'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('text', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('background_color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('dark-gray', 'Dark Gray'), ('white', 'White')])), ('text_align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('font_size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('small', 'Small'), ('normal', 'Normal'), ('large', 'Large'), ('jumbo', 'Jumbo')])), ('font_family', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('sans-serif', 'Sans Serif'), ('serif', 'Serif')]))), label='Text', template='common/blocks/styled_text_full_bleed.html')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('logo_list', common.blocks.LogoListBlock()), ('video', wagtail.wagtailcore.blocks.StructBlock((('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('attribution', wagtail.wagtailcore.blocks.CharBlock(max_length=255, required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('heading_1', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_2', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_3', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))))),
        ),
        migrations.AlterField(
            model_name='simplepagewithsidebar',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('text', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('background_color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('dark-gray', 'Dark Gray'), ('white', 'White')])), ('text_align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('font_size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('small', 'Small'), ('normal', 'Normal'), ('large', 'Large'), ('jumbo', 'Jumbo')])), ('font_family', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('sans-serif', 'Sans Serif'), ('serif', 'Serif')]))), label='Text')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('logo_list', common.blocks.LogoListBlock()), ('video', wagtail.wagtailcore.blocks.StructBlock((('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('attribution', wagtail.wagtailcore.blocks.CharBlock(max_length=255, required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('heading_1', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_2', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_3', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))))),
        ),
    ]
