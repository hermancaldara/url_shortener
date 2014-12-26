from django.conf.urls import patterns, url

from url_shortener.views import index

urlpatterns = patterns(
    '',
    url(r'^$', index),
)
