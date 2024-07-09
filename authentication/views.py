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
from django.contrib.auth import login  # Certifique-se de importar aqui
from django.views import View
from django.conf import settings
import requests
from django.shortcuts import redirect, HttpResponse

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

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')
        print(access_token)
        if not access_token:
            return Response({'error': 'No access token provided'}, status=400)
        
        # Validate token with Google token info endpoint
        validation_url = f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}'
        validation_response = requests.get(validation_url)
        
        if validation_response.status_code == 200:
            user_info = validation_response.json()
            email = user_info.get('email')
            
          
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
               
                user = User.objects.create_user(email=email)  
            
         
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            response = super().post(request, *args, **kwargs)
            if user and not Pacient.objects.filter(user=user).exists():
                response.data['requires_additional_info'] = True
            return response
        
        else:
            return Response({'error': 'Failed to validate access token'}, status=400)

class CompleteProfileView(APIView):
    def post(self, request):
        serializer = PacientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                    return HttpResponse(f'Access Token: {access_token}')
                else:
                    return HttpResponse('Failed to obtain access token', status=400)
            except requests.RequestException as e:
                return HttpResponse(f'Error: {str(e)}', status=500)
        else:
            return HttpResponse('No code provided', status=400)