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
    TaxonomyCategoryPage,
    TaxonomySettings,
)


class DevelopmentSiteFactory(wagtail_factories.SiteFactory):
    class Meta:
        django_get_or_create = ('is_default_site',)
    site_name = 'Press Freedom Tracker (Dev)'
    port = 8000
    is_default_site = True
    root_page = None


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

    class Params:
        arrest = factory.Trait(
            title='Arrest / Criminal Charge',
            plural_name='Arrests and Criminal Charges',
            slug='arrest-criminal-charge'
        )
        border_stop = factory.Trait(
            title='Border Stop',
            plural_name='Border Stops',
            slug='border-stop'
        )
        denial_of_access = factory.Trait(
            title='Denial of Access',
            plural_name='Denials of Access',
            slug='denial-access',
        )
        equipment_search = factory.Trait(
            title='Equipment Search or Seizure',
            plural_name='Equipment Searches, Seizures and Damage',
            slug='equipment-search-seizure-or-damage',
        )
        assault = factory.Trait(
            title='Assault',
            plural_name='Assaults',
            slug='assault',
        )
        leak_case = factory.Trait(
            title='Leak Case',
            plural_name='Leak Cases',
            slug='leak-case'
        )
        subpoena = factory.Trait(
            title='Subpoena / Legal Order',
            plural_name='Subpoenas and Legal Orders',
            slug='subpoena'
        )
        equipment_damage = factory.Trait(
            title='Equipment Damage',
            plural_name='Equipment Damages',
            slug='equipment-damage',
        )
        other_incident = factory.Trait(
            title='Other Incident',
            plural_name='Other Incidents',
            slug='other-incident',
        )
        chilling_statement = factory.Trait(
            title='Chilling Statement',
            plural_name='Chilling Statements',
            slug='chilling-statement',
        )
        prior_restraint = factory.Trait(
            title='Prior Restraint',
            plural_name='Prior Restraints',
            slug='prior-restraint',
        )

    title = factory.Sequence(lambda n: 'Category {n}'.format(n=n))
    methodology = RichText("Methodology")
    taxonomy = factory.RelatedFactory(TaxonomyCategoryPageFactory, 'category')
    page_symbol = factory.Iterator(CATEGORY_SYMBOL_CHOICES, getter=lambda c: c[0])
    viz_type = 'none'

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
    attribution = factory.Sequence(lambda n: f'Attribution {n}')

    class Meta:
        model = CustomImage


class PersonPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = PersonPage

    title = factory.Sequence(lambda n: f'Person {n}')
    bio = RichText("Bio")
    website = 'https://freedom.press'
    photo = None


class OrganizationIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = OrganizationIndexPage

    title = 'All Organizations'


class OrganizationPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = OrganizationPage

    title = factory.Sequence(lambda n: f'Organization {n}')
    slug = factory.Sequence(lambda n: 'organization-{n}'.format(n=n))
    website = 'https://freedom.press'
    description = 'Organization Description'


class SimplePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = SimplePage


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

    title = factory.Sequence(lambda n: f'Tag {n}')
