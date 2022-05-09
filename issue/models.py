from django.db import models

# Create your models here.

class Issue(models.Model):
    keyword = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    context = models.TextField()

    link1 = models.URLField(blank=True)
    link2 = models.URLField(blank=True)
    link3 = models.URLField(blank=True)

    def __str__(self):
        return self.keyword

