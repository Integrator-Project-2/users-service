from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor 
import requests
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Doctor)
def sync_doctor_to_gateway_database(sender, instance, created, **kwargs):
    if created:
        user = instance.user

        # Acessando a senha em texto plano armazenada temporariamente
        plain_password = user.plain_password
        
        if plain_password is None:
            logger.error("Plain password not found for user %s", user.email)
            return

        user_data = {
            "email": user.email,
            "password": plain_password,  # Senha em texto plano
            "linked_user": user.id,
        }
        
        logger.info("User data to sync: %s", user_data)

        api_gateway_url = "http://localhost:8004/api/create-user/"
        
        try:
            response = requests.post(api_gateway_url, json=user_data)
            response.raise_for_status()
            logger.info("Successfully synchronized with API Gateway: %s", response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error("Error synchronizing doctor with API Gateway: %s", e)
            
        # Removendo a senha em texto plano após enviar para a gateway
        user.plain_password = None
