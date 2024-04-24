from rest_framework import serializers
from .models import Pacient
from authentication.serializers import UserSerializer

class PacientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Pacient
        fields = ['id', 'cpf', 'birth_date']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=
        user_data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()
            pacient = Pacient.objects.create(user=user, **validated_data)
            return pacient
        else:
            raise serializers.ValidationError(user_serializer.errors)
