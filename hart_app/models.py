from django.db import models

# Create your models here.

class chat_sms(models.Model):
    name = models.CharField(max_length=200)
    sms_text = models.CharField(max_length=2000)
    date = models.DateTimeField()


