import factory
import wagtail_factories
from wagtail.core import blocks
from wagtail.core.rich_text import RichText

from common.blocks import (
    Heading1,
    Heading2,
    Heading3,
    StyledTextBlock,
)
from common.choices import CATEGORY_SYMBOL_CHOICES
from common.models import (
    CategoryPage,
    CategoryIncidentFilter,
    CommonTag,
    CustomImage,
    SimplePage,
    PersonPage,
    OrganizationPage,
    OrganizationIndexPage,
    SiteSettings,
    TaxonomyCategoryPage,
    TaxonomySettings,
)
from common.tests.utils import StreamfieldProvider, make_html_string


factory.Faker.add_provider(StreamfieldProvider)


class DevelopmentSiteFactory(wagtail_factories.SiteFactory):
    class Meta:
        django_get_or_create = ('is_default_site',)
    site_name = 'Press Freedom Tracker (Dev)'
    port = 8000
    is_default_site = True
    root_page = None


class SiteSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SiteSettings
        django_get_or_create = ('site',)

    site = factory.SubFactory(DevelopmentSiteFactory)
    incident_sidebar_note = factory.Faker('streamfield', fields=[
        'heading',
        'rich_text_line',
    ])
    homepage_only = True
    banner_content = None


class CategoryIncidentFilterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryIncidentFilter

    sort_order = factory.Sequence(lambda n: n)


class TaxonomySettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaxonomySettings
        django_get_or_create = ('site',)

    site = factory.SubFactory(DevelopmentSiteFactory)


class TaxonomyCategoryPageFactory(factory.django.DjangoModelFactory):
    taxonomy_setting = factory.SubFactory(TaxonomySettingsFactory)
    sort_order = factory.Sequence(lambda n: n)

    class Meta:
        model = TaxonomyCategoryPage


class CategoryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = CategoryPage
        exclude = ('methodology_text', )

    class Params:
        arrest = factory.Trait(
            title='Arrest / Criminal Charge',
            plural_name='Arrests and Criminal Charges',
            slug='arrest-criminal-charge',
            page_symbol='arrest',
        )
        border_stop = factory.Trait(
            title='Border Stop',
            plural_name='Border Stops',
            slug='border-stop',
            page_symbol='border_stop',
        )
        denial_of_access = factory.Trait(
            title='Denial of Access',
            plural_name='Denials of Access',
            slug='denial-access',
            page_symbol='denial_of_access',
        )
        equipment_search = factory.Trait(
            title='Equipment Search or Seizure',
            plural_name='Equipment Searches, Seizures and Damage',
            slug='equipment-search-seizure-or-damage',
            page_symbol='equipment_search',
        )
        assault = factory.Trait(
            title='Assault',
            plural_name='Assaults',
            slug='assault',
            page_symbol='assault',
        )
        leak_case = factory.Trait(
            title='Leak Case',
            plural_name='Leak Cases',
            slug='leak-case',
            page_symbol='leak_case',
        )
        subpoena = factory.Trait(
            title='Subpoena / Legal Order',
            plural_name='Subpoenas and Legal Orders',
            slug='subpoena',
            page_symbol='subpoena',
        )
        equipment_damage = factory.Trait(
            title='Equipment Damage',
            plural_name='Equipment Damages',
            slug='equipment-damage',
            page_symbol='equipment_damage',
        )
        other_incident = factory.Trait(
            title='Other Incident',
            plural_name='Other Incidents',
            slug='other-incident',
            page_symbol='other_incident',
        )
        chilling_statement = factory.Trait(
            title='Chilling Statement',
            plural_name='Chilling Statements',
            slug='chilling-statement',
            page_symbol='chilling_statement',
        )
        prior_restraint = factory.Trait(
            title='Prior Restraint',
            plural_name='Prior Restraints',
            slug='prior-restraint',
            page_symbol='prior_restraint',
        )

    methodology_text = factory.Faker('paragraph', nb_sentences=5)

    title = factory.Sequence(lambda n: 'Category {n}'.format(n=n))
    description = factory.LazyAttribute(lambda _: make_html_string())
    methodology = factory.LazyAttribute(lambda o: RichText(o.methodology_text))
    taxonomy = factory.RelatedFactory(TaxonomyCategoryPageFactory, 'category')
    page_symbol = factory.Iterator(CATEGORY_SYMBOL_CHOICES, getter=lambda c: c[0])

    @factory.post_generation
    def incident_filters(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            CategoryIncidentFilter.objects.bulk_create([
                CategoryIncidentFilter(
                    category=self,
                    incident_filter=incident_filter,
                )
                for incident_filter in extracted
            ])


class CustomImageFactory(wagtail_factories.ImageFactory):
    attribution = factory.Faker('name')

    class Meta:
        model = CustomImage


class PersonPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = PersonPage
        exclude = ('bio_text', )

    bio_text = factory.Faker('paragraph')

    title = factory.Faker('name')
    bio = factory.LazyAttribute(lambda o: RichText(o.bio_text))
    website = factory.Faker('uri')
    photo = None


class OrganizationIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = OrganizationIndexPage

    title = 'All Organizations'


class OrganizationPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = OrganizationPage

    title = factory.Faker('company')
    slug = factory.Sequence(lambda n: 'organization-{n}'.format(n=n))
    website = factory.Faker('uri')
    description = factory.Faker('catch_phrase')


class SimplePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = SimplePage

    body = factory.Faker('streamfield', fields=[
        'styled_text_paragraphs',
        'styled_text',
        'info_table_pages',
        'info_table_emails',
        'info_table_external_links',
        'info_table_plain_text',
        'raw_html',
    ])


class RichTextBlockFactory(wagtail_factories.blocks.BlockFactory):
    class Meta:
        model = blocks.RichTextBlock


class RawHTMLBlockFactory(wagtail_factories.blocks.BlockFactory):
    class Meta:
        model = blocks.RawHTMLBlock


class ChoiceBlockFactory(wagtail_factories.blocks.BlockFactory):
    class Meta:
        model = blocks.ChoiceBlock


class Heading1Factory(wagtail_factories.StructBlockFactory):
    content = wagtail_factories.CharBlockFactory

    class Meta:
        model = Heading1


class Heading2Factory(wagtail_factories.StructBlockFactory):
    content = wagtail_factories.CharBlockFactory

    class Meta:
        model = Heading2


class Heading3Factory(wagtail_factories.StructBlockFactory):
    content = wagtail_factories.CharBlockFactory

    class Meta:
        model = Heading3


class StyledTextBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = StyledTextBlock

    text = RichTextBlockFactory
    background_color = ChoiceBlockFactory
    text_align = ChoiceBlockFactory
    font_size = ChoiceBlockFactory
    font_family = ChoiceBlockFactory


class CommonTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommonTag
        django_get_or_create = ('title',)

    title = factory.Faker('word')
