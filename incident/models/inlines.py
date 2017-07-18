from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailimages.blocks import ImageChooserBlock

from autocomplete.edit_handlers import AutocompletePageChooserPanel
from statistics.blocks import StatisticsBlock


class IncidentPageUpdates(Orderable):
    page = ParentalKey('incident.IncidentPage', related_name='updates')
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = StreamField([
        ('rich_text', blocks.RichTextBlock(icon='doc-full', label='Rich Text')),
        ('image', ImageChooserBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
        ('statistics', StatisticsBlock()),
    ])

    panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]


class IncidentCategorization(Orderable):
    incident_page = ParentalKey('incident.IncidentPage', related_name='categories')
    category = ParentalKey('common.CategoryPage', related_name='incidents')

    @property
    def summary(self):
        return self.category.title


class IncidentPageLinks(Orderable):
    page = ParentalKey('incident.IncidentPage', related_name='links')
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(null=False, blank=False)


class EquipmentSeized(models.Model):
    incident = ParentalKey(
        'incident.IncidentPage',
        related_name='equipment_seized',
    )
    equipment = ParentalKey(
        'incident.Equipment',
        verbose_name='Equipment Seized',
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    panels = [
        AutocompletePageChooserPanel('equipment', page_type='incident.Equipment'),
        FieldPanel('quantity'),
    ]

    @property
    def summary(self):
        return '{0.equipment}: count of {0.quantity}'


class EquipmentBroken(models.Model):
    incident = ParentalKey(
        'incident.IncidentPage',
        related_name='equipment_broken',
    )
    equipment = ParentalKey(
        'incident.Equipment',
        verbose_name='Equipment Broken',
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    panels = [
        AutocompletePageChooserPanel('equipment', page_type='incident.Equipment'),
        FieldPanel('quantity'),
    ]

    @property
    def summary(self):
        return '{0.equipment}: count of {0.quantity}'
