from django.test import TestCase
from django.urls import reverse

from rango import views, Fake
from rango.models import Category

from unittest.mock import MagicMock, Mock


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        category = Category(name='test', views=-1, likes=0)
        category.save()
        self.assertEqual((category.views >= 0), True)

    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        Example: "Random Category String" should be "random-category-string".
        """

        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        views.useFake = True
        Fake.add_category('Python', 1, 1)
        Fake.add_category('C++', 1, 1)
        Fake.add_category('Erlang', 1, 1)

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "C++")
        self.assertContains(response, "Erlang")
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)
        Fake.delete()
        views.useFake = False

class AboutViewTests(TestCase):
    def test_visit_count_displays(self):
        views.useStub = True

        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visits: 2")

        views.useStub = False


    def test_visit_count_increments(self):
        temp = views.get_server_side_cookie
        views.get_server_side_cookie = MagicMock(side_effect=["4", "2020-01-01 12:00:00.759963"])

        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visits: 5")

        views.get_server_side_cookie = temp