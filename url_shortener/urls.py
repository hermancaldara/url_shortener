from django.conf.urls import patterns, url

from url_shortener.views import index, redirect

urlpatterns = patterns(
    '',
    url(r'^$', index),
    url(r'^(?P<hash_shortened_url>[a-zA-Z0-9]{7})', redirect),
)
