from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer

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