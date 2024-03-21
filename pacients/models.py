from django.db import models

class Pacient(models.Model):
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    password = models.CharField()
    phone = models.CharField(max_length=11)
    adress = models.CharField()
    city = models.CharField()
    state = models.CharField(max_length=2)
    birth_date = models.DateField()
    
    def __str__(self):
        return self.nome

