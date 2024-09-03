from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import PacientSerializer
from pacients.models import Pacient

class CustomPacientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST': 
            return True
        return request.user and request.user.is_authenticated

class PacientViewSet(viewsets.ModelViewSet):
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer
    permission_classes = [CustomPacientPermission]

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Delete method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)