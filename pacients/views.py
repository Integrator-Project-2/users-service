from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import PacientSerializer
from pacients.models import Pacient
from rest_framework.decorators import action

class CustomPacientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST': 
            return True
        return request.user and request.user.is_authenticated

class PacientViewSet(viewsets.ModelViewSet):
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer
    permission_classes = [CustomPacientPermission]

    @action(detail=True, methods=['post'])
    def update_token(self, request, pk=None):
        patient = self.get_object()
        token = request.data.get('expo_push_token')
        if token:
            patient.expo_push_token = token
            patient.save()
            return Response({"status": "Token atualizado com sucesso"})
        else:
            return Response({"error": "Token não fornecido"}, status=400)

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Delete method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)