from django.shortcuts import render

from url_shortener.forms import ShortenURLForm
from url_shortener.models import ShortenedURL
from url_shortener.shortener import string_shortener


def index(request):
    context = {}

    if request.method == 'POST':
        form = ShortenURLForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            shortened_url = string_shortener(url)
            ShortenedURL.objects.get_or_create(url=url, shortened_url=shortened_url)
            context['shortened_url'] = shortened_url
    else:
        form = ShortenURLForm()

    context['form'] = form

    return render(request, 'url_shortener/index.html', context)
