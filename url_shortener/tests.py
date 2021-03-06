from django import forms
from django.core.urlresolvers import resolve
from django.db import models
from django.test import TestCase, Client

from url_shortener.forms import ShortenURLForm
from url_shortener.models import ShortenedURL
from url_shortener.shortener import string_shortener


class TestUrl(TestCase):

    def test_index_url_is_mapped(self):
        match = resolve('/')

        self.assertEqual(match.view_name, 'url_shortener.views.index')

    def test_redirect_url_is_mapped(self):
        match = resolve('/abcdefg')

        self.assertEqual(match.view_name, 'url_shortener.views.redirect')


class TestIndexView(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.response = cls.client.get('/')
        cls.response_post = cls.client.post('/', {'url': 'http://www.google.com'})

    @classmethod
    def tearDownClass(cls):
        ShortenedURL.objects.all().delete()

    def test_index_view_works(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_view_renders_a_template(self):
        self.assertTemplateUsed(self.response, 'url_shortener/index.html')

    def test_index_view_has_form_on_context(self):
        self.assertIsInstance(self.response.context['form'], ShortenURLForm)

    def test_index_view_has_the_shortened_url_on_context_when_form_is_filled_correctly(self):
        self.assertNotEqual(self.response_post.context['shortened_url'], '')

    def test_index_view_create_a_registry_with_url_and_his_shortened_form(self):
        self.assertGreater(len(ShortenedURL.objects.all()), 0)

    def test_index_view_does_not_duplicate_a_registry_for_the_same_url(self):
        self.client.post('/', {'url': 'http://www.google.com'})

        self.assertEqual(len(ShortenedURL.objects.all()), 1)


class TestRedirectView(TestCase):

    @classmethod
    def setUpClass(cls):
        ShortenedURL(
            url="http://www.google.com",
            shortened_url="abcdefg",
        ).save()

    @classmethod
    def tearDownClass(cls):
        ShortenedURL.objects.all().delete()

    def test_redirect_the_shortened_url_to_the_original_url(self):
        client = Client()
        response = client.get('/abcdefg')

        self.assertRedirects(response, 'http://www.google.com')


class TestForm(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.form = ShortenURLForm()

    def test_form_has_a_field_for_an_url(self):
        self.assertEqual(self.form.base_fields.get('url').label, 'URL')

    def test_field_for_url(self):
        self.assertIsInstance(self.form.base_fields.get('url'), forms.URLField)


class TestURLShortner(TestCase):

    def test_shorten_a_string(self):
        self.assertEqual(string_shortener('Herman'), '8d57a8f')


class TestModelShortenedURL(TestCase):

    def test_has_a_field_for_url(self):
        self.assertIsInstance(ShortenedURL._meta.get_field('url'), models.URLField)

    def test_has_a_field_for_shortened_url(self):
        self.assertIsInstance(ShortenedURL._meta.get_field('shortened_url'), models.URLField)
