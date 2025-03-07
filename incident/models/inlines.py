from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.images.blocks import ImageChooserBlock

from common.blocks import (
    AlignedCaptionedEmbedBlock,
    TweetEmbedBlock,
    RichTextBlockQuoteBlock,
    RichTextTemplateBlock,
)
from incident.models import choices
from wagtailautocomplete.edit_handlers import AutocompletePanel
from statistics.blocks import StatisticsBlock


class IncidentCharge(ClusterableModel):
    incident_page = ParentalKey('incident.IncidentPage', related_name='charges')
    charge = ParentalKey('incident.Charge', related_name='incidents')
    date = models.DateField()
    status = models.CharField(
        choices=choices.STATUS_OF_CHARGES,
        max_length=1000,
    )
    notes = models.TextField(default='', blank=True)

    panels = [
        AutocompletePanel('charge'),
        FieldPanel('date'),
        FieldPanel('status'),
        FieldPanel('notes'),
        InlinePanel('updates', label='Updates'),
    ]

    def entries_display(self):
        date_format = '%b. %-d, %Y'
        entries = [
            (self.date, self.get_status_display())
        ] + [
            (update.date, update.get_status_display()) for update in self.updates.all()
        ]

        return [
            (date.strftime(date_format), status) for date, status in
            sorted(entries, key=lambda item: item[0])
        ]

    @property
    def summary(self):
        if update := self.updates.order_by('-date').first():
            status = update.get_status_display()
            date = update.date
        else:
            status = self.get_status_display()
            date = self.date

        return f'{self.charge.title} ({status} as of {date})'


class ChargeUpdate(models.Model):
    incident_charge = ParentalKey(
        IncidentCharge,
        related_name='updates',
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    status = models.CharField(
        choices=choices.STATUS_OF_CHARGES,
        max_length=1000,
    )
    notes = models.TextField(default='', blank=True)
    panels = [
        FieldPanel('date'),
        FieldPanel('status'),
        FieldPanel('notes'),
    ]


class IncidentPageUpdates(models.Model):
    page = ParentalKey('incident.IncidentPage', related_name='updates')
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = StreamField([
        ('rich_text', RichTextTemplateBlock(icon='doc-full', label='Rich Text')),
        ('image', ImageChooserBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
        ('tweet', TweetEmbedBlock()),
        ('blockquote', RichTextBlockQuoteBlock()),
        ('video', AlignedCaptionedEmbedBlock()),
        ('statistics', StatisticsBlock()),
    ])

    panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]

    def __str__(self):
        return '({}) {}'.format(self.date, self.title)

    class Meta:
        indexes = [
            models.Index(fields=['page', '-date']),
        ]


class IncidentCategorization(Orderable):
    incident_page = ParentalKey('incident.IncidentPage', related_name='categories')
    category = ParentalKey('common.CategoryPage', related_name='incidents')

    @property
    def summary(self):
        return self.category.title

    def __str__(self):
        return '"{}" in category "{}"'.format(self.incident_page, self.category)


class IncidentPageLinks(Orderable):
    page = ParentalKey('incident.IncidentPage', related_name='links')
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(max_length=1024, blank=False)
    publication = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        value = '{} ({})'.format(self.title, self.url)
        if self.publication:
            value += ' via {}'.format(self.publication)
        return value


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
    _autocomplete_model = 'incident.Equipment'

    panels = [
        AutocompletePanel('equipment', target_model='incident.Equipment'),
        FieldPanel('quantity'),
    ]

    class Meta:
        verbose_name = "Equipment Seized"

    @property
    def summary(self):
        return '{0.equipment}: count of {0.quantity}'.format(self)


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
    _autocomplete_model = 'incident.Equipment'

    panels = [
        AutocompletePanel('equipment', target_model='incident.Equipment'),
        FieldPanel('quantity'),
    ]

    class Meta:
        verbose_name = 'Equipment Broken'

    @property
    def summary(self):
        return '{0.equipment}: count of {0.quantity}'.format(self)
