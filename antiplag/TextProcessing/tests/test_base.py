"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase
from django.conf import settings


# settings.configure()
# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_home(self):
    #     """Tests the home page."""
    #     response = self.client.get('/')
    #     self.assertContains(response, 'Home Page', 1, 200)
    #
    # def test_contact(self):
    #     """Tests the contact page."""
    #     response = self.client.get('/contact')
    #     self.assertContains(response, 'Contact', 3, 200)
    #
    # def test_about(self):
    #     """Tests the about page."""
    #     response = self.client.get('/about')
    #     self.assertContains(response, 'About', 3, 200)
