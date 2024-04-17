from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

class DoctorManager(BaseUserManager):
    def create_doctor(self, name, crm, email, password=None, phone=None, address=None, city=None, state=None, birth_date=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        doctor = self.model(
            name=name,
            crm=crm,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            birth_date=birth_date,
            **extra_fields
        )
        doctor.set_password(password)
        doctor.save(using=self._db)
        return doctor


class Doctor(AbstractBaseUser):
    name = models.CharField(max_length=255)
    crm = models.CharField(max_length=13)
    email = models.EmailField(unique=True)
    password = models.CharField()
    phone = models.CharField(max_length=11)
    address = models.CharField()
    city = models.CharField()
    state = models.CharField(max_length=2)
    birth_date = models.DateField()
    username = None
    
    objects = DoctorManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self):
        return self.name
    