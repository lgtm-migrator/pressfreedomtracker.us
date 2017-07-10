# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 17:46
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks

from wagtail.wagtailcore.blocks import StreamValue

import json


def richtext_to_styledtext(block):
    return {
        'type': 'text',
        'value': {
            'text': block['value'],
            'font_family': 'sans-serif',
            'background_color': 'white',
            'text_align': 'left',
            'font_size': 'normal',
        }
    }


def get_stream_data(page, mapper):
    stream_data = []
    mapped = False

    print('Looking at page', page.title)
    for block in page.body.stream_data:
        print('Before stream data', json.dumps(page.body.stream_data))
        if block['type'] == 'rich_text':
            import pdb
            pdb.set_trace()
        if block['type'] == 'rich_text' and isinstance(block['value'], str):
            print('IN thE iF')
            styletext_block = mapper(block)
            stream_data.append(styletext_block)
            mapped = True

        else:
            stream_data.append(block)

    return stream_data, mapped


def change_rich_text_to_styled_text(apps, schema_editor):
    SimplePage = apps.get_model('common.SimplePage')
    SimplePageWithSidebar = apps.get_model('common.SimplePageWithSidebar')

    for page in SimplePage.objects.all():
        stream_data, mapped = get_stream_data(page, richtext_to_styledtext)

        if mapped:
            print(page.title, 'got mapped')
            stream_block = page.body.stream_block
            print(json.dumps(stream_data))
            page.body = StreamValue(stream_block, stream_data, is_lazy=True)
            page.save()
            print(page.title, 'saved')
        else:
            print(page.title, 'did not get mapped, skipped')

    # for page in SimplePageWithSidebar.objects.all():
    #     new_blocks = []
    #     for block in page.body.stream_data:
    #         stream_data, mapped = get_stream_data(page, richtext_to_styledtext)

    #         if mapped:
    #             stream_block = page.body.stream_block
    #             page.body = StreamValue(stream_block, stream_data, is_lazy=True)
    #             page.save()

class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_delete_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full', label='Rich Text')), ('text', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('background_color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('dark-gray', 'Dark Gray'), ('white', 'White')])), ('text_align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('font_size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('small', 'Small'), ('normal', 'Normal'), ('large', 'Large'), ('jumbo', 'Jumbo')])), ('font_family', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('sans-serif', 'Sans Serif'), ('serif', 'Serif')]))), label='Text', template='common/blocks/styled_text_full_bleed.html')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('heading_1', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_2', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_3', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))))),
        ),
        migrations.AlterField(
            model_name='simplepagewithsidebar',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full', label='Rich Text')), ('text', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('background_color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('dark-gray', 'Dark Gray'), ('white', 'White')])), ('text_align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('font_size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('small', 'Small'), ('normal', 'Normal'), ('large', 'Large'), ('jumbo', 'Jumbo')])), ('font_family', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('sans-serif', 'Sans Serif'), ('serif', 'Serif')]))), label='Text')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('heading_1', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_2', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_3', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))))),
        ),
        migrations.RunPython(change_rich_text_to_styled_text),
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('text', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('background_color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('dark-gray', 'Dark Gray'), ('white', 'White')])), ('text_align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('font_size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('small', 'Small'), ('normal', 'Normal'), ('large', 'Large'), ('jumbo', 'Jumbo')])), ('font_family', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('sans-serif', 'Sans Serif'), ('serif', 'Serif')]))), label='Text', template='common/blocks/styled_text_full_bleed.html')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('heading_1', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_2', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_3', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))))),
        ),
        migrations.AlterField(
            model_name='simplepagewithsidebar',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('text', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('background_color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('orange', 'Orange'), ('dark-gray', 'Dark Gray'), ('white', 'White')])), ('text_align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')])), ('font_size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('small', 'Small'), ('normal', 'Normal'), ('large', 'Large'), ('jumbo', 'Jumbo')])), ('font_family', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('sans-serif', 'Sans Serif'), ('serif', 'Serif')]))), label='Text')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full-width', 'Full Width')]))))), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock(label='List Item'), template='common/blocks/list_block_columns.html')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('heading_1', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_2', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('heading_3', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))))),
        ),
    ]
