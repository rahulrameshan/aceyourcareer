from django.db import models

# Create your models here.


class contact_us_model(models.Model):
    entry_num = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=1110)
    contact_email = models.CharField(max_length=1110)
    contact_subject = models.CharField(max_length=11100)
    contact_message = models.CharField(max_length=111000)


class subscribe_model(models.Model):
    entry_num = models.AutoField(primary_key=True)
    subscribe_email = models.CharField(max_length=1110)
