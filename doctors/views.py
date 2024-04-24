from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomDoctorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [CustomDoctorPermission]
    
    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'PATCH method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'delete method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
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