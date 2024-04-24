from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

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
