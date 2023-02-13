from django.db import models
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
