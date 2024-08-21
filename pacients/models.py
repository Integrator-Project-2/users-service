from django.db import models
from authentication.models import User

class Pacient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F','Female'),
        ('NB', 'Non-Binary')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True)
    height = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    allergies_and_observations = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nome
