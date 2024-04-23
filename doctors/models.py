from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    crm = models.CharField(max_length=13)
    email = models.CharField(unique=True)
    password = models.CharField()
    phone = models.CharField(max_length=11)
    address = models.CharField()
    city = models.CharField()
    state = models.CharField(max_length=2)
    birth_date = models.DateField()
    
    def __str__(self):
        return self.name
    