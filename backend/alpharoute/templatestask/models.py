from django.db import models


class Template(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link_url = models.CharField(max_length=255)
