from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor 
import requests

@receiver(post_save, sender=Doctor)
def sync_doctor_to_gateway_database(sender, instance, created, **kwargs):
    if created:
        user = instance.user

        # Acessando a senha em texto plano armazenada temporariamente
        plain_password = user.plain_password

        user_data = {
            "email": user.email,
            "password": plain_password,  # Senha em texto plano
            "linked_user": user.id,
        }
        
        print("dados do usuário: ", user_data)

        api_gateway_url = "http://localhost:8004/api/create-user/"
        
        try:
            response = requests.post(api_gateway_url, json=user_data)
            print("sincronized: ", response)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao sincronizar médico com a API Gateway: {e}")
            
        # Removendo a senha em texto plano após enviar para a gateway
        user.plain_password = None
        user.save(update_fields=['plain_password'])
