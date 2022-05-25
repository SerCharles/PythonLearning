from django.db import models
  
# Create your models here.
class user_info(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class history_record(models.Model):
    name = models.CharField(max_length = 64)
    time = models.IntegerField(max_length = 64)
    content = models.CharField(max_length = 2000)

class user_and_history(models.Model):
    username = models.CharField(max_length = 32)
    history_name = models.CharField(max_length = 64)