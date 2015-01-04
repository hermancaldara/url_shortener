from django.core.urlresolvers import resolve
from django import forms
from django.test import TestCase, Client

from url_shortener.forms import ShortenURLForm
from url_shortener.shortener import Shortener


class TestUrl(TestCase):

    def test_index_url_is_mapped(self):
        match = resolve('/')

        self.assertEqual(match.view_name, 'url_shortener.views.index')


class TestView(TestCase):

    @classmethod
    def setUpClass(cls):
        client = Client()
        cls.response = client.get('/')

    def test_index_view_works(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_view_renders_a_template(self):
        self.assertTemplateUsed(self.response, 'url_shortener/index.html')

    def test_index_view_has_form_on_context(self):
        self.assertIsInstance(self.response.context['form'], ShortenURLForm)


class TestForm(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.form = ShortenURLForm()

    def test_form_has_a_field_for_an_url(self):
        self.assertEqual(self.form.base_fields.get('url').label, 'URL')

    def test_field_for_url(self):
        self.assertIsInstance(self.form.base_fields.get('url'), forms.URLField)
