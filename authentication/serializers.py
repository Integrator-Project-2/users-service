from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User        
        fields = ['id', 'name', 'email', 'password', 'address', 'phone']
        
        extra_kwargs = {'password': {'write_only': True}}    
        
    def create(self, validated_data):
        
        # Captura a senha em texto plano
        plain_password = validated_data['password']
                
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            address=validated_data['address'],
            phone=validated_data['phone']
        )
                
        # Configura a senha criptografada e armazena a senha em texto plano temporariamente
        user.set_password(plain_password)
        user.plain_password = plain_password
        user.save()
        return user
    
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
