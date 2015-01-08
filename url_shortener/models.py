from django.db import models


class ShortenedURL(models.Model):
    url = models.URLField()
    shortened_url = models.URLField()
