from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

from common.edit_handlers import HelpPanel


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    button_text = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    content_panels = [
        HelpPanel('Forms can be embedded in an iframe by a third-party website. '
                  'Append <code>?embed=t</code> to any FormPage URL to request the embeddable version. '
                  'That query string should be included in the <code>src</code> attribute of your iframe.'
        ),
    ] + AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel('button_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_context(self, request):
        context = super(FormPage, self).get_context(request)
        if request.GET.get('embed', None):
            context['template_name'] = 'base.chromeless.html'
        else:
            context['template_name'] = 'base.html'
        return context

    def serve(self, request, *args, **kwargs):
        response = super(FormPage, self).serve(request, *args, **kwargs)
        if 'embed' in request.GET:
            response.xframe_options_exempt = True
        return response
