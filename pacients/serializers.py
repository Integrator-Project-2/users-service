from rest_framework import serializers
from .models import Pacient
from authentication.serializers import UserSerializer

class PacientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Pacient
        fields = ['id', 'cpf', 'user', 'gender', 'height', 'weight','allergies_and_observations', 'expo_push_token']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()
            pacient = Pacient.objects.create(user=user, **validated_data)
            return pacient
        else:
            raise serializers.ValidationError(user_serializer.errors)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        # Atualize o objeto User se fornecido
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)
        
        # Atualize os campos do Pacient
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
        
class PacientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacient
        fields = ['id', 'cpf', 'user']
