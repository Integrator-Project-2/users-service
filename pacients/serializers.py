from rest_framework import serializers
from .models import Pacient

class PacientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacient
        fields = ['id', 'name', 'email', 'cpf', 'password', 'phone', 'adress', 'city', 'state', 'birth_date']
