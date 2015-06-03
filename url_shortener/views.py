from django.core.cache import cache
from django.shortcuts import redirect as django_redirect
from django.shortcuts import render

from url_shortener.forms import ShortenURLForm
from url_shortener.models import ShortenedURL
from url_shortener.shortener import string_shortener


def index(request):
    context = {}

    if request.method == 'POST':
        form = ShortenURLForm(request.POST)

        if form.is_valid():
            context['host'] = request.get_host()

            url = form.cleaned_data['url']
            cached_url = cache.get(url)
            if cached_url:
                context['shortened_url'] = cached_url
            else:
                shortened_url = string_shortener(url)
                ShortenedURL.objects.get_or_create(url=url, shortened_url=shortened_url)
                context['shortened_url'] = shortened_url
                cache.set(url, shortened_url)
    else:
        form = ShortenURLForm()

    context['form'] = form

    return render(request, 'url_shortener/index.html', context)


def redirect(request, hash_shortened_url):
    shortened_url = ShortenedURL.objects.get(shortened_url=hash_shortened_url)

    original_url = shortened_url.url

    return django_redirect(original_url)
