from django.shortcuts import render

from url_shortener.forms import ShortenURLForm


def index(request):
    form = ShortenURLForm()

    return render(request, 'url_shortener/index.html', {'form': form})
