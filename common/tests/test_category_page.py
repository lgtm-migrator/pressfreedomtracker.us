from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import TestCase, RequestFactory
from wagtail.core.models import Site, Page
from wagtail.tests.utils import WagtailPageTests
from wagtail.tests.utils.form_data import (
    inline_formset,
    nested_form_data,
    rich_text,
)

from common.models.pages import CategoryIncidentFilter, CategoryPage
from common.models.settings import IncidentFilterSettings, GeneralIncidentFilter
from common.tests.factories import CategoryPageFactory
from common.models.choices import FILTER_CHOICES
from home.tests.factories import HomePageFactory
from incident.utils.incident_filter import IncidentFilter
from incident.tests.factories import IncidentPageFactory


class ContextTest(TestCase):
    def test_incidents_filtered_by_category(self):
        category1 = CategoryPageFactory()
        category2 = CategoryPageFactory()
        incident1 = IncidentPageFactory(categories=[category1])
        IncidentPageFactory(title='Not relevant', categories=[category2])

        request = RequestFactory().get('/')

        context = category1.get_context(request)

        self.assertEqual(set(context['entries_page']), {incident1})

    def test_unpaginated_recent_incidents(self):
        category1 = CategoryPageFactory()
        category2 = CategoryPageFactory()
        incident3 = IncidentPageFactory(categories=[category1], date='2022-01-01')
        incident1 = IncidentPageFactory(categories=[category1], date='2022-03-01')
        incident2 = IncidentPageFactory(categories=[category1], date='2022-02-01')
        IncidentPageFactory(title='Not relevant', categories=[category2])

        request = RequestFactory().get('/')

        context = category1.get_context(request)

        self.assertEqual(list(context['recent_incidents']), [incident1, incident2, incident3])

    def test_incidents_filtered_by_category__and_choice(self):
        category1 = CategoryPageFactory(incident_filters=['arrest_status'])
        category2 = CategoryPageFactory()
        incident1 = IncidentPageFactory(categories=[category1], arrest_status='DETAINED_NO_PROCESSING')
        IncidentPageFactory(title='Not choice', categories=[category1], arrest_status='UNKNOWN')
        IncidentPageFactory(title='Not category', categories=[category2])

        request = RequestFactory().get('/', {'arrest_status': 'DETAINED_NO_PROCESSING'})

        context = category1.get_context(request)

        self.assertEqual(set(context['entries_page']), {incident1})

    def test_filtered__has_filter(self):
        """
        CategoryPage context method should correctly detect if any filters
        are present
        """
        category_page = CategoryPageFactory()
        request = RequestFactory().get(
            '/',
            {'arrest_status': 'DETAINED_NO_PROCESSING'}
        )
        context = category_page.get_context(request)
        self.assertTrue(context['filtered'])

    def test_filtered__no_filter(self):
        """
        CategoryPage context method should correctly detect if no filters
        are present
        """
        category_page = CategoryPageFactory()
        request = RequestFactory().get('/')
        context = category_page.get_context(request)
        self.assertFalse(context['filtered'])

    def test_filtered__ignore_page(self):
        """
        CategoryPage context method should not count `page` in `request.GET` as
        a filter, since it is just a pagination implementation detail
        """
        category_page = CategoryPageFactory()
        request = RequestFactory().get('/', {'page': '2'})
        context = category_page.get_context(request)
        self.assertFalse(context['filtered'])

    def test_filtered__ignore_categories(self):
        """
        CategoryPage context method should not count `category` in
        `request.GET` as a filter since the page is limited by category
        already and the `category` querystring entry is redundant
        """
        category_page = CategoryPageFactory()
        request = RequestFactory().get('/', {'categories': '1'})
        context = category_page.get_context(request)
        self.assertFalse(context['filtered'])


class IncidentFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GeneralIncidentFilter.objects.all().delete()
        CategoryIncidentFilter.objects.all().delete()

    def setUp(self):
        self.category = CategoryPageFactory()
        self.site = Site.objects.get(is_default_site=True)
        self.settings = IncidentFilterSettings.for_site(self.site)

    def test_filters_match_dynamically_generated_incident_filters(self):
        # Incident Filter choices are hard-coded to avoid circular
        # import problems, but ought to match what the
        # `IncidentFilter` class itself considers to be the list of
        # possible filter choices.
        self.assertEqual(
            FILTER_CHOICES,
            list(IncidentFilter.get_filter_choices()),
        )

    def test_valid_incident_filter(self):
        """
        Category incident filters should be fine to create if they don't conflict
        with general incident filters.
        """
        GeneralIncidentFilter.objects.create(
            incident_filter_settings=self.settings,
            incident_filter='state',
        )
        incident_filter = CategoryIncidentFilter(
            category=self.category,
            incident_filter='arrest_status',
        )
        incident_filter.clean()

    def test_incident_filter_unique_with_settings(self):
        """
        Incident filters should not be useable in categories if they're already
        being used in general incident filter settings. Attempting to do so should
        raise a validation error.
        """
        GeneralIncidentFilter.objects.create(
            incident_filter_settings=self.settings,
            incident_filter='arrest_status',
        )

        incident_filter = CategoryIncidentFilter(
            category=self.category,
            incident_filter='arrest_status',
        )

        with self.assertRaises(ValidationError):
            incident_filter.clean()


class CategoryPageTest(TestCase):
    def setUp(self):
        Page.objects.filter(slug='home').delete()
        root_page = Page.objects.get(title='Root')
        self.home_page = HomePageFactory.build(parent=None, slug='home')
        root_page.add_child(instance=self.home_page)

        site, created = Site.objects.get_or_create(
            is_default_site=True,
            defaults={
                'site_name': 'Test site',
                'hostname': 'testserver',
                'port': '1111',
                'root_page': self.home_page,
            }
        )
        if not created:
            site.root_page = self.home_page
            site.save()

        self.category_page = CategoryPageFactory(
            parent=self.home_page,
            incident_filters=['arrest_status'],
        )

    def test_get_page_should_succeed(self):
        response = self.client.get(self.category_page.url)
        self.assertEqual(response.status_code, 200)

    def test_view_draft_should_succeed(self):
        self.category_page.save_revision().publish()
        self.category_page.title = 'XYZ'
        self.category_page.save_revision()

        user = User.objects.create_superuser(username='test', password='test', email='test@test.com')
        self.client.force_login(user)
        draft_url = reverse('wagtailadmin_pages:view_draft', args=(self.category_page.pk,))
        response = self.client.get(draft_url)
        self.assertEqual(response.status_code, 200)

    def test_preview_page_should_succeed(self):
        self.category_page.save_revision().publish()
        self.category_page.title = 'XYZ'
        self.category_page.save_revision()

        user = User.objects.create_superuser(username='test', password='test', email='test@test.com')
        self.client.force_login(user)
        preview_url = reverse('wagtailadmin_pages:preview_on_edit', args=(self.category_page.pk,))

        post_data = {
            'slug': self.category_page.slug,
            'title': 'ABC',
            'methodology': '{}',
            'quick_facts-TOTAL_FORMS': 0,
            'quick_facts-INITIAL_FORMS': 0,
            'quick_facts-MIN_NUM_FORMS': 0,
            'quick_facts-MAX_NUM_FORMS': 1000,
            'statistics_items-TOTAL_FORMS': 0,
            'statistics_items-INITIAL_FORMS': 0,
            'statistics_items-MIN_NUM_FORMS': 0,
            'statistics_items-MAX_NUM_FORMS': 1000,
            'featured_incidents-TOTAL_FORMS': 0,
            'featured_incidents-INITIAL_FORMS': 0,
            'featured_incidents-MIN_NUM_FORMS': 0,
            'featured_incidents-MAX_NUM_FORMS': 1000,
            'featured_blogs-TOTAL_FORMS': 0,
            'featured_blogs-INITIAL_FORMS': 0,
            'featured_blogs-MIN_NUM_FORMS': 0,
            'featured_blogs-MAX_NUM_FORMS': 1000,
            'methodology_items-TOTAL_FORMS': 0,
            'methodology_items-INITIAL_FORMS': 0,
            'methodology_items-MIN_NUM_FORMS': 0,
            'methodology_items-MAX_NUM_FORMS': 1000,
            'incident_filters-TOTAL_FORMS': 0,
            'incident_filters-INITIAL_FORMS': 0,
            'incident_filters-MIN_NUM_FORMS': 0,
            'incident_filters-MAX_NUM_FORMS': 1000,
            'incident_filters-0-incident_filter': 'arrest_status',
            'incident_filters-0-id': 1,
            'incident_filters-0-ORDER': 1,
            'page_symbol': 'arrest',
            'viz_type': 'none'
        }

        response = self.client.post(
            preview_url,
            post_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {'is_valid': True})

        response = self.client.get(preview_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], self.category_page)


class CategoryPageMethodologyStatisticsTest(WagtailPageTests):
    @classmethod
    def setUpTestData(cls):
        Page.objects.filter(slug='home').delete()
        root_page = Page.objects.get(title='Root')
        cls.home_page = HomePageFactory.build(parent=None, slug='home')
        root_page.add_child(instance=cls.home_page)

        site, created = Site.objects.get_or_create(
            is_default_site=True,
            defaults={
                'site_name': 'Test site',
                'hostname': 'testserver',
                'port': '1111',
                'root_page': cls.home_page,
            }
        )
        if not created:
            site.root_page = cls.home_page
            site.save()
        CategoryPageFactory(
            parent=cls.home_page,
            # Needed to apply an "city" filter below
            incident_filters=['city'],
        )
        stats_tag = '{% num_incidents city="Albuquerque" %}'
        cls.page_data = {
            'title': 'Test Category',
            'slug': 'test-category',
            'methodology': rich_text('<p>Lorem {} dolor sit amet</p>'.format(stats_tag)),
            'page_symbol': 'arrest',
            'viz_type': 'none',
            'quick_facts': inline_formset([]),
            'statistics_items': inline_formset([]),
            'featured_incidents': inline_formset([]),
            'featured_blogs': inline_formset([]),
            'methodology_items': inline_formset([]),
            'incident_filters': inline_formset([]),
        }

    def test_can_create_category_page(self):
        self.assertCanCreate(
            self.home_page,
            CategoryPage,
            nested_form_data(self.page_data),
        )
        category = CategoryPage.objects.get(slug='test-category')
        response = self.client.get(category.url)
        self.assertEqual(response.status_code, 200)

    def test_can_preview_category_page(self):
        category = CategoryPageFactory(parent=self.home_page)
        preview_url = reverse('wagtailadmin_pages:preview_on_edit', args=(category.pk,))
        response = self.client.post(
            preview_url,
            nested_form_data(self.page_data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {'is_valid': True})

        response = self.client.get(preview_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], category)
