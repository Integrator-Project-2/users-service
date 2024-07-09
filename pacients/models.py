from django.db import models
from authentication.models import User

class Pacient(models.Model):
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
