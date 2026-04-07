from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)    
    email = models.EmailField()
    point = models.IntegerField(default=1)
    address = models.CharField(max_length=200, null=True, blank=True)   

    def __str__(self):
        #return self.name + ' คะแนน: ' + str(self.point) + 'points'  
        return 'ชื่อ: {} คะแนน: {} points'.format(self.name, self.point)

