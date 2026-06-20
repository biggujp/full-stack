from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=100)
    homenum = models.CharField(max_length=6)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    point = models.IntegerField(default=1)
    address = models.TextField(null=True, blank=True)

