from django.db import models
class User(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    role = models.CharField(max_length=10)
    attendance = models.CharField(max_length=10)