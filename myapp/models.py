from django.db import models

# Create your models here.
class people(models.Model):
    name=models.CharField(max_length=25)
    email=models.CharField(max_length=25)
    phone=models.IntegerField()
    gender=models.CharField(max_length=25)
    username=models.CharField(max_length=25)
    password=models.CharField(max_length=25)



class feedback(models.Model):
    name=models.CharField(max_length=25)
    phone=models.IntegerField()
    email=models.CharField(max_length=25)
    message=models.CharField(max_length=50)