from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Doctor, User
from .serializers import DoctorSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny] 
    
    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'PATCH method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'delete method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_doctor_by_user_id(self, request, user_id=None):
        try:
            doctor = Doctor.objects.get(user__id=user_id)
            serializer = self.get_serializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)