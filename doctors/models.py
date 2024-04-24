from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from authentication.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crm = models.CharField(max_length=13)
    
    def __str__(self):
        return self.user.name

    