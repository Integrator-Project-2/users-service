from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User        
        fields = ['id', 'name', 'email', 'password', 'address', 'phone', 'birth_date']
        
        extra_kwargs = {'password': {'write_only': True}}    
    
    def create(self, validated_data):
        
        # Captura a senha em texto plano
        plain_password = validated_data['password']
                
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            address=validated_data['address'],
            phone=validated_data['phone'],
            birth_date=validated_data['birth_date']
        )
                
        # Configura a senha criptografada e armazena a senha em texto plano temporariamente
        user.set_password(plain_password)
        user.plain_password = plain_password
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        # Atualize os campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
