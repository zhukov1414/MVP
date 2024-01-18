from django.db import models


class Template(models.Model):
    # id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link_url = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['id']

    def __str__(self):
        return self.title
