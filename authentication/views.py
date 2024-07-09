from django.http import JsonResponse
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from authentication.models import User
from pacients.serializers import PacientSerializer
from pacients.models import Pacient
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login 
from django.views import View
from django.conf import settings
import requests
from django.shortcuts import redirect, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            access_token = response.data.get('access')
            if refresh_token and access_token:
                response.set_cookie('refresh_token', refresh_token, httponly=True)
                response.set_cookie('access_token', access_token, httponly=True)
        return response


class GoogleCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        if code:
            data = {
                'code': code,
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': 'http://127.0.0.1:8001/api/auth/google/callback/',
                'grant_type': 'authorization_code',
            }
            try:
                response = requests.post('https://oauth2.googleapis.com/token', data=data)
                response_data = response.json()
                access_token = response_data.get('access_token')

                if access_token:
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
                    profile_response = requests.get(profile_url, headers=headers)
                    profile_data = profile_response.json()

    
                    email = profile_data.get('email')
                    name = profile_data.get('name')
                    phone_number = profile_data.get('phone_number') 

                    user, created = User.objects.get_or_create(email=email, defaults={'name': name})
                    
                    if phone_number:
                        user.phone_number = phone_number
                        user.save()
                  
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })

                else:
                    return JsonResponse({'error': 'Failed to obtain access token'}, status=400)

            except requests.RequestException as e:
                return JsonResponse({'error': f'Request error: {str(e)}'}, status=500)

        else:
            return JsonResponse({'error': 'No code provided'}, status=400)
