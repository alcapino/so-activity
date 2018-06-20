from django.db import models

# Create your models here.
def generateToken():
    import random
    return ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(30))

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=100,)
    password = models.CharField(max_length=100,)
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')
    active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=30, default=generateToken)

    class Meta:
        ordering = ('created',)