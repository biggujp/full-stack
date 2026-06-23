from django.db import models

# Create your models here.
class Member(models.Model):
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    point = models.IntegerField(default=1)
    join_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "User: {} // Name: {} // Point: {}".format(self.username, self.fullname,self.point)
