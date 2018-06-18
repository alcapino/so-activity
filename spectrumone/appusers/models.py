from django.db import models

# Create your models here.

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=100,)
    password = models.CharField(max_length=100,)
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')
    activated = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)