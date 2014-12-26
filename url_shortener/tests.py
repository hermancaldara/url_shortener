from django.core.urlresolvers import resolve
from django.test import TestCase, Client


class TestUrl(TestCase):

    def test_index_url_is_mapped(self):
        match = resolve('/')

        self.assertEqual(match.view_name, 'url_shortener.views.index')


class TestView(TestCase):

    def test_index_view_works(self):
        client = Client()
        response = client.get('/')

        self.assertEqual(response.status_code, 200)
